import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    CUSTOMERS_FILE = os.path.join(DATA_DIR, 'clientes_ficticios.json')
    TEMPLATE_FILE = os.path.join(DATA_DIR, 'plantilla_ordenes.csv')
    PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
