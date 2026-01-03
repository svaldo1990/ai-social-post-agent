"""
Sistema cerebral del agente autónomo - Memoria, decisiones y aprendizaje
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import re


class AgentMemory:
    """Sistema de memoria para el agente - recuerda posts anteriores y patrones"""

    def __init__(self, data_dir: str = "../data"):
        self.data_dir = Path(data_dir)
        self.memory_file = self.data_dir / "agent_memory.json"
        self.posts_file = self.data_dir / "posts.json"
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict:
        """Carga la memoria del agente"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'topics_covered': {},  # tema -> count
            'sources_used': {},    # source -> count
            'successful_patterns': [],  # patrones que funcionan bien
            'last_generation': None,
            'total_generations': 0,
            'article_history': []  # URLs de artículos ya procesados
        }

    def save_memory(self):
        """Guarda la memoria del agente"""
        self.data_dir.mkdir(exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    def remember_generation(self, articles: List[Dict], posts: List[Dict]):
        """Registra una generación en la memoria"""
        self.memory['total_generations'] += 1
        self.memory['last_generation'] = datetime.now().isoformat()

        # Registrar artículos procesados
        for article in articles:
            self.memory['article_history'].append({
                'url': article['url'],
                'title': article['title'],
                'source': article['source'],
                'processed_at': datetime.now().isoformat()
            })

            # Actualizar conteo de fuentes
            source = article['source']
            self.memory['sources_used'][source] = self.memory['sources_used'].get(source, 0) + 1

        # Extraer y recordar tópicos de los posts
        for post in posts:
            topics = self._extract_topics(post['post_text'])
            for topic in topics:
                self.memory['topics_covered'][topic] = self.memory['topics_covered'].get(topic, 0) + 1

        self.save_memory()

    def _extract_topics(self, text: str) -> List[str]:
        """Extrae tópicos clave del texto usando hashtags y palabras clave"""
        topics = []

        # Extraer hashtags
        hashtags = re.findall(r'#(\w+)', text.lower())
        topics.extend(hashtags)

        # Palabras clave comunes de IA
        keywords = ['gpt', 'gemini', 'claude', 'llm', 'vision', 'multimodal',
                   'ai', 'ia', 'machine learning', 'neural', 'transformer',
                   'chatbot', 'agent', 'automation']

        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                topics.append(keyword)

        return list(set(topics))

    def was_article_processed(self, article_url: str) -> bool:
        """Verifica si un artículo ya fue procesado anteriormente"""
        return any(a['url'] == article_url for a in self.memory['article_history'])

    def get_topic_diversity_score(self) -> float:
        """Calcula qué tan diversos son los tópicos cubiertos (0-1)"""
        if not self.memory['topics_covered']:
            return 1.0

        counts = list(self.memory['topics_covered'].values())
        max_count = max(counts)
        min_count = min(counts)

        if max_count == min_count:
            return 1.0

        # Menor diferencia = mayor diversidad
        return 1.0 - (max_count - min_count) / max_count


class DecisionEngine:
    """Motor de decisiones del agente - decide qué artículos usar y cuándo generar"""

    def __init__(self, memory: AgentMemory):
        self.memory = memory

    def should_generate_now(self) -> Tuple[bool, str]:
        """Decide si es momento de generar nuevos posts"""
        last_gen = self.memory.memory.get('last_generation')

        # Primera vez - siempre generar
        if not last_gen:
            return True, "Primera ejecución del agente"

        # Calcular tiempo desde última generación
        last_time = datetime.fromisoformat(last_gen)
        hours_passed = (datetime.now() - last_time).total_seconds() / 3600

        # Regla: generar si han pasado más de 24 horas
        if hours_passed >= 24:
            return True, f"Han pasado {hours_passed:.1f} horas desde la última generación"

        # Regla: no generar si es muy reciente
        if hours_passed < 4:
            return False, f"Demasiado reciente ({hours_passed:.1f} horas). Esperar al menos 4 horas"

        # Decisión basada en diversidad de contenido
        diversity = self.memory.get_topic_diversity_score()
        if diversity < 0.5:
            return True, f"Baja diversidad de tópicos ({diversity:.2f}). Necesario nuevo contenido"

        return False, f"Condiciones normales. Próxima generación en {24 - hours_passed:.1f} horas"

    def score_article(self, article: Dict) -> Tuple[float, List[str]]:
        """
        Calcula un score de relevancia para un artículo (0-100)
        Retorna (score, razones)
        """
        score = 0.0
        reasons = []

        # 1. Novedad - artículos nuevos son mejores
        if not self.memory.was_article_processed(article['url']):
            score += 40
            reasons.append("✓ Artículo nuevo (nunca procesado)")
        else:
            score += 5
            reasons.append("⚠ Artículo ya procesado anteriormente")

        # 2. Balance de fuentes - preferir fuentes menos usadas
        source = article['source']
        source_count = self.memory.memory['sources_used'].get(source, 0)
        total_sources = sum(self.memory.memory['sources_used'].values())

        if total_sources > 0:
            source_ratio = source_count / total_sources
            if source_ratio < 0.3:
                score += 30
                reasons.append(f"✓ Fuente poco usada ({source_count} veces, {source_ratio*100:.0f}%)")
            elif source_ratio < 0.5:
                score += 15
                reasons.append(f"~ Fuente moderadamente usada ({source_count} veces)")
            else:
                score += 5
                reasons.append(f"⚠ Fuente muy usada ({source_count} veces, {source_ratio*100:.0f}%)")
        else:
            score += 30
            reasons.append("✓ Primera vez usando esta fuente")

        # 3. Calidad del contenido - descripción y título
        if article.get('description') and len(article['description']) > 100:
            score += 15
            reasons.append("✓ Descripción detallada disponible")
        elif article.get('description'):
            score += 8
            reasons.append("~ Descripción corta")

        if len(article.get('title', '')) > 30:
            score += 15
            reasons.append("✓ Título descriptivo")

        return score, reasons

    def select_best_articles(self, articles: List[Dict], max_articles: int = 3) -> List[Dict]:
        """Selecciona los mejores artículos basado en scoring"""
        scored_articles = []

        print("\n🧠 MOTOR DE DECISIONES - Evaluando artículos...")
        print("=" * 70)

        for article in articles:
            score, reasons = self.score_article(article)
            scored_articles.append((score, article, reasons))

            print(f"\n📄 {article['title'][:60]}...")
            print(f"   Fuente: {article['source']}")
            print(f"   Score: {score:.1f}/100")
            for reason in reasons:
                print(f"   {reason}")

        # Ordenar por score descendente
        scored_articles.sort(reverse=True, key=lambda x: x[0])

        # Seleccionar los mejores
        selected = [item[1] for item in scored_articles[:max_articles]]

        print("\n" + "=" * 70)
        print(f"✅ Seleccionados {len(selected)} artículos de {len(articles)} candidatos")
        print("=" * 70)

        return selected


class LearningSystem:
    """Sistema de aprendizaje - adapta el comportamiento basado en resultados"""

    def __init__(self, memory: AgentMemory):
        self.memory = memory

    def analyze_performance(self) -> Dict:
        """Analiza el desempeño histórico del agente"""
        analysis = {
            'total_posts_generated': 0,
            'sources_balance': {},
            'topic_coverage': {},
            'recommendations': []
        }

        # Cargar todos los posts
        posts_file = self.memory.posts_file
        if posts_file.exists():
            with open(posts_file, 'r', encoding='utf-8') as f:
                posts = json.load(f)
                analysis['total_posts_generated'] = len(posts)

                # Analizar balance de fuentes
                sources = [p['article']['source'] for p in posts]
                source_counts = Counter(sources)
                analysis['sources_balance'] = dict(source_counts)

        # Copiar tópicos de memoria
        analysis['topic_coverage'] = self.memory.memory['topics_covered'].copy()

        # Generar recomendaciones
        if analysis['sources_balance']:
            max_source = max(analysis['sources_balance'].values())
            min_source = min(analysis['sources_balance'].values())

            if max_source > min_source * 3:
                analysis['recommendations'].append(
                    f"⚠️ Desbalance en fuentes: algunas fuentes tienen 3x más posts que otras"
                )

        if len(analysis['topic_coverage']) < 5:
            analysis['recommendations'].append(
                "💡 Poca diversidad de tópicos. Considerar buscar fuentes más variadas"
            )

        diversity = self.memory.get_topic_diversity_score()
        if diversity < 0.5:
            analysis['recommendations'].append(
                f"⚠️ Diversidad de tópicos baja ({diversity:.2%}). Buscar temas nuevos"
            )

        return analysis

    def get_adaptive_prompt_params(self) -> Dict:
        """Genera parámetros adaptativos para el prompt basado en aprendizaje"""
        params = {
            'tone': 'profesional pero accesible',
            'emoji_level': 'sutil (1-2 máximo)',
            'hashtag_count': '3-4',
            'paragraph_count': '2-3'
        }

        # Analizar patrones de tópicos más usados
        topics = self.memory.memory['topics_covered']
        if topics:
            top_topics = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:3]

            # Si hay mucho enfoque en tópicos técnicos, ajustar tono
            technical_topics = ['llm', 'transformer', 'neural', 'machine learning']
            tech_count = sum(count for topic, count in top_topics if topic in technical_topics)

            if tech_count > len(top_topics) * 0.6:
                params['tone'] = 'más técnico y detallado'

        # Diversificar formato basado en generaciones anteriores
        gen_count = self.memory.memory['total_generations']
        if gen_count % 3 == 0:
            params['paragraph_count'] = '1 párrafo impactante'
        elif gen_count % 3 == 1:
            params['paragraph_count'] = '4-5 párrafos detallados'

        return params


class AutonomousAgent:
    """Agente autónomo con capacidades de memoria, decisión y aprendizaje"""

    def __init__(self, data_dir: str = "../data"):
        self.memory = AgentMemory(data_dir)
        self.decision_engine = DecisionEngine(self.memory)
        self.learning_system = LearningSystem(self.memory)

    def evaluate_and_decide(self) -> Tuple[bool, str, Dict]:
        """Evalúa la situación y decide si proceder"""
        should_run, reason = self.decision_engine.should_generate_now()

        # Análisis de desempeño
        performance = self.learning_system.analyze_performance()

        return should_run, reason, performance

    def process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Procesa artículos con decisión inteligente"""
        return self.decision_engine.select_best_articles(articles)

    def learn_from_generation(self, articles: List[Dict], posts: List[Dict]):
        """Aprende de una generación completada"""
        self.memory.remember_generation(articles, posts)

    def get_adaptive_params(self) -> Dict:
        """Obtiene parámetros adaptativos para la generación"""
        return self.learning_system.get_adaptive_prompt_params()

    def print_status_report(self):
        """Imprime un reporte del estado del agente"""
        print("\n" + "="*70)
        print("🤖 REPORTE DE ESTADO DEL AGENTE AUTÓNOMO")
        print("="*70)

        # Estadísticas de memoria
        print(f"\n📊 Memoria:")
        print(f"   • Generaciones totales: {self.memory.memory['total_generations']}")
        print(f"   • Artículos procesados: {len(self.memory.memory['article_history'])}")
        print(f"   • Tópicos cubiertos: {len(self.memory.memory['topics_covered'])}")
        print(f"   • Diversidad de tópicos: {self.memory.get_topic_diversity_score():.2%}")

        if self.memory.memory['last_generation']:
            last = datetime.fromisoformat(self.memory.memory['last_generation'])
            print(f"   • Última generación: {last.strftime('%Y-%m-%d %H:%M:%S')}")

        # Análisis de desempeño
        performance = self.learning_system.analyze_performance()

        print(f"\n📈 Desempeño:")
        print(f"   • Posts generados total: {performance['total_posts_generated']}")

        if performance['sources_balance']:
            print(f"   • Balance de fuentes:")
            for source, count in performance['sources_balance'].items():
                print(f"     - {source}: {count} posts")

        # Recomendaciones
        if performance['recommendations']:
            print(f"\n💡 Recomendaciones:")
            for rec in performance['recommendations']:
                print(f"   {rec}")

        # Decisión actual
        should_run, reason = self.decision_engine.should_generate_now()
        print(f"\n🎯 Decisión autónoma:")
        print(f"   • Generar ahora: {'✅ SÍ' if should_run else '❌ NO'}")
        print(f"   • Razón: {reason}")

        # Parámetros adaptativos
        params = self.get_adaptive_params()
        print(f"\n⚙️  Parámetros adaptativos actuales:")
        for key, value in params.items():
            print(f"   • {key}: {value}")

        print("\n" + "="*70)


if __name__ == "__main__":
    # Test del sistema autónomo
    agent = AutonomousAgent()
    agent.print_status_report()
