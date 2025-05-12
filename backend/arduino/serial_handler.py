import serial
import time
from threading import Thread
from .parser import parse

class SerialHandler:
    def __init__(self):
        self.measurement_order = ['temp', 'pressure', 'accel_z']
        self.current_measurement = 0
        self.ser = None
        self.latest_data = {}
        self.running = True
        self.connect()
        
    def connect(self):
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            Thread(target=self.read_serial).start()
        except serial.SerialException:
            print("Arduino not connected!")

    def read_serial(self):
        while self.running and self.ser:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                data = parse(line)
                if data:
                    key = self.measurement_order[self.current_measurement]
                    self.latest_data[key] = data['raw_value']
                    self.current_measurement = (self.current_measurement + 1) % 3
            time.sleep(0.1)

    def get_latest_data(self):
        return self.latest_data

    def close(self):
        self.running = False
        if self.ser:
            self.ser.close()