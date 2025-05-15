import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import serial
from config import SERIAL_PORT
from sensors.parser import parse

ser = serial.Serial(SERIAL_PORT, 9600)
while True:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    data = parse(line)
    if data:
        print(data)