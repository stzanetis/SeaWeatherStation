import os
import serial
import time
import numpy as np
from threading import Thread, Lock
from .parser import parse
from config import SERIAL_PORT, MODE, LATITUDE, LONGITUDE

"""Handles sensor data simulation for DEMO mode"""
class SimulatedHandler:
    def __init__(self):
        self.latest_data = {
            'lat': float(LATITUDE),
            'lon': float(LONGITUDE),
            'signal': -70.0, # dBm
            'temp': 20.0, # C
            'pressure': 1013.25, # hPa
            'accel_z': 0
        }
        self.accel_buffer = []
        self.buffer_size = 500 # 5 seconds of data at 100Hz
        self.lock = Lock()
        self.running = True
        self._simulation_thread = None
        self._start_simulation()

    def _start_simulation(self):
        def simulation_loop():
            wave_freq = 0.5
            wave_amp = 1000
            noise_level = 0.1
            temp_base = 20.0
            pressure_base = 101325.0
            sig_base = -70.0 # base dBm
            lat = float(LATITUDE)  # static for demo
            lon = float(LONGITUDE) # static for demo
            
            while self.running:
                if np.random.rand() < 0.003:
                    wave_amp = np.clip(3000 + np.random.randn()*5000, 1000, 20000)
                    wave_freq = np.clip(0.1 + np.random.rand()*0.5, 0.08, 0.6)
                    noise_level = np.clip(0.3 + np.random.rand()*0.7, 0.2, 1.0)

                t = time.time()
                
                # simulate dBm fluctuations (-80dBm to -50dBm range)
                signal = sig_base + 10*np.sin(t/500)
                signal = np.clip(signal, -80, -50)
                
                # simulate environmental sensors (15C to 25C and 1003.25 to 1023.25)
                temp = temp_base + 5*np.sin(t/300)
                pressure = pressure_base + 1000*np.sin(t/600)
                
                # simulate acceleration data (-40000 to 40000)
                accel_z = int(
                    wave_amp*np.sin(2*np.pi*wave_freq*t) +
                    noise_level*wave_amp*np.random.randn()
                )

                with self.lock:
                    self.latest_data = {
                        'lat': lat,
                        'lon': lon,
                        'signal':   round(signal, 1),
                        'temp':     round(temp, 2),
                        'pressure': round(pressure/100, 2),
                        'accel_z':  int(accel_z)
                    }
                    self.accel_buffer.append(accel_z)
                    if len(self.accel_buffer) > self.buffer_size:
                        self.accel_buffer.pop(0)

                time.sleep(0.01)

        self._simulation_thread = Thread(target=simulation_loop, daemon=True)
        self._simulation_thread.start()

    def get_latest_data(self):
        with self.lock:
            return self.latest_data.copy()

    def get_accel_history(self):
        with self.lock:
            return self.accel_buffer.copy()

    def close(self):
        self.running = False
        if self._simulation_thread:
            self._simulation_thread.join(timeout=1)

"""Handles actual Arduino communication for DEPLOY mode"""
class RealHandler:
    def __init__(self):
        self.ser = None
        self.latest_data = {}
        self.accel_buffer = []
        self.buffer_size = 500
        self.lock = Lock()
        self.running = True
        self.max_retries = 3
        self._read_thread = None

        if not self._connect_retry():
            print("\nCRITICAL HARDWARE ERROR")
            print(f"Failed to connect to {SERIAL_PORT}")
            raise RuntimeError("Max connection attempts exceeded")

    def _connect_retry(self):
        from time import sleep
        attempts = 0
        
        while attempts < self.max_retries:
            print(f"➢ Attempt {attempts+1}/{self.max_retries}")
            if self._connect():
                return True
            attempts += 1
            backoff = 2**attempts
            print(f"Retrying in {backoff}s...")
            sleep(backoff)
        return False

    def _connect(self):
        try:
            # Open serial port
            self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
            print(f"Connected to {SERIAL_PORT}; waiting 2s for Arduino reboot…")
            time.sleep(2)

            # flush any garbled startup bytes
            self.ser.reset_input_buffer()
            # discard first line (likely partial)
            _ = self.ser.readline()

            # reader thread
            if not self._read_thread or not self._read_thread.is_alive():
                self._read_thread = Thread(target=self._read_serial, daemon=True)
                self._read_thread.start()

            print("Serial read thread started.")
            return True

        except serial.SerialException as e:
            print(f"Connection failed: {e}")
            return False

    def _read_serial(self):
        buffer = ""
        while self.running:
            try:
                if not self.ser or not self.ser.is_open:
                    if not self._connect_retry():
                        print("Could not reconnect; stopping reader.")
                        break
                    continue

                # Read all available bytes
                n = self.ser.in_waiting
                if n:
                    chunk = self.ser.read(n).decode('utf-8', errors='ignore')
                    buffer += chunk

                    # Process complete lines
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        clean = line.strip()
                        data = parse(clean)
                        if data:
                            with self.lock:
                                self.latest_data.update(data)
                                if 'accel_z' in data:
                                    self.accel_buffer.append(data['accel_z'])
                                    if len(self.accel_buffer) > self.buffer_size:
                                        self.accel_buffer.pop(0)
                        else:
                            # optional: log malformed line
                            # print(f"Bad line skipped: {clean}")
                            pass

                time.sleep(0.001)

            except serial.SerialException as e:
                print(f"Serial error: {e}; disconnecting…")
                self._disconnect()
            except Exception as e:
                # Catch any unexpected parsing/lock errors
                print(f"Read thread exception: {e}")

    def _disconnect(self):
        if self.ser:
            try:
                if self.ser.is_open:
                    self.ser.close()
                    print("Serial port closed.")
            except Exception as e:
                print(f"Error on close: {e}")
            finally:
                self.ser = None

    def get_latest_data(self):
        with self.lock:
            return self.latest_data.copy()

    def get_accel_history(self):
        with self.lock:
            return list(self.accel_buffer)

    def close(self):
        self.running = False
        self._disconnect()
        if self._read_thread:
            self._read_thread.join(timeout=1)

"""Unified interface for sensor data access"""
class SerialHandler:
    def __init__(self):
        if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
            print(f"\n{'='*50}")
            if MODE == "DEMO":
                print("INITIALIZING DEMO MODE".center(50))
                print("USING SIMULATED SENSOR DATA\n".center(50))
            else:
                print("INITIALIZING DEPLOY MODE".center(50))
                print("USING HARWARE ARDUINO SENSORS\n".center(50))
            
        self.handler = SimulatedHandler() if MODE == "DEMO" else RealHandler()

    def get_latest_data(self):
        return self.handler.get_latest_data()

    def get_accel_history(self):
        return self.handler.get_accel_history()

    def close(self):
        self.handler.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()