import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sensors.serial_handler import SerialHandler
from analysis.wave_analysis import wave_metrics


def capture_test_data(duration=30):
    """Capture live data for testing"""
    handler = SerialHandler()
    samples = []
    
    print(f"Capturing {duration} seconds of data...")
    for _ in range(duration*100):  # 100Hz × duration
        samples.extend(handler.get_accel_history())
        time.sleep(0.01)
    
    return np.array(samples)

def plot(data):
    """Visualize raw data and FFT results"""
    # Time domain plot
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(data)) / 100, data)  # X-axis in seconds
    plt.title("Raw Accelerometer Data")
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s²)")

    # Frequency analysis
    metrics = wave_metrics(data.tolist())
    n = len(data)
    yf = np.fft.fft(data)
    xf = np.linspace(0.0, 100/2, n//2)
    
    plt.subplot(2, 1, 2)
    plt.plot(xf, 2.0/n * np.abs(yf[:n//2]))
    plt.title("FFT Analysis")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.axvline(metrics['frequency'], color='r', linestyle='--', 
               label=f"Dominant {metrics['frequency']}Hz")
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_data = capture_test_data()
    plot(test_data)