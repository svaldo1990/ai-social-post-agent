"""
Agente principal que coordina el scraping y generación de posts
AHORA CON CAPACIDADES AUTÓNOMAS: Memoria, Decisiones y Aprendizaje
"""
import json
import os
from datetime import datetime
from pathlib import Path
from scraper import ArticleScraper
from generator import LinkedInPostGenerator
from agent_brain import AutonomousAgent


class SocialPostAgent:
    """Agente que busca artículos de AI y genera posts de LinkedIn"""

    def __init__(self, data_dir: str = "../data", autonomous: bool = True):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.posts_file = self.data_dir / "posts.json"
        self.scraper = ArticleScraper()
        self.generator = LinkedInPostGenerator()

        # Sistema autónomo
        self.autonomous = autonomous
        if autonomous:
            self.brain = AutonomousAgent(data_dir)

    def load_existing_posts(self) -> list:
        """Carga posts existentes desde el archivo JSON"""
        if self.posts_file.exists():
            with open(self.posts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_posts(self, posts: list):
        """Guarda posts en el archivo JSON"""
        with open(self.posts_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

    def run(self):
        """Ejecuta el agente completo"""
        print("="*60)
        print("🤖 AI Social Post Agent")
        if self.autonomous:
            print("🧠 MODO AUTÓNOMO ACTIVADO")
        print("="*60)

        # FASE 0: Evaluación autónoma (si está habilitado)
        if self.autonomous:
            self.brain.print_status_report()

            should_run, reason, performance = self.brain.evaluate_and_decide()

            if not should_run:
                print(f"\n🛑 El agente decide NO generar en este momento:")
                print(f"   Razón: {reason}")
                print("\n💡 El agente está optimizando el uso de recursos y diversidad de contenido.")
                return

            print(f"\n✅ El agente decide generar nuevos posts:")
            print(f"   Razón: {reason}")
            input("\n⏸  Presiona Enter para continuar con la generación...")

        # 1. Scrape artículos
        print("\n📰 Paso 1: Buscando artículos de AI...")
        all_articles = self.scraper.get_ai_articles()

        if not all_articles:
            print("❌ No se encontraron artículos. Terminando.")
            return

        print(f"✅ Encontrados {len(all_articles)} artículos candidatos")

        # 1.5: Selección inteligente de artículos (si modo autónomo)
        if self.autonomous:
            articles = self.brain.process_articles(all_articles)
        else:
            articles = all_articles

        # 2. Generar posts
        print("\n✍️  Paso 2: Generando posts con Gemini...")
        if self.autonomous:
            # Obtener parámetros adaptativos
            adaptive_params = self.brain.get_adaptive_params()
            print(f"   🎛  Usando parámetros adaptativos: {adaptive_params}")
            new_posts = self.generator.generate_posts_from_articles(articles, adaptive_params)
        else:
            new_posts = self.generator.generate_posts_from_articles(articles)

        if not new_posts:
            print("❌ No se generaron posts. Terminando.")
            return

        # 3. Guardar posts
        print("\n💾 Paso 3: Guardando posts...")
        existing_posts = self.load_existing_posts()

        # Agregar ID único a cada post
        for i, post in enumerate(new_posts):
            post['id'] = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"

        # Combinar con posts existentes (nuevos primero)
        all_posts = new_posts + existing_posts
        self.save_posts(all_posts)

        print(f"✅ Guardados {len(new_posts)} posts nuevos")
        print(f"📊 Total de posts en la base de datos: {len(all_posts)}")

        # 3.5: Aprendizaje (si modo autónomo)
        if self.autonomous:
            print("\n🧠 Fase de aprendizaje...")
            self.brain.learn_from_generation(articles, new_posts)
            print("✅ Memoria actualizada y patrones aprendidos")

        # 4. Mostrar resumen
        print("\n" + "="*60)
        print("📋 RESUMEN DE POSTS GENERADOS")
        print("="*60)

        for i, post in enumerate(new_posts, 1):
            print(f"\n--- Post {i} ---")
            print(f"Fuente: {post['article']['source']}")
            print(f"Título: {post['article']['title']}")
            print(f"\nPost generado:")
            print(post['post_text'][:200] + "..." if len(post['post_text']) > 200 else post['post_text'])
            print()

        print("="*60)
        print(f"✨ Proceso completado. Posts guardados en: {self.posts_file}")
        if self.autonomous:
            print("🧠 El agente ha aprendido de esta generación y ajustará su comportamiento futuro")
        print("="*60)


if __name__ == "__main__":
    try:
        agent = SocialPostAgent()
        agent.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nAsegúrate de:")
        print("1. Tener un archivo .env con tu GEMINI_API_KEY")
        print("2. Haber instalado las dependencias: pip install -r requirements.txt")
