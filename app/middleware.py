"""
Security middleware and utilities
"""
from functools import wraps
from flask import request, jsonify
import time


class SecurityHeadersMiddleware:
    """Add security headers to responses"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        @app.after_request
        def add_security_headers(response):
            # Security headers
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
            # Cache control for API responses
            if request.path.startswith('/api'):
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            
            return response


class RequestLoggingMiddleware:
    """Log requests with timing"""
    
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        @app.before_request
        def before_request():
            request.start_time = time.time()
        
        @app.after_request
        def after_request(response):
            if hasattr(request, 'start_time'):
                duration = time.time() - request.start_time
                app.logger.info(
                    f"{request.method} {request.path} - {response.status_code} - {duration:.3f}s"
                )
            return response


def validate_content_length(max_length=10 * 1024 * 1024):  # 10MB default
    """Decorator to validate request content length"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_length and request.content_length > max_length:
                return jsonify({'error': 'Request too large'}), 413
            return f(*args, **kwargs)
        return decorated_function
    return decorator
