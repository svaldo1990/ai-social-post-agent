"""
Tests para el ArticleScraper
"""
import pytest
from scraper import ArticleScraper


class TestArticleScraper:
    """Tests para la clase ArticleScraper"""

    @pytest.fixture
    def scraper(self):
        """Fixture para crear una instancia del scraper"""
        return ArticleScraper()

    def test_scraper_initialization(self, scraper):
        """Test que el scraper se inicializa correctamente"""
        assert scraper is not None
        assert hasattr(scraper, 'get_ai_articles')

    def test_get_ai_articles_returns_list(self, scraper):
        """Test que get_ai_articles devuelve una lista"""
        articles = scraper.get_ai_articles()
        assert isinstance(articles, list)

    def test_get_ai_articles_returns_valid_articles(self, scraper):
        """Test que los artículos tienen los campos requeridos"""
        articles = scraper.get_ai_articles()

        if len(articles) > 0:
            article = articles[0]

            # Verificar que tiene los campos requeridos
            assert 'title' in article
            assert 'url' in article
            assert 'description' in article
            assert 'source' in article
            assert 'scraped_at' in article

            # Verificar tipos de datos
            assert isinstance(article['title'], str)
            assert isinstance(article['url'], str)
            assert isinstance(article['description'], str)
            assert isinstance(article['source'], str)
            assert isinstance(article['scraped_at'], str)

            # Verificar que no están vacíos
            assert len(article['title']) > 0
            assert len(article['url']) > 0
            assert article['url'].startswith('http')

    def test_scrape_openai_blog_returns_list(self, scraper):
        """Test que scrape_openai_blog devuelve una lista"""
        articles = scraper.scrape_openai_blog()
        assert isinstance(articles, list)

    def test_scrape_google_ai_blog_returns_list(self, scraper):
        """Test que scrape_google_ai_blog devuelve una lista"""
        articles = scraper.scrape_google_ai_blog()
        assert isinstance(articles, list)

    def test_articles_have_unique_urls(self, scraper):
        """Test que no hay URLs duplicadas"""
        articles = scraper.get_ai_articles()

        urls = [article['url'] for article in articles]
        unique_urls = set(urls)

        assert len(urls) == len(unique_urls), "Hay URLs duplicadas"

    def test_fallback_articles_when_scraping_fails(self, scraper):
        """Test que devuelve artículos de fallback si scraping falla"""
        # Incluso si el scraping falla, debe devolver al menos los artículos de fallback
        articles = scraper.get_ai_articles()
        assert len(articles) > 0, "Debe devolver al menos artículos de fallback"

    def test_get_fallback_articles_returns_list(self, scraper):
        """Test que get_fallback_articles devuelve una lista"""
        fallback = scraper.get_fallback_articles()
        assert isinstance(fallback, list)
        assert len(fallback) > 0, "Debe tener al menos un artículo de fallback"
