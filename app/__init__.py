from flask import Flask, send_from_directory
from .config import Config

def create_app():
    app = Flask(__name__, static_folder=Config.PUBLIC_DIR)
    
    # Register API Blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(Config.PUBLIC_DIR, 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(Config.PUBLIC_DIR, path)

    return app
