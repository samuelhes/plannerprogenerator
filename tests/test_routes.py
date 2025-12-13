"""
Integration tests for API routes
"""
import pytest
import json
from app import create_app


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestGenerateEndpoint:
    """Tests for /api/generate endpoint"""
    
    def test_generate_success(self, client):
        """Test successful order generation"""
        payload = {
            'cantidad_ordenes': 5,
            'ct_origen': 'CD Test',
            'fecha_entrega': '2025-01-15',
            'capacidad_min': 1.0,
            'capacidad_max': 5.0,
            'ventana_inicio': '09:00',
            'ventana_fin': '17:00',
            'pais': 'Chile',
            'ciudad': 'Santiago'
        }
        
        response = client.post(
            '/api/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        assert len(response.data) > 0
    
    def test_generate_missing_ct_origen(self, client):
        """Test error when CT Origen missing"""
        payload = {
            'cantidad_ordenes': 5,
            'ct_origen': '',  # Empty
            'fecha_entrega': '2025-01-15',
            'capacidad_min': 1.0,
            'capacidad_max': 5.0,
            'ventana_inicio': '09:00',
            'ventana_fin': '17:00'
        }
        
        response = client.post(
            '/api/generate',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_generate_invalid_json(self, client):
        """Test error with invalid JSON"""
        response = client.post(
            '/api/generate',
            data='invalid json',
            content_type='application/json'
        )
        
        assert response.status_code in [400, 500]


class TestGenerateVehiclesEndpoint:
    """Tests for /api/generate-vehicles endpoint"""
    
    def test_generate_vehicles_success(self, client):
        """Test successful vehicle generation"""
        payload = {
            'groups': [
                {
                    'count': 3,
                    'type': 'Camion',
                    'origin': 'CD Central',
                    'capacity1': 1000,
                    'capacity2': None,
                    'start_time': '08:00',
                    'end_time': '18:00'
                }
            ]
        }
        
        response = client.post(
            '/api/generate-vehicles',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    def test_generate_vehicles_empty_groups(self, client):
        """Test error with empty groups"""
        payload = {'groups': []}
        
        response = client.post(
            '/api/generate-vehicles',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestHealthEndpoints:
    """Tests for health check endpoints"""
    
    def test_healthz(self, client):
        """Test /healthz endpoint"""
        response = client.get('/healthz')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_readyz(self, client):
        """Test /readyz endpoint"""
        response = client.get('/readyz')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'ready'


class TestStaticFiles:
    """Tests for static file serving"""
    
    def test_index_page(self, client):
        """Test that index.html loads"""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'Planner Pro' in response.data or b'html' in response.data
