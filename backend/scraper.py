"""
Web scraper para artículos de AI de diferentes sitios
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime
import xml.etree.ElementTree as ET


class ArticleScraper:
    """Scraper para artículos de AI"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def scrape_openai_blog(self) -> List[Dict]:
        """Scrape artículos del blog de OpenAI usando RSS"""
        articles = []
        try:
            # Intentar con RSS feed primero (más confiable)
            url = "https://openai.com/blog/rss/"
            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code == 200:
                root = ET.fromstring(response.content)
                items = root.findall('.//item')[:5]  # Primeros 5

                for item in items:
                    title = item.find('title').text if item.find('title') is not None else ""
                    link = item.find('link').text if item.find('link') is not None else ""
                    description = item.find('description').text if item.find('description') is not None else ""

                    if title and link:
                        # Limpiar HTML de la descripción
                        if description:
                            soup = BeautifulSoup(description, 'html.parser')
                            description = soup.get_text(strip=True)[:300]

                        articles.append({
                            'title': title,
                            'url': link,
                            'description': description,
                            'source': 'OpenAI Blog',
                            'scraped_at': datetime.now().isoformat()
                        })
                return articles

        except Exception as e:
            print(f"Error scraping OpenAI RSS: {e}")

        # Si RSS falla, intentar scraping directo
        try:
            url = "https://openai.com/news/"
            response = requests.get(url, headers=self.headers, timeout=15)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Buscar enlaces con "news" o "research" en la URL
                links = soup.find_all('a', href=True)
                for link in links[:10]:
                    href = link.get('href', '')
                    if '/index/' in href or '/research/' in href:
                        title = link.get_text(strip=True)
                        if len(title) > 10:  # Filtrar títulos muy cortos
                            full_url = f"https://openai.com{href}" if not href.startswith('http') else href
                            articles.append({
                                'title': title,
                                'url': full_url,
                                'description': '',
                                'source': 'OpenAI Blog',
                                'scraped_at': datetime.now().isoformat()
                            })
                            if len(articles) >= 3:
                                break
        except Exception as e:
            print(f"Error scraping OpenAI blog: {e}")

        return articles

    def scrape_google_ai_blog(self) -> List[Dict]:
        """Scrape artículos del blog de Google AI"""
        articles = []
        try:
            url = "https://blog.google/technology/ai/"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Google AI Blog usa diferentes selectores
            article_elements = soup.find_all('article', limit=5)

            for element in article_elements:
                title_elem = element.find(['h2', 'h3'])
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                link_elem = element.find('a', href=True)
                link = link_elem['href'] if link_elem else ""

                if not link.startswith('http'):
                    link = f"https://blog.google{link}"

                desc_elem = element.find('p')
                description = desc_elem.get_text(strip=True)[:300] if desc_elem else ""

                if title and link:
                    articles.append({
                        'title': title,
                        'url': link,
                        'description': description,
                        'source': 'Google AI Blog',
                        'scraped_at': datetime.now().isoformat()
                    })

        except Exception as e:
            print(f"Error scraping Google AI blog: {e}")

        return articles

    def get_fallback_articles(self) -> List[Dict]:
        """Artículos de ejemplo en caso de que el scraping falle"""
        return [
            {
                'title': 'GPT-4 Turbo with Vision',
                'url': 'https://openai.com/index/gpt-4-turbo',
                'description': 'GPT-4 Turbo with vision is now available in the API. This model can process images and return textual responses, unlocking new use cases.',
                'source': 'OpenAI Blog',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Gemini 2.0: Our new AI model for the agentic era',
                'url': 'https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/',
                'description': 'Introducing Gemini 2.0, our most capable model yet, built for the agentic era. It delivers breakthrough performance and new capabilities.',
                'source': 'Google AI Blog',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': 'Claude 3.5 Sonnet',
                'url': 'https://www.anthropic.com/news/claude-3-5-sonnet',
                'description': 'Claude 3.5 Sonnet raises the industry bar for intelligence, outperforming competitor models and Claude 3 Opus on a wide range of evaluations.',
                'source': 'Anthropic News',
                'scraped_at': datetime.now().isoformat()
            }
        ]

    def get_ai_articles(self) -> List[Dict]:
        """Obtiene artículos de todas las fuentes"""
        all_articles = []

        print("Scraping OpenAI blog...")
        openai_articles = self.scrape_openai_blog()
        all_articles.extend(openai_articles)

        print("Scraping Google AI blog...")
        google_articles = self.scrape_google_ai_blog()
        all_articles.extend(google_articles)

        # Si no se encontraron suficientes artículos, complementar con fallback
        if len(all_articles) < 3:
            print("⚠️  Pocos artículos encontrados en vivo.")
            print("Complementando con artículos de ejemplo...")
            fallback = self.get_fallback_articles()
            # Agregar artículos de fallback que no estén duplicados
            for article in fallback:
                if not any(a['title'] == article['title'] for a in all_articles):
                    all_articles.append(article)
                    if len(all_articles) >= 3:
                        break

        print(f"Total articles found: {len(all_articles)}")
        return all_articles


if __name__ == "__main__":
    scraper = ArticleScraper()
    articles = scraper.get_ai_articles()
    for article in articles:
        print(f"\n{article['title']}")
        print(f"Source: {article['source']}")
        print(f"URL: {article['url']}")
