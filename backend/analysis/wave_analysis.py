import numpy as np
from scipy.fft import fft
from scipy.signal import find_peaks

def wave_metrics(accelerometer_data, sampling_rate=100):
    if len(accelerometer_data) < 100:  # Minimum 1 second of data
        return {'frequency': 0.0, 'height': 0.0}
    
    # Convert to m/s² (assuming sensor sensitivity)
    accel_g = np.array(accelerometer_data) / 16384.0  # For ±2g range
    
    # remove DC offset
    accel_clean = accel_g - np.mean(accel_g)
    
    # FFT
    n = len(accel_clean)
    yf = fft(accel_clean)
    xf = np.linspace(0.0, sampling_rate/2, n//2)
    
    # dominant frequency between 0.05-1 Hz (typical ocean waves)
    mask = (xf >= 0.05) & (xf <= 1.0)
    valid_freq = xf[mask]
    valid_mag = 2.0/n * np.abs(yf[:n//2][mask])

    if len(valid_mag) == 0:
        return {'frequency': 0.0, 'height': 0.0}

    idx = np.argmax(valid_mag)
    frequency = valid_freq[idx]
    
    # height estimation (peak-to-peak in vertical displacement)
    peaks, _ = find_peaks(accel_clean, distance=sampling_rate//2)
    troughs, _ = find_peaks(-accel_clean, distance=sampling_rate//2)
    
    if len(peaks) > 1 and len(troughs) > 1:
        max_peak = np.max(accel_clean[peaks])
        min_trough = np.min(accel_clean[troughs])
        wave_height = (max_peak - min_trough) * 0.5
    else:
        wave_height = np.std(accel_clean) * 0.3
    
    return {
        'frequency': round(float(frequency), 2),
        'height': round(float(wave_height), 2)
    }