from app.services import GenerationService
import io

# Mock Config
class MockConfig:
    CUSTOMERS_FILE = 'data/customers.json'
    TEMPLATE_FILE = 'data/template.csv'
    ADDRESSES_SHEET_URL = None

import app.services
app.services.Config = MockConfig

def verify_vehicles():
    service = GenerationService()
    
    # Mock groups
    groups = [
        {
            "type": "Moto",
            "count": 2,
            "capacity1": 100,
            "origin": "CD TEST",
            "start_time": "08:00",
            "end_time": "18:00"
        }
    ]

    print("Generating Vehicle CSV...")
    mem, filename = service.generate_vehicles_excel(groups)
    
    content = mem.getvalue().decode('utf-8')
    
    print("\n--- OUTPUT PREVIEW ---")
    print(content)
    print("--- END PREVIEW ---\n")

    # Assertions
    expected_header = "PLACA;ORIGEN;DESTINO;CAPACIDAD UNO;CAPACIDAD DOS;HORA INICIO JORNADA;HORA FIN JORNADA;INICIO HORA DESCANSO;FIN HORA DESCANSO;COSTO POR SALIDA;COSTO POR KILOMETRO;COSTO POR HORA;COSTO FIJO;MAXIMA CANTIDAD DE ENTREGAS POR RECORRIDO;MAXIMO TIEMPO DE MANEJO [HORAS];MAXIMA CANTIDAD DE RECORRIDOS;DISTANCIA MAXIMA POR RECORRIDO [KILOMETROS];VELOCIDAD VEHICULO;PERIODO DE RECARGA [HORAS];MAXIMO DE DINERO;NO CONSIDERAR RETORNO AL CD;"
    
    lines = content.splitlines()
    header_line = lines[0]
    
    if header_line.strip() == expected_header.strip():
        print("✅ Header Match Success")
    else:
        print("❌ Header Mismatch")
        print(f"Expected: {expected_header}")
        print(f"Got:      {header_line}")

    # Check delimiter count (21 fields + trailing = 22 semicolons? Let's check string logic)
    # The header string has 21 semicolons.
    if header_line.count(';') >= 21:
         print(f"✅ Delimiter Count Safe ({header_line.count(';')})")
    else:
         print(f"❌ Delimiter Count Mismatch: Got {header_line.count(';')}")

    # Check data row
    data_row = lines[1]
    if "MOTO01" in data_row and "CD TEST" in data_row and "100" in data_row:
         print("✅ Data Presence Verified")
    
    # Check constants (e.g. 5500000 max money)
    if "5500000" in data_row:
         print("✅ Constants (Money) Verified")

if __name__ == "__main__":
    verify_vehicles()
