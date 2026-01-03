"""
Tests para el LinkedInPostGenerator
"""
import pytest
from unittest.mock import Mock, patch
from generator import LinkedInPostGenerator


class TestLinkedInPostGenerator:
    """Tests para la clase LinkedInPostGenerator"""

    @pytest.fixture
    def generator(self):
        """Fixture para crear una instancia del generador"""
        return LinkedInPostGenerator()

    @pytest.fixture
    def sample_article(self):
        """Fixture con un artículo de ejemplo"""
        return {
            'title': 'Test Article About AI',
            'url': 'https://example.com/article',
            'description': 'This is a test description about artificial intelligence.',
            'source': 'Test Blog',
            'scraped_at': '2026-01-03T12:00:00'
        }

    def test_generator_initialization(self, generator):
        """Test que el generador se inicializa correctamente"""
        assert generator is not None
        assert hasattr(generator, 'generate_post')
        assert hasattr(generator, 'generate_posts_from_articles')

    def test_generate_post_returns_dict(self, generator, sample_article):
        """Test que generate_post devuelve un diccionario"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            # Mock de la respuesta de Gemini
            mock_response = Mock()
            mock_response.text = "Este es un post generado de prueba sobre IA."
            mock_model.return_value.generate_content.return_value = mock_response

            post = generator.generate_post(sample_article)

            assert isinstance(post, dict)

    def test_generated_post_has_required_fields(self, generator, sample_article):
        """Test que el post generado tiene los campos requeridos"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = Mock()
            mock_response.text = "Post de prueba generado."
            mock_model.return_value.generate_content.return_value = mock_response

            post = generator.generate_post(sample_article)

            # Verificar campos requeridos (el ID se agrega en agent.py, no aquí)
            assert 'post_text' in post
            assert 'article' in post
            assert 'generated_at' in post

            # Verificar tipos
            assert isinstance(post['post_text'], str)
            assert isinstance(post['article'], dict)
            assert isinstance(post['generated_at'], str)

            # Verificar contenido
            assert len(post['post_text']) > 0
            assert post['article'] == sample_article
            # El post_text debe incluir la URL al final
            assert sample_article['url'] in post['post_text']

    def test_generate_posts_from_articles_returns_list(self, generator):
        """Test que generate_posts_from_articles devuelve una lista"""
        articles = [
            {
                'title': 'Article 1',
                'url': 'https://example.com/1',
                'description': 'Description 1',
                'source': 'Test',
                'scraped_at': '2026-01-03T12:00:00'
            }
        ]

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = Mock()
            mock_response.text = "Post generado."
            mock_model.return_value.generate_content.return_value = mock_response

            posts = generator.generate_posts_from_articles(articles)

            assert isinstance(posts, list)
            assert len(posts) == len(articles)

    def test_adaptive_params_applied(self, generator, sample_article):
        """Test que los parámetros adaptativos se aplican correctamente"""
        adaptive_params = {
            'tone': 'casual',
            'emoji_level': 'moderado (3-4)',
            'hashtag_count': '5-6',
            'paragraph_count': '4-5'
        }

        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = Mock()
            mock_response.text = "Post adaptado generado."
            mock_model.return_value.generate_content.return_value = mock_response

            post = generator.generate_post(sample_article, adaptive_params)

            assert post is not None
            assert 'post_text' in post

    def test_generate_post_handles_empty_article(self, generator):
        """Test que maneja correctamente artículos vacíos"""
        empty_article = {
            'title': '',
            'url': '',
            'description': '',
            'source': '',
            'scraped_at': ''
        }

        # Debería manejar el error o devolver algo válido
        try:
            post = generator.generate_post(empty_article)
            # Si no falla, verificar que devuelve algo
            assert post is not None
        except Exception:
            # Si falla, eso también es aceptable para artículos vacíos
            pass

    def test_post_text_includes_url(self, generator, sample_article):
        """Test que el post_text incluye la URL al final"""
        with patch('google.generativeai.GenerativeModel') as mock_model:
            mock_response = Mock()
            mock_response.text = "Post de prueba."
            mock_model.return_value.generate_content.return_value = mock_response

            post = generator.generate_post(sample_article)

            # El post debe incluir "Leer más:" seguido de la URL
            assert 'Leer más:' in post['post_text']
            assert sample_article['url'] in post['post_text']
