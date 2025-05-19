def parse(line):
    try:
        # Clean non-printable characters
        clean = ''.join([c if c.isprintable() else '' for c in line]).strip()
        # Skip lines with alphabetic characters (debug messages)
        if any(c.isalpha() and c not in {'E', '-', '+', '.'} for c in clean):
            return None
        
        parts = clean.split(':')
        # Full sensor mode (lat:lon:signal:temp:pressure:accel_z)
        if len(parts) == 6:
            valid_parts = []
            for p in parts:
                p_clean = p.strip().replace('-', '', 1)  # Allow '-' for negatives
                if p_clean.replace('.', '', 1).lstrip('-').isdigit() and p_clean:
                    valid_parts.append(float(p))
                else:
                    return None  # Invalid part
            
            lat, lon, signal, temp, pressure, accel_z = valid_parts
            if all([
                -90 <= lat <= 90,          # valid latitude
                -180 <= lon <= 180,        # valid longitude
                -120 <= signal <= 0,       # dBm
                -40 <= temp <= 85,
                300 <= pressure <= 1100,
                -17000 <= accel_z <= 17000
            ]):
                return {
                    'lat': lat,
                    'lon': lon,
                    'signal': signal,
                    'temp': temp,
                    'pressure': pressure,
                    'accel_z': accel_z
                }
        
        # Accelerometer-only mode
        elif len(parts) == 1:
            p_clean = parts[0].strip().replace('-', '', 1)
            if p_clean.replace('.', '', 1).lstrip('-').isdigit() and p_clean:
                accel_z = float(parts[0])
                if -17000 <= accel_z <= 17000:
                    return {'accel_z': accel_z}
                    
        return None
    except Exception as e:
        print(f"Rejected line: '{clean}'")
        return None