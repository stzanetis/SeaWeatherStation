def parse(line):
    try:
        parts = line.strip().split(':')
        
        # accelerometer-only mode (single value)
        if len(parts) == 1:
            accel_z = float(parts[0])
            if -17000 <= accel_z <= 17000:
                return {'accel_z': accel_z}
            return None
            
        # full sensor mode (three values)
        elif len(parts) == 3:
            temp     = float(parts[0])
            pressure = float(parts[1])
            accel_z  = float(parts[2])
            if all([
                -40 <= temp <= 85,
                300 <= pressure <= 1100,
                -17000 <= accel_z <= 17000
            ]):
                return {
                    'temp': temp,
                    'pressure': pressure,
                    'accel_z': accel_z
                }
        return None
    except (ValueError, IndexError, TypeError) as e:
        print(f"Invalid data: {line.strip()} - {str(e)}")
        return None