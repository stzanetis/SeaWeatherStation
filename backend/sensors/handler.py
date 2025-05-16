import os
import serial
import time
import numpy as np
from threading import Thread, Lock
from .parser import parse
from config import SERIAL_PORT, MODE

"""Handles sensor data simulation for DEMO mode"""
class SimulatedHandler:
    def __init__(self):

        self.latest_data = {
            'temp': 20.0,
            'pressure': 1013.25,
            'accel_z': 0
        }
        self.accel_buffer = []
        self.buffer_size = 500  # 5 seconds of data at 100Hz
        self.lock = Lock()
        self.running = True
        self._simulation_thread = None
        self._start_simulation()

    def _start_simulation(self):

        def simulation_loop():

            wave_freq = 0.5
            wave_amp = 8000
            noise_level = 0.2
            temp_base = 20.0
            pressure_base = 101325.0
            
            while self.running:

                if np.random.rand() < 0.01:  # 1% chance per iteration to change
                    wave_freq   = np.clip(0.3  + np.random.rand() *0.7,  0.2,  1.0)
                    wave_amp    = np.clip(5000 + np.random.randn()*2000, 3000, 15000)
                    noise_level = np.clip(0.1  + np.random.rand() *0.4,  0.05, 0.5)

                t = time.time()
                
                # simulate environmental sensors
                temp = temp_base + 5*np.sin(t/300)  # 5min cycle
                pressure = pressure_base + 1000*np.sin(t/600)  # 10min cycle
                
                # generate acceleration data
                accel_z = int(
                    wave_amp*np.sin(2*np.pi*wave_freq*t) +
                    noise_level*wave_amp*np.random.randn()
                )

                with self.lock:

                    self.latest_data = {
                        'temp': round(temp, 2),
                        'pressure': round(pressure/100, 2),
                        'accel_z': int(accel_z)
                    }
                    
                    self.accel_buffer.append(accel_z)
                    if len(self.accel_buffer) > self.buffer_size:
                        self.accel_buffer.pop(0)

                # 100Hz sampling rate
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
        self.retry_count = 0
        
        if not self._connect_retry():
            print("\nCRITICAL HARDWARE ERROR")
            print(f"Failed to connect to {SERIAL_PORT}")
            print("Verify Arduino is connected and port is correct")
            raise RuntimeError("Max connection attempts exceeded")

    def _connect_retry(self):

        from time import sleep
        print(f"Attempting connection to {SERIAL_PORT}")
        
        while self.retry_count < self.max_retries:
            print(f"➢ Attempt {self.retry_count+1}/{self.max_retries}")
            if self._connect():
                return True
            self.retry_count += 1
            if self.retry_count < self.max_retries:
                sleep_time = 2 ** self.retry_count
                print(f"Retrying in {sleep_time}s...")
                sleep(sleep_time)
        return False

    def _connect(self):
        try:
            self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
            self.ser.reset_input_buffer()
            print(f"Connected to {SERIAL_PORT}")
            Thread(target=self._read_serial, daemon=True).start()
            return True
        except serial.SerialException as e:
            print(f"Connection failed: {str(e)}")
            return False
    
    def _read_serial(self):

        while self.running and self.ser:
            try:
                if self.ser.in_waiting > 0:
                    raw_data = self.ser.readline()
                    line = raw_data.decode('utf-8', errors='ignore').strip()
                    if line:
                        data = parse(line)
                        if data:
                            with self.lock:
                                self.latest_data = data
                                if 'accel_z' in data:
                                    self.accel_buffer.append(data['accel_z'])
                                    if len(self.accel_buffer) > self.buffer_size:
                                        self.accel_buffer.pop(0)
                time.sleep(0.001)
            except serial.SerialException as e:
                print(f"Serial error: {str(e)}")
                self._disconnect()
                
                if self.retry_count >= self.max_retries:
                    print(f"Maximum reconnection attempts ({self.max_retries}) reached. Giving up.")
                    self.running = False
                    break
                    
                print(f"Reconnection attempt {self.retry_count+1}/{self.max_retries}")
                if not self._connect():
                    time.sleep(1)  # wait before next attempt
            except Exception as e:
                print(f"Unexpected error: {str(e)}")

    def _disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.ser = None

    def get_latest_data(self):
        with self.lock:
            return self.latest_data.copy()

    def get_accel_history(self):
        with self.lock:
            return self.accel_buffer.copy()

    def close(self):
        self.running = False
        self._disconnect()

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