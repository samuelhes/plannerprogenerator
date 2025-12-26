from app.services import GenerationService
import io

# Mock Config
class MockConfig:
    # Dummy paths, service should be robust enough or we mock internal methods
    CUSTOMERS_FILE = 'data/customers.json'
    TEMPLATE_FILE = 'data/template.csv'
    ADDRESSES_SHEET_URL = None

import app.services
app.services.Config = MockConfig

def verify_csv():
    # Instantiate
    service = GenerationService()
    
    # Mock specific internal method to avoid file dependency
    service.customers = [
        {"address": "Test 1, Santiago", "country": "Chile", "city": "Santiago", "lat": -33.1, "long": -70.1, "id": "123", "name": "Tester"},
        {"address": "Test 2, Viña", "country": "Chile", "city": "Viña del mar", "lat": -33.2, "long":-70.2, "id": "456", "name": "Tester 2"}
    ]
    
    params = {
        "cantidad_ordenes": 5,
        "pais": "Chile",
        "ciudad": "Santiago",
        "fecha_entrega": "2025-12-31",
        "capacidad_min": 0.001,
        "capacidad_max": 0.005,
        "ct_origen": "CD TEST"
    }

    print("Generating CSV...")
    mem, filename = service.generate_excel(params)
    
    content = mem.getvalue().decode('utf-8')
    
    print("\n--- OUTPUT PREVIEW ---")
    print(content)
    print("--- END PREVIEW ---\n")

    # Assertions
    expected_header = "N° DOCUMENTO;LATITUD;LONGITUD;DIRECCION;NOMBRE ITEM;CANTIDAD;CODIGO ITEM;FECHA MIN ENTREGA;FECHA MAX ENTREGA;MIN VENTANA HORARIA 1;MAX VENTANA HORARIA 1;MIN VENTANA HORARIA 2;MAX VENTANA HORARIA 2;COSTO ITEM;CAPACIDAD UNO;CAPACIDAD DOS;SERVICE TIME;IMPORTANCIA;IDENTIFICADOR CONTACTO;NOMBRE CONTACTO;TELEFONO;EMAIL CONTACTO;CT ORIGEN;"
    
    lines = content.splitlines()
    header_line = lines[0]
    
    if header_line.strip() == expected_header.strip():
        print("✅ Header Match Success")
    else:
        print("❌ Header Mismatch")
        print(f"Expected: {expected_header}")
        print(f"Got:      {header_line}")

    # Check delimiter count (23 fields = 23 semicolons because of trailing semicolon)
    if header_line.count(';') == 23:
         print("✅ Delimiter Count Correct (23)")
    else:
         print(f"❌ Delimiter Count Mismatch: Got {header_line.count(';')}")

    # Check decimal format in second line
    first_row = lines[1].split(';')
    # Capacidad Uno is index 14
    cap_val = first_row[14]
    if ',' in cap_val and '.' not in cap_val:
        print(f"✅ Decimal Format Correct: {cap_val}")
    else:
        print(f"❌ Decimal Format Issue: {cap_val}")

if __name__ == "__main__":
    verify_csv()
