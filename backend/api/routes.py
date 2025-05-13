import os
from flask import Blueprint, jsonify
from flask import current_app 
from analysis.wave_analysis import wave_metrics
from analysis.shore_impact import inundation
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
    handler = current_app.serial_handler
    data = handler.get_latest_data()
    return jsonify({
        'temperature': data.get('temp'),
        'pressure':    data.get('pressure')
    })

@main_bp.route('/waves')
def get_waves():
    handler = current_app.serial_handler
    accel_data = handler.get_accel_history()
    metrics = wave_metrics(accel_data)
    shore_runup = inundation(metrics)
    return jsonify(shore_runup)

@main_bp.route('/weather')
def get_weather():
    try:
        api_key = os.getenv("OWM_API_KEY")
        lat = os.getenv("LATITUDE")
        lon = os.getenv("LONGITUDE")
        
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        
        weather_data = resp.json()
        return jsonify({
            'wind_speed': weather_data['wind'].get('speed', 0),
            'wind_direction': weather_data['wind'].get('deg', 0),
            'condition': weather_data['weather'][0]['main'] if weather_data['weather'] else 'unknown',
            'description': weather_data['weather'][0]['description'] if weather_data['weather'] else 'unknown'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500