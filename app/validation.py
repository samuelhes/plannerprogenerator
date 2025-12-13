"""
Input validation utilities for Planner Pro Generator
"""
from datetime import datetime

class ValidationError(ValueError):
    """Custom validation error"""
    pass

def validate_order_params(params: dict) -> dict:
    """
    Validates and sanitizes order generation parameters
    Returns sanitized params or raises ValidationError
    """
    sanitized = {}
    
    # Validate количество_ordenes (required)
    try:
        count = int(params.get('cantidad_ordenes', 0))
        if count \u003c 1 or count \u003e 10000:
            raise ValidationError("La cantidad de órdenes debe estar entre 1 y 10,000")
        sanitized['cantidad_ordenes'] = count
    except (ValueError, TypeError):
        raise ValidationError("Cantidad de órdenes inválida")
    
    # Validate items_por_orden (optional, defaults to 1)
    try:
        items = int(params.get('items_por_orden') or 1)
        if items \u003c 1 or items \u003e 100:
            raise ValidationError("Ítems por orden debe estar entre 1 y 100")
        sanitized['items_por_orden'] = items
    except (ValueError, TypeError):
        sanitized['items_por_orden'] = 1
    
    # Validate CT Origen (required)
    ct_origen = params.get('ct_origen', '').strip()
    if not ct_origen:
        raise ValidationError("CT Origen es obligatorio")
    sanitized['ct_origen'] = ct_origen
    
    # Validate fecha_entrega (required)
    fecha = params.get('fecha_entrega')
    if not fecha:
        raise ValidationError("Fecha de entrega es obligatoria")
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        sanitized['fecha_entrega'] = fecha
    except (ValueError, TypeError):
        raise ValidationError("Formato de fecha inválido (debe ser YYYY-MM-DD)")
    
    # Validate capacidades (required)
    try:
        cap_min = float(params.get('capacidad_min', 0))
        cap_max = float(params.get('capacidad_max', 0))
        if cap_min \u003c 0 or cap_max \u003c 0:
            raise ValidationError("Las capacidades no pueden ser negativas")
        if cap_min \u003e cap_max:
            raise ValidationError("Capacidad mínima no puede ser mayor que la máxima")
        sanitized['capacidad_min'] = cap_min
        sanitized['capacidad_max'] = cap_max
    except (ValueError, TypeError):
        raise ValidationError("Valores de capacidad inválidos")
    
    # Validate capacidades 2 (optional)
    cap2_min = params.get('capacidad2_min')
    cap2_max = params.get('capacidad2_max')
    if cap2_min is not None and cap2_max is not None:
        try:
            cap2_min = float(cap2_min)
            cap2_max = float(cap2_max)
            if cap2_min \u003c 0 or cap2_max \u003c 0:
                raise ValidationError("Capacidad 2: valores no pueden ser negativos")
            if cap2_min \u003e cap2_max:
                raise ValidationError("Capacidad 2: mínima no puede ser mayor que máxima")
            sanitized['capacidad2_min'] = cap2_min
            sanitized['capacidad2_max'] = cap2_max
        except (ValueError, TypeError):
            pass  # Optional, so skip if invalid
    
    # Validate ventana horaria 1 (required)
    v1_inicio = params.get('ventana_inicio', '').strip()
    v1_fin = params.get('ventana_fin', '').strip()
    if not v1_inicio or not v1_fin:
        raise ValidationError("Ventana horaria 1 es obligatoria")
    sanitized['ventana_inicio'] = v1_inicio
    sanitized['ventana_fin'] = v1_fin
    
    # Validate ventana horaria 2 (optional)
    v2_inicio = params.get('ventana2_inicio', '').strip()
    v2_fin = params.get('ventana2_fin', '').strip()
    if v2_inicio:
        sanitized['ventana2_inicio'] = v2_inicio
    if v2_fin:
        sanitized['ventana2_fin'] = v2_fin
    
    # Pass through other optional fields
    for key in ['pais', 'pais_otro', 'ciudad', 'ciudad_otro', 'service_time', 'dynamic_tags']:
        if key in params:
            sanitized[key] = params[key]
    
    return sanitized

def validate_vehicle_groups(groups: list) -> list:
    """
    Validates vehicle groups data
    Returns sanitized groups or raises ValidationError
    """
    if not groups or not isinstance(groups, list):
        raise ValidationError("Debe proporcionar al menos un grupo de vehículos")
    
    sanitized = []
    for idx, group in enumerate(groups):
        if not isinstance(group, dict):
            raise ValidationError(f"Grupo {idx + 1}: formato inválido")
        
        try:
            count = int(group.get('count', 0))
            if count \u003c 1 or count \u003e 10000:
                raise ValidationError(f"Grupo {idx + 1}: cantidad debe estar entre 1 y 10,000")
        except (ValueError, TypeError):
            raise ValidationError(f"Grupo {idx + 1}: cantidad inválida")
        
        vehicle_type = group.get('type', '').strip()
        if not vehicle_type:
            raise ValidationError(f"Grupo {idx + 1}: tipo de vehículo es obligatorio")
        
        origin = group.get('origin', '').strip()
        if not origin:
            raise ValidationError(f"Grupo {idx + 1}: origen es obligatorio")
        
        try:
            cap1 = float(group.get('capacity1', 0))
            if cap1 \u003c 0:
                raise ValidationError(f"Grupo {idx + 1}: capacidad no puede ser negativa")
        except (ValueError, TypeError):
            raise ValidationError(f"Grupo {idx + 1}: capacidad inválida")
        
        sanitized.append({
            'count': count,
            'type': vehicle_type,
            'origin': origin,
            'capacity1': cap1,
            'capacity2': group.get('capacity2'),
            'start': group.get('start', '08:00'),
            'end': group.get('end', '18:00')
        })
    
    return sanitized
