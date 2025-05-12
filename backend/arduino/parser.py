def parse(line):
    try:
        parts = line.strip().split(':')
        if len(parts) != 3:
            return None
            
        # validate sensor ranges
        temp = float(parts[0])
        if not (-40 <= temp <= 85):  # C range
            return None
            
        pressure = float(parts[1])
        if not (300 <= pressure <= 1100):  # hPa range
            return None
            
        accel_z = float(parts[2])
        if not (-17000 <= accel_z <= 17000): # accel range
            return None
            
        return {
            'temp': temp,
            'pressure': pressure,
            'accel_z': accel_z
        }
    except (ValueError, IndexError, TypeError) as e:
        print(f"Invalid data: {line.strip()} - {str(e)}")
        return None