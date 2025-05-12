from flask import Flask
from arduino.serial_handler import SerialHandler

def create_app():
    app = Flask(__name__)
    app.serial_handler = SerialHandler()
    
    # import blueprints
    from api.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app