import os
import io
import csv
import json
import random
from datetime import datetime
from openpyxl import Workbook
from .config import Config

class GenerationService:
    def __init__(self):
        # Load Resources on init
        self._load_customers()
        self._load_template_headers()

    def _load_customers(self):
        try:
            with open(Config.CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
                self.customers = json.load(f)
        except Exception as e:
            print(f"Error loading customers: {e}")
            self.customers = []

    def _load_template_headers(self):
        try:
            with open(Config.TEMPLATE_FILE, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=';')
                self.headers = list(filter(None, next(reader)))
        except Exception as e:
            print(f"Error loading CSV template: {e}")
            self.headers = []

    def generate_excel(self, params):
        # Destructure params with safe defaults (validated by Frontend but be safe)
        count = params.get('cantidad_ordenes', 40)
        count = params.get('cantidad_ordenes', 40)
        # Default Items to 1 if not present or 0
        items_per_order = int(params.get('items_por_orden') or 1)
        if items_per_order < 1: items_per_order = 1
        # Capacity
        cap_min = params.get('capacidad_min', 1)
        cap_max = params.get('capacidad_max', 10)
        
        if cap_min > cap_max:
             raise ValueError("Capacity Min cannot be greater than Capacity Max")

        # Capacity 2 (Optional)
        cap2_min = params.get('capacidad2_min')
        cap2_max = params.get('capacidad2_max')
        
        # Tags (Optional)
        tags = params.get('tags', []) # List of {header, values}

        # Windows
        win1_start = params.get('ventana_inicio', '09:00')
        win1_end = params.get('ventana_fin', '18:00')
        win2_start = params.get('ventana2_inicio')
        win2_end = params.get('ventana2_fin')
        
        
        # Optional
        ct_origin = params.get('ct_origen')
        
        if not ct_origin or str(ct_origin).strip() == "":
             raise ValueError("CT Origen is mandatory.")
        service_time = params.get('service_time')
        
        # Geo
        city_filter = params.get('ciudad', '')
        country_filter = params.get('pais', '')
        delivery_date = params.get('fecha_entrega', datetime.now().strftime('%Y-%m-%d'))

        # Date formatting
        try:
            date_obj = datetime.strptime(delivery_date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d/%m/%Y')
        except:
            formatted_date = delivery_date

        # Filter customers
        filtered_customers = [c for c in self.customers if 
                              (city_filter.lower() in c.get('city', '').lower()) and 
                              (country_filter.lower() in c.get('country', '').lower())]
        
        if not filtered_customers:
            filtered_customers = self.customers # Fallback

        if not filtered_customers:
             raise ValueError("No customer data available to generate orders.")

        wb = Workbook()
        ws = wb.active
        ws.title = "Ordenes Generadas"
        
        # Append Dynamic Headers
        for tag in tags:
            header_name = tag.get('header')
            if header_name and header_name not in self.headers:
                self.headers.append(header_name)
        
        ws.append(self.headers)

        global_item_counter = 1

        for i in range(count):
            customer = random.choice(filtered_customers)
            order_id = f"ORD-{str(i+1).zfill(6)}"
            
            # Pre-calculate capacity for the whole order (shared across rows)
             # Use uniform for float range. Format to 4 decimal places and replace dot with comma
            cap_val = random.uniform(cap_min, cap_max)
            cap_str = f"{cap_val:.4f}".replace('.', ',')

            # Cap 2 Logic
            cap2_str = ""
            if cap2_min is not None and cap2_max is not None:
                c2_val = random.uniform(cap2_min, cap2_max)
                cap2_str = f"{c2_val:.4f}".replace('.', ',')

            # Generate multiple rows if items_per_order > 1
            for j in range(items_per_order):
                # Row dict
                row = {h: "" for h in self.headers}

                # --- Mapping Logic ---
                
                # 1. Customer Info (Shared)
                row["N° DOCUMENTO"] = order_id
                row["LATITUD"] = str(customer.get('lat', '')).replace('.', ',')
                row["LONGITUD"] = str(customer.get('long', '')).replace('.', ',')
                row["DIRECCION"] = customer.get('address', '')
                
                # Contact (Shared)
                row["NOMBRE CONTACTO"] = customer.get('name', '')
                row["IDENTIFICADOR CONTACTO"] = customer.get('id', '')
                row["TELEFONO"] = f"+569{random.randint(11111111,99999999)}"
                row["EMAIL CONTACTO"] = f"contacto{i}@example.com"

                # 2. Items (Distinct per row)
                row["NOMBRE ITEM"] = f"Item {global_item_counter}"
                row["CODIGO ITEM"] = f"SKU-{global_item_counter}" 
                row["CANTIDAD"] = "1" # 1 unit per line item
                row["COSTO ITEM"] = "1500" # Unit cost
                
                global_item_counter += 1

                # 3. Capacity (Shared)
                row["CAPACIDAD UNO"] = cap_str
                row["CAPACIDAD DOS"] = cap2_str
                
                # 4. Windows (Shared)
                row["FECHA MIN ENTREGA"] = formatted_date
                row["FECHA MAX ENTREGA"] = formatted_date
                row["MIN VENTANA HORARIA 1"] = win1_start
                row["MAX VENTANA HORARIA 1"] = win1_end
                
                if win2_start and win2_end:
                    row["MIN VENTANA HORARIA 2"] = win2_start
                    row["MAX VENTANA HORARIA 2"] = win2_end
                
                # 5. Optional Fields (Shared)
                if ct_origin:
                    row["CT ORIGEN"] = ct_origin
                else:
                    row["CT ORIGEN"] = "CD DEFAULT"
                    
                if service_time is not None:
                    row["SERVICE TIME"] = str(service_time)
                else:
                    row["SERVICE TIME"] = "5" # Default

                row["IMPORTANCIA"] = "1"
                
                # Dynamic Tags
                for tag in tags:
                    header = tag.get('header')
                    values = tag.get('values', [])
                    if header and values:
                        row[header] = random.choice(values)

                # Write Row
                # Check for explicit City/Country columns (if template has them) - Best effort
                if "CIUDAD" in self.headers:
                    row["CIUDAD"] = city_filter
                if "PAIS" in self.headers:
                    row["PAIS"] = country_filter

                ws.append([row.get(h, "") for h in self.headers])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        return output, f"ordenes_{count}.xlsx"
