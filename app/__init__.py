from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    CORS(app)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "healthcare-ai-secret-2024")
    app.config["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

    from app.routes.main import main_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
