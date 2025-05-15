import serial
import time
from threading import Thread, Lock
from .parser import parse
from config import SERIAL_PORT

class SerialHandler:
    def __init__(self):
        self.ser = None
        self.latest_data = {}
        self.accel_buffer = []  # last N accelerometer readings
        self.buffer_size = 500  # 5 seconds of data at 100Hz (10ms intervals)
        self.lock = Lock()
        self.running = True
        self.connect()

    def connect(self):
        while self.running and not self.ser:
            try:
                self.ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
                self.ser.reset_input_buffer()  # clear old data
                Thread(target=self.read_serial, daemon=True).start()
                print(f"Connected to {SERIAL_PORT}")
            except serial.SerialException as e:
                print(f"Connection failed: {str(e)}. Retrying in 2s...")
                time.sleep(2)

    def read_serial(self):
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
                                self.accel_buffer.append(data['accel_z'])
                                if len(self.accel_buffer) > self.buffer_size:
                                    self.accel_buffer.pop(0)
            except serial.SerialException as e:
                print(f"Serial error: {str(e)}. Reconnecting...")
                self.close() 
                self.connect()
                time.sleep(2)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
            time.sleep(0.001)

    def get_latest_data(self):
        with self.lock:
            return self.latest_data.copy()

    def get_accel_history(self):
        with self.lock:
            return self.accel_buffer.copy()

    def close(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()