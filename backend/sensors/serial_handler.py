import serial
import time
from threading import Thread, Lock
from .parser import parse

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
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            Thread(target=self.read_serial, daemon=True).start()
        except serial.SerialException as e:
            print(f"Arduino connection failed: {str(e)}")

    def read_serial(self):
        while self.running and self.ser:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    data = parse(line)
                    if data:
                        with self.lock:
                            self.latest_data = data
                            # Update accelerometer buffer
                            self.accel_buffer.append(data['accel_z'])
                            if len(self.accel_buffer) > self.buffer_size:
                                self.accel_buffer.pop(0)
            except (serial.SerialException, UnicodeDecodeError) as e:
                print(f"Serial read error: {str(e)}")
                time.sleep(1)
            time.sleep(0.001)  # match 10ms sampling rate

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