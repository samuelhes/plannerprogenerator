from flask import Flask, send_from_directory, jsonify
from .config import Config, configure_logging

def create_app():
    app = Flask(__name__, static_folder=Config.PUBLIC_DIR)
    app.config.from_object(Config)

    # Configure Logging
    configure_logging(app)
    app.logger.info("Planner Pro Generator V3 Starting...")
    
    # Register API Blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(Config.PUBLIC_DIR, 'index.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(Config.PUBLIC_DIR, path)

    # Health Checks (World Class Standard)
    @app.route('/healthz')
    def healthz():
        return jsonify({"status": "ok", "version": "2.5.1"}), 200

    @app.route('/readyz')
    def readyz():
        return jsonify({"status": "ready", "version": "2.5.1"}), 200

    return app

# Expose app globally for Render auto-detect (gunicorn app:app)
app = create_app()
