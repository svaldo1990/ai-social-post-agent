"""
Generador de posts de LinkedIn usando Google Gemini
"""
import os
from google import genai
from google.genai import types
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class LinkedInPostGenerator:
    """Genera posts de LinkedIn a partir de artículos de AI"""

    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

        self.client = genai.Client(api_key=api_key)

    def generate_post(self, article: Dict, adaptive_params: Dict = None) -> Dict:
        """Genera un post de LinkedIn basado en un artículo"""

        # Parámetros por defecto
        params = {
            'tone': 'profesional pero accesible',
            'emoji_level': 'sutil (1-2 máximo)',
            'hashtag_count': '3-4',
            'paragraph_count': '2-3'
        }

        # Sobrescribir con parámetros adaptativos si se proveen
        if adaptive_params:
            params.update(adaptive_params)

        prompt = f"""Eres un experto en crear contenido viral para LinkedIn sobre Inteligencia Artificial.

Basándote en el siguiente artículo, crea un post atractivo para LinkedIn:

Título: {article['title']}
Fuente: {article['source']}
Descripción: {article['description']}
URL: {article['url']}

Requisitos del post:
- Debe ser {params['tone']}
- Incluye {params['paragraph_count']} párrafos cortos
- Destaca el valor o impacto de la noticia
- Usa un tono entusiasta pero informado
- Termina con una pregunta para generar engagement
- NO uses hashtags excesivos (máximo {params['hashtag_count']} relevantes)
- Incluye emojis {params['emoji_level']} solo si son apropiados
- NO incluyas el link en el texto, ya se agregará después

Genera SOLO el texto del post, sin introducción ni comentarios adicionales."""

        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )

            post_text = response.text.strip()

            # Agregar el link al final
            full_post = f"{post_text}\n\nLeer más: {article['url']}"

            return {
                'article': article,
                'post_text': full_post,
                'generated_at': article['scraped_at']
            }

        except Exception as e:
            print(f"Error generando post para '{article['title']}': {e}")
            return None

    def generate_posts_from_articles(self, articles: List[Dict], adaptive_params: Dict = None) -> List[Dict]:
        """Genera posts para todos los artículos"""
        posts = []

        for i, article in enumerate(articles, 1):
            print(f"Generando post {i}/{len(articles)}: {article['title'][:50]}...")
            post = self.generate_post(article, adaptive_params)
            if post:
                posts.append(post)

        print(f"\nGenerados {len(posts)} posts exitosamente")
        return posts


if __name__ == "__main__":
    # Test
    generator = LinkedInPostGenerator()
    test_article = {
        'title': 'GPT-4 Turbo Preview',
        'source': 'OpenAI Blog',
        'description': 'Announcing GPT-4 Turbo, our most capable model with improved performance.',
        'url': 'https://openai.com/blog/gpt-4-turbo',
        'scraped_at': '2024-01-01T00:00:00'
    }

    post = generator.generate_post(test_article)
    if post:
        print("\n" + "="*50)
        print("POST GENERADO:")
        print("="*50)
        print(post['post_text'])
