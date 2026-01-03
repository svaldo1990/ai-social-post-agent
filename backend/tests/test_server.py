"""
Tests para los API endpoints del servidor Flask
"""
import pytest
import json
import os
import sys

# Agregar el directorio backend al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app


class TestServerEndpoints:
    """Tests para los endpoints de la API"""

    @pytest.fixture
    def client(self):
        """Fixture para crear un cliente de prueba"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_health_endpoint(self, client):
        """Test del endpoint /api/health"""
        response = client.get('/api/health')

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_get_posts_endpoint(self, client):
        """Test del endpoint GET /api/posts"""
        response = client.get('/api/posts')

        assert response.status_code == 200
        data = json.loads(response.data)

        # Verificar estructura de respuesta
        assert 'success' in data
        assert 'posts' in data
        assert isinstance(data['posts'], list)

    def test_get_stats_endpoint(self, client):
        """Test del endpoint GET /api/stats"""
        response = client.get('/api/stats')

        assert response.status_code == 200
        data = json.loads(response.data)

        # Verificar estructura de respuesta
        assert 'success' in data
        assert 'stats' in data
        assert 'total_posts' in data['stats']
        assert 'sources' in data['stats']
        assert isinstance(data['stats']['total_posts'], int)
        assert isinstance(data['stats']['sources'], dict)

    def test_get_specific_post(self, client):
        """Test del endpoint GET /api/posts/<id>"""
        # Primero obtener todos los posts
        response = client.get('/api/posts')
        data = json.loads(response.data)

        if len(data['posts']) > 0:
            # Intentar obtener el primer post
            post_id = data['posts'][0]['id']
            response = client.get(f'/api/posts/{post_id}')

            assert response.status_code == 200
            post_data = json.loads(response.data)
            assert post_data['success'] == True
            assert 'post' in post_data
            assert post_data['post']['id'] == post_id

    def test_get_nonexistent_post_returns_404(self, client):
        """Test que obtener un post inexistente devuelve 404"""
        response = client.get('/api/posts/post_nonexistent_12345')

        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] == False

    def test_fetch_metadata_endpoint_requires_url(self, client):
        """Test que /api/fetch-metadata requiere un parámetro URL"""
        response = client.get('/api/fetch-metadata')

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False

    def test_fetch_metadata_with_valid_url(self, client):
        """Test fetch-metadata con una URL válida"""
        test_url = 'https://example.com'
        response = client.get(f'/api/fetch-metadata?url={test_url}')

        # Puede fallar si el scraping no funciona, pero debe devolver una respuesta válida
        assert response.status_code in [200, 500]
        data = json.loads(response.data)
        assert 'success' in data

    def test_custom_source_endpoint_requires_post(self, client):
        """Test que /api/custom-source solo acepta POST"""
        response = client.get('/api/custom-source')

        assert response.status_code == 405  # Method Not Allowed

    def test_custom_source_requires_url(self, client):
        """Test que /api/custom-source requiere URL en el body"""
        response = client.post(
            '/api/custom-source',
            data=json.dumps({}),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] == False

    def test_generate_status_endpoint(self, client):
        """Test del endpoint /api/generate/status"""
        response = client.get('/api/generate/status')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert 'success' in data
        assert 'status' in data
        assert 'is_generating' in data['status']
        assert 'progress' in data['status']

    def test_agent_status_endpoint(self, client):
        """Test del endpoint /api/agent/status"""
        response = client.get('/api/agent/status')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert 'success' in data
        assert 'agent' in data

    def test_agent_memory_endpoint(self, client):
        """Test del endpoint /api/agent/memory"""
        response = client.get('/api/agent/memory')

        assert response.status_code == 200
        data = json.loads(response.data)

        assert 'success' in data
        assert 'memory' in data

    def test_cors_headers_present(self, client):
        """Test que los headers CORS están presentes"""
        response = client.get('/api/health')

        # Flask-CORS debería agregar estos headers
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_json_content_type(self, client):
        """Test que las respuestas son JSON"""
        response = client.get('/api/posts')

        assert 'application/json' in response.content_type
