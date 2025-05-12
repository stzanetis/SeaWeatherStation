from flask import Blueprint, jsonify
from flask import current_app 
from analysis.frequency import wave_metrics
from arduino.serial_handler import SerialHandler
from dotenv import load_dotenv
import requests

load_dotenv()
main_bp = Blueprint('main', __name__)

@main_bp.route('/status')
def get_status():
    # TODO: Implement this properly
    return jsonify({
        'online': True,
        'battery': 85,
        'signal_strength': 75
    })

@main_bp.route('/info')
def get_info():
    handler = current_app.SerialHandler()
    data = handler.get_latest_data()
    return jsonify({
        'temperature': data.get('temp'),
        'pressure':    data.get('pressure')
    })

@main_bp.route('/waves')
def get_waves():
    handler = current_app.SerialHandler()
    data = handler.get_latest_data()
    z_values = [data.get('accel_z', 0)]
    # TODO: Implement wave prediction
    metrics = wave_metrics(z_values)
    return jsonify(metrics)

@main_bp.route('/weather')
def get_weather():
    api_key = os.getenv("OWM_API_KEY")
    lat     = os.getenv("LATITUDE")
    lon     = os.getenv("LONGITUDE")

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}"
        f"&appid={api_key}&units=metric"
    )
    resp = requests.get(url).json()
    return jsonify({
        'wind_speed':     resp['wind']['speed'],
        'wind_direction': resp['wind']['deg'],
        'condition':      resp['weather'][0]['main']
    })