import os
from dotenv import load_dotenv

load_dotenv()
OWM_API_KEY = os.getenv("OWM_API_KEY")
LATITUDE    = os.getenv("LATITUDE")
LONGITUDE   = os.getenv("LONGITUDE")
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")

if not OWM_API_KEY:
    raise RuntimeError("Missing OWM_API_KEY in environment!")