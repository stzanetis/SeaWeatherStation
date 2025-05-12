import numpy as np
from scipy.fft import fft

def wave_metrics(accelerometer_data, sampling_rate=10):

    # TODO: Implement this properly
    
    if len(accelerometer_data) < 10:
        return {'frequency': 0, 'height': 0}
    
    # FFT
    n = len(accelerometer_data)
    y = fft(accelerometer_data)
    xf = np.linspace(0.0, 1.0/(2.0/sampling_rate), n//2)
    
    # wave dominant frequency (placeholder calculation)
    idx = np.argmax(np.abs(y[0:n//2]))
    frequency = xf[idx]
    
    # wave height (placeholder calculation)
    wave_height = np.var(accelerometer_data)*100
    
    return {
        'frequency': round(float(frequency), 2),
        'height': round(float(wave_height), 2)
    }