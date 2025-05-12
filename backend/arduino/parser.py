def parse(line):
    try:
        data = {}
        parts = line.split(',')
        for part in parts:
            key, value = part.split(':')
            data[key.strip().lower()] = float(value)
        return data
    except:
        return None