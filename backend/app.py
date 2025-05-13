from flask import Flask
from flask_cors import CORS
from sensors.serial_handler import SerialHandler

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.serial_handler = SerialHandler()
    
    # import blueprints
    from api.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app