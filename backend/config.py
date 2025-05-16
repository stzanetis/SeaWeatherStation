import os
from dotenv import load_dotenv

load_dotenv()
MODE = os.getenv("MODE", "DEMO").upper()

OWM_API_KEY = os.getenv("OWM_API_KEY")
LATITUDE    = os.getenv("LATITUDE", "40.6273906")
LONGITUDE   = os.getenv("LONGITUDE", "22.9610895")

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyACM0")

if not OWM_API_KEY:
    raise RuntimeError("Missing OWM_API_KEY in environment!")