import numpy as np

def wave_metrics(accelerometer_data, sampling_rate=100):
    if len(accelerometer_data) < 10:
        return {'frequency': 0.0, 'height': 0.0}
    if not accelerometer_data:
        return {'frequency': 0.0, 'height': 0.0}
    
    # convert raw LSB to m/s² (MPU6050 at +/-2g: 16384 LSB/g)
    lsb_to_ms2 = 9.81 / 16384
    data = np.array(accelerometer_data) * lsb_to_ms2
    data = data - np.mean(data)  # remove DC offset
    
    n = len(data)
    if n < 10:
        return {'frequency': 0.0, 'height': 0.0}
    
    """calculate dominant frequency using FFT"""
    fft = np.fft.rfft(data)
    fft_freqs = np.fft.rfftfreq(n, d=1.0/sampling_rate)
    magnitudes = np.abs(fft)
    
    # ignore very low frequencies (below 0.1 Hz) to filter out drift/noise
    valid_freqs = fft_freqs >= 0.1
    valid_magnitudes = magnitudes.copy()
    valid_magnitudes[~valid_freqs] = 0
    
    if np.max(valid_magnitudes) == 0:
        dominant_freq = 0.0
    else:
        dominant_freq = fft_freqs[np.argmax(valid_magnitudes)]
    
    """calculate wave height using physics-based heuristic"""
    std_accel = np.std(data)
    scaling_factor = 0.25  # derived from sinusoidal motion relationship
    
    if dominant_freq <= 0:
        wave_height = 0.0
    else:
        wave_height = scaling_factor*std_accel / (dominant_freq**2)
    
    return {
        'frequency': round(float(dominant_freq), 2),
        'height':    round(float(wave_height), 2)
    }