from flask import Blueprint, request, send_file, jsonify
from .services import GenerationService
import datetime

api_bp = Blueprint('api', __name__)
service = GenerationService()

@api_bp.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        print(f"[{datetime.datetime.now()}] Generate Request: {data}")
        
        # The service handles the heavy lifting
        file_stream, filename = service.generate_excel(data)
        
        return send_file(
            file_stream,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
