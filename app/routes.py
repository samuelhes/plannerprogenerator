from flask import Blueprint, request, send_file, jsonify, current_app
from .services import GenerationService
import datetime

api_bp = Blueprint('api', __name__)
service = GenerationService()

@api_bp.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        current_app.logger.info(f"Generate Orders Request: {data}")
        
        # The service handles the heavy lifting
        file_stream, filename = service.generate_excel(data)
        
        return send_file(
            file_stream,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except ValueError as ve:
        current_app.logger.warning(f"Business Logic Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        current_app.logger.error(f"Server Error (Generate Orders): {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

@api_bp.route('/generate-vehicles', methods=['POST'])
def generate_vehicles():
    try:
        data = request.json
        current_app.logger.info(f"Generate Vehicles Request: {len(data.get('groups', []))} groups provided.")
        groups = data.get('groups', [])
        
        if not groups:
             return jsonify({'error': 'No vehicle groups provided'}), 400

        # Pass the whole data object if it contains tags, otherwise wrap it
        if 'groups' in data:
             payload = data
        else:
             # Backward compatibility if data is just list of groups ?? 
             # Actually request.json returns dict usually. 
             # If client sent just list? Unlikely with JSON. 
             # Let's assume data is the dict. 
             payload = data
        
        output, filename = service.generate_vehicles_excel(payload)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except ValueError as e:
        current_app.logger.warning(f"Business Logic Error (Vehicles): {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error generating vehicles: {e}", exc_info=True)
        return jsonify({'error': 'Internal Server Error'}), 500
