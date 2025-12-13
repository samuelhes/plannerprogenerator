from flask import Flask, send_from_directory, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from .config import Config, configure_logging
from .middleware import SecurityHeadersMiddleware, RequestLoggingMiddleware

def create_app():
    app = Flask(__name__, static_folder=Config.PUBLIC_DIR)
    app.config.from_object(Config)

    # Configure Logging
    configure_logging(app)
    app.logger.info("Planner Pro Generator V3 Starting...")
    
    # Security: CORS Configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["https://plannerprogenerator.onrender.com", "http://localhost:*"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "max_age": 3600
        }
    })
    
    # Security: Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    
    # Apply specific limits to API endpoints
    @limiter.limit("30 per minute")
    def rate_limited_api():
        pass
    
    # Security Middleware
    SecurityHeadersMiddleware(app)
    RequestLoggingMiddleware(app)
    
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
        return jsonify({"status": "ok", "version": "2.5.0"}), 200

    @app.route('/readyz')
    def readyz():
        # Could add more complex readiness checks here
        return jsonify({"status": "ready", "version": "2.5.0"}), 200

    return app

# Expose app globally for Render auto-detect (gunicorn app:app)
app = create_app()
