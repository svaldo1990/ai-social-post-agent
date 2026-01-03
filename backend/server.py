"""
API Flask para servir los posts generados
"""
import json
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import requests
from bs4 import BeautifulSoup
from scraper import ArticleScraper
from generator import LinkedInPostGenerator
from agent_brain import AutonomousAgent
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite requests desde el frontend React

DATA_DIR = Path(__file__).parent.parent / "data"
POSTS_FILE = DATA_DIR / "posts.json"

# Estado para tracking de generación
generation_status = {
    'is_generating': False,
    'progress': '',
    'error': None
}


def load_posts():
    """Carga los posts desde el archivo JSON"""
    if POSTS_FILE.exists():
        with open(POSTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Endpoint para obtener todos los posts"""
    posts = load_posts()
    return jsonify({
        'success': True,
        'count': len(posts),
        'posts': posts
    })


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Endpoint para obtener un post específico"""
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)

    if post:
        return jsonify({
            'success': True,
            'post': post
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Post not found'
        }), 404


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Endpoint para obtener estadísticas"""
    posts = load_posts()

    sources = {}
    for post in posts:
        source = post['article']['source']
        sources[source] = sources.get(source, 0) + 1

    return jsonify({
        'success': True,
        'stats': {
            'total_posts': len(posts),
            'sources': sources
        }
    })


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'API is running'
    })


def generate_posts_background():
    """Función que genera posts en background con capacidades autónomas"""
    global generation_status

    try:
        generation_status['is_generating'] = True
        generation_status['progress'] = '🧠 Evaluando con sistema autónomo...'
        generation_status['error'] = None

        # Inicializar agente autónomo
        brain = AutonomousAgent()

        # Evaluar si debe generar
        should_run, reason, performance = brain.evaluate_and_decide()

        if not should_run:
            generation_status['error'] = f'El agente decidió no generar: {reason}'
            generation_status['is_generating'] = False
            return

        generation_status['progress'] = 'Buscando artículos...'

        # Scrape artículos
        scraper = ArticleScraper()
        all_articles = scraper.get_ai_articles()

        if not all_articles:
            generation_status['error'] = 'No se encontraron artículos'
            generation_status['is_generating'] = False
            return

        generation_status['progress'] = f'🧠 Seleccionando mejores artículos de {len(all_articles)} candidatos...'

        # Selección inteligente
        articles = brain.process_articles(all_articles)

        generation_status['progress'] = f'Generando {len(articles)} posts con parámetros adaptativos...'

        # Generar posts con parámetros adaptativos
        generator = LinkedInPostGenerator()
        adaptive_params = brain.get_adaptive_params()
        new_posts = generator.generate_posts_from_articles(articles, adaptive_params)

        if not new_posts:
            generation_status['error'] = 'No se pudieron generar posts'
            generation_status['is_generating'] = False
            return

        # Guardar posts
        generation_status['progress'] = 'Guardando posts...'
        existing_posts = load_posts()

        # Agregar ID único
        for i, post in enumerate(new_posts):
            post['id'] = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"

        all_posts = new_posts + existing_posts

        DATA_DIR.mkdir(exist_ok=True)
        with open(POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)

        # Fase de aprendizaje
        generation_status['progress'] = '🧠 Aprendiendo de esta generación...'
        brain.learn_from_generation(articles, new_posts)

        generation_status['progress'] = f'✅ Completado: {len(new_posts)} posts generados (el agente aprendió)'
        generation_status['is_generating'] = False

    except Exception as e:
        generation_status['error'] = str(e)
        generation_status['is_generating'] = False


@app.route('/api/generate', methods=['POST'])
def generate_posts():
    """Endpoint para generar nuevos posts"""
    global generation_status

    if generation_status['is_generating']:
        return jsonify({
            'success': False,
            'error': 'Ya hay una generación en progreso',
            'status': generation_status
        }), 409

    # Iniciar generación en background
    thread = threading.Thread(target=generate_posts_background)
    thread.daemon = True
    thread.start()

    return jsonify({
        'success': True,
        'message': 'Generación iniciada',
        'status': generation_status
    })


@app.route('/api/generate/status', methods=['GET'])
def get_generation_status():
    """Endpoint para obtener el estado de la generación"""
    return jsonify({
        'success': True,
        'status': generation_status
    })


@app.route('/api/agent/status', methods=['GET'])
def get_agent_status():
    """Endpoint para obtener el estado del agente autónomo"""
    try:
        brain = AutonomousAgent()

        # Obtener información del estado del agente
        should_run, reason = brain.decision_engine.should_generate_now()
        performance = brain.learning_system.analyze_performance()
        adaptive_params = brain.get_adaptive_params()

        return jsonify({
            'success': True,
            'agent': {
                'memory': {
                    'total_generations': brain.memory.memory['total_generations'],
                    'articles_processed': len(brain.memory.memory['article_history']),
                    'topics_covered': len(brain.memory.memory['topics_covered']),
                    'topic_diversity': brain.memory.get_topic_diversity_score(),
                    'last_generation': brain.memory.memory.get('last_generation'),
                    'sources_used': brain.memory.memory['sources_used']
                },
                'decision': {
                    'should_generate_now': should_run,
                    'reason': reason
                },
                'performance': performance,
                'adaptive_params': adaptive_params
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/agent/memory', methods=['GET'])
def get_agent_memory():
    """Endpoint para ver la memoria completa del agente"""
    try:
        brain = AutonomousAgent()
        return jsonify({
            'success': True,
            'memory': brain.memory.memory
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/fetch-metadata', methods=['GET'])
def fetch_metadata():
    """Endpoint para obtener metadata de una URL"""
    url = request.args.get('url')

    if not url:
        return jsonify({
            'success': False,
            'error': 'URL es requerida'
        }), 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Intentar obtener título
        title = None
        if soup.find('meta', property='og:title'):
            title = soup.find('meta', property='og:title').get('content')
        elif soup.find('title'):
            title = soup.find('title').get_text(strip=True)

        # Intentar obtener descripción
        description = None
        if soup.find('meta', property='og:description'):
            description = soup.find('meta', property='og:description').get('content')
        elif soup.find('meta', attrs={'name': 'description'}):
            description = soup.find('meta', attrs={'name': 'description'}).get('content')

        return jsonify({
            'success': True,
            'metadata': {
                'title': title,
                'description': description
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al obtener metadata: {str(e)}'
        }), 500


@app.route('/api/custom-source', methods=['POST'])
def add_custom_source():
    """Endpoint para agregar una fuente personalizada y generar post"""
    data = request.json

    if not data or not data.get('url'):
        return jsonify({
            'success': False,
            'error': 'URL es requerida'
        }), 400

    try:
        url = data['url'].strip()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        # Si no se proporcionó título o descripción, intentar obtenerlos
        if not title or not description:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')

                if not title:
                    if soup.find('meta', property='og:title'):
                        title = soup.find('meta', property='og:title').get('content')
                    elif soup.find('title'):
                        title = soup.find('title').get_text(strip=True)

                if not description:
                    if soup.find('meta', property='og:description'):
                        description = soup.find('meta', property='og:description').get('content')
                    elif soup.find('meta', attrs={'name': 'description'}):
                        description = soup.find('meta', attrs={'name': 'description'}).get('content')

            except Exception as e:
                print(f"Error al obtener metadata: {e}")

        # Si aún no hay título, usar la URL
        if not title:
            title = url

        # Crear artículo
        article = {
            'title': title,
            'url': url,
            'description': description or 'Artículo personalizado',
            'source': 'Fuente Personalizada',
            'scraped_at': datetime.now().isoformat()
        }

        # Generar post inmediatamente
        generator = LinkedInPostGenerator()

        # Usar agente autónomo para parámetros adaptativos
        brain = AutonomousAgent()
        adaptive_params = brain.get_adaptive_params()

        post = generator.generate_post(article, adaptive_params)

        if not post:
            return jsonify({
                'success': False,
                'error': 'No se pudo generar el post'
            }), 500

        # Guardar post
        existing_posts = load_posts()
        post['id'] = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_custom"
        all_posts = [post] + existing_posts

        DATA_DIR.mkdir(exist_ok=True)
        with open(POSTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_posts, f, indent=2, ensure_ascii=False)

        # Aprender de esta generación
        brain.learn_from_generation([article], [post])

        return jsonify({
            'success': True,
            'article': article,
            'post': post,
            'message': 'Post generado exitosamente desde fuente personalizada'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al procesar fuente: {str(e)}'
        }), 500


if __name__ == '__main__':
    print("🚀 Starting API server...")
    print(f"📁 Posts file: {POSTS_FILE}")
    print("🌐 API running at: http://localhost:5001")
    print("\nEndpoints:")
    print("  GET  /api/posts          - Lista todos los posts")
    print("  GET  /api/posts/<id>     - Obtiene un post específico")
    print("  GET  /api/stats          - Estadísticas")
    print("  GET  /api/health         - Health check")
    print("  POST /api/generate       - Genera nuevos posts (con agente autónomo)")
    print("  GET  /api/generate/status - Estado de generación")
    print("  🧠 GET  /api/agent/status  - Estado del agente autónomo")
    print("  🧠 GET  /api/agent/memory  - Memoria del agente")
    print("  📎 GET  /api/fetch-metadata - Obtener metadata de URL")
    print("  📎 POST /api/custom-source  - Agregar fuente personalizada")
    print("\n")

    app.run(debug=True, port=5001)
