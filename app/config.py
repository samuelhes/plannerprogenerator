import os
import logging
import sys

class Config:
    # 1. Base Paths
    # 1. Base Paths
    # Assuming structure: /root/app/config.py
    # We want: /root/public
    
    # Current File: .../app/config.py
    APP_DIR = os.path.dirname(os.path.abspath(__file__)) # .../app
    ROOT_DIR = os.path.dirname(APP_DIR) # .../
    
    PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
    DATA_DIR = os.path.join(ROOT_DIR, 'data')
    
    # 2. Data Files
    CUSTOMERS_FILE = os.environ.get('CUSTOMERS_FILE', os.path.join(DATA_DIR, 'clientes_ficticios.json'))
    TEMPLATE_FILE = os.environ.get('TEMPLATE_FILE', os.path.join(DATA_DIR, 'plantilla_ordenes.csv'))
    TEMPLATE_PATH = os.path.join(DATA_DIR, 'plantilla_ordenes.csv')
    
    # 3. External Services (Google Sheets)
    # Default is the specific sheet requested, but overridable.
    ADDRESSES_SHEET_URL = os.environ.get(
        'ADDRESSES_SHEET_URL', 
        'https://docs.google.com/spreadsheets/d/1i71QcFcWq6QeWYloVCujokPZWRhXGi0y-1Cjt6DsGX4/export?format=csv'
    )
    
    # 4. App Settings
    PORT = int(os.environ.get('PORT', 3000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

def configure_logging(app):
    """
    Configure JSON-friendly logging for Cloud Run.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(app.config['LOG_LEVEL'])
    
    # Basic format for now. For true JSON, we might need a custom formatter, 
    # but standard logging is often good enough for Cloud Run if formatted cleanly.
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    handler.setFormatter(formatter)
    
    app.logger.addHandler(handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    # Remove default handlers to avoid duplicate logs
    app.logger.handlers = [handler]
