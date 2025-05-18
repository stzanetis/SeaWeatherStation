def parse(line):
    try:
        # clean non-printable characters
        clean = ''.join([c if c.isprintable() else '' for c in line]).strip()
        # skip lines with alphabetic characters (debug messages)
        if any(c.isalpha() and c not in {'E', '-', '+'} for c in clean):
            return None
        
        parts = clean.split(':')
        # full sensor mode
        if len(parts) == 3:
            valid_parts = []
            for p in parts:
                p_clean = p.strip().replace('-', '', 1)  # allow '-' for negatives
                if p_clean.replace('.', '', 1).isdigit() and p_clean:
                    valid_parts.append(float(p))
                else:
                    return None  # invalid part
            
            temp, pressure, accel_z = valid_parts
            if all([
                -40 <= temp <= 85,
                300 <= pressure <= 1100,
                -17000 <= accel_z <= 17000
            ]):
                return {'temp': temp, 'pressure': pressure, 'accel_z': accel_z}
        
        # accelerometer-only mode
        elif len(parts) == 1:
            p_clean = parts[0].strip().replace('-', '', 1)
            if p_clean.replace('.', '', 1).isdigit() and p_clean:
                accel_z = float(parts[0])
                if -17000 <= accel_z <= 17000:
                    return {'accel_z': accel_z}
                    
        return None
    except Exception as e:
        print(f"Rejected line: '{clean}'")
        return None