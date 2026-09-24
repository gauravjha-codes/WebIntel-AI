import os
import sys

# Force UTF-8 on Windows terminal stdout and stderr to prevent cp1252 encoding crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure workspace root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask
from flask_cors import CORS
from config import FLASK_HOST, FLASK_PORT, FLASK_DEBUG, FLASK_USE_RELOADER
from src.routes.web_routes import web_bp
from src.routes.api_routes import api_bp

def create_app() -> Flask:
    """Application factory for initializing Flask with CORS and Blueprints."""
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG, use_reloader=FLASK_USE_RELOADER)
