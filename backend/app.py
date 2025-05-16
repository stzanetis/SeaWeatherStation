import sys
from flask import Flask
from flask_cors import CORS
from sensors.handler import SerialHandler
from config import MODE

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    try:
        app.serial_handler = SerialHandler()
    except Exception as e:
        if MODE == "DEPLOY":
            print("\nDEPLOY MODE FAILED - ARDUINO CONNECTION REQUIRED")
            print(f"Error: {str(e)}")
            print("Either connect Arduino or restart with DEMO mode")
            sys.exit(1)  # hard exit for deploy failures
        
        raise e

    from api.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app