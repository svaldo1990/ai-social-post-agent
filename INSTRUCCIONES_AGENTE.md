# Instrucciones para Configurar el Agente de Posts

Este documento contiene instrucciones detalladas para personalizar el comportamiento del agente de generación de posts de LinkedIn.

## 📋 Tabla de Contenidos

1. [Configuración del Scraper](#configuración-del-scraper)
2. [Personalización de Posts](#personalización-de-posts)
3. [Agregar Nuevas Fuentes](#agregar-nuevas-fuentes)
4. [Modificar el Prompt de Gemini](#modificar-el-prompt-de-gemini)
5. [Configuración Avanzada](#configuración-avanzada)

---

## 🔍 Configuración del Scraper

### Ubicación del Archivo
[backend/scraper.py](backend/scraper.py)

### Modificar Artículos de Ejemplo (Fallback)

Cuando el scraper no puede encontrar artículos en vivo, usa artículos de ejemplo. Para modificarlos:

```python
def get_fallback_articles(self) -> List[Dict]:
    """Artículos de ejemplo en caso de que el scraping falle"""
    return [
        {
            'title': 'Tu Título Aquí',
            'url': 'https://tu-enlace.com',
            'description': 'Tu descripción del artículo',
            'source': 'Nombre de la Fuente',
            'scraped_at': datetime.now().isoformat()
        },
        # Agrega más artículos aquí...
    ]
```

### Ajustar Cantidad Mínima de Artículos

Por defecto, el agente busca al menos 3 artículos. Para cambiar esto:

En [backend/scraper.py](backend/scraper.py), línea 171:
```python
if len(all_articles) < 3:  # Cambia el 3 por el número que prefieras
```

---

## ✍️ Personalización de Posts

### Ubicación del Archivo
[backend/generator.py](backend/generator.py)

### Modificar el Tono de los Posts

El prompt que controla cómo Gemini genera los posts está en la línea 26-45. Puedes modificarlo para cambiar:

#### Cambiar el Tono

**Ejemplo: Más casual**
```python
prompt = f"""Eres un creador de contenido casual para LinkedIn sobre IA.

Basándote en el siguiente artículo, crea un post relajado y amigable:

Título: {article['title']}
...

Requisitos del post:
- Usa un lenguaje casual y cercano
- Incluye más emojis (3-5)
- Habla en primera persona
- Termina con una pregunta directa a la audiencia
```

**Ejemplo: Más técnico/profesional**
```python
prompt = f"""Eres un analista senior de IA escribiendo para ejecutivos de tecnología.

Basándote en el siguiente artículo, crea un análisis profesional:

Título: {article['title']}
...

Requisitos del post:
- Lenguaje técnico pero accesible
- Enfoque en impacto de negocio
- Sin emojis
- Incluye insights estratégicos
- Formato ejecutivo: problema-solución-acción
```

#### Cambiar la Longitud

En la línea 37, modifica:
```python
- Incluye 2-3 párrafos cortos  # Cambia esto por:
- Incluye 1 párrafo impactante  # Para posts cortos
# O
- Incluye 4-5 párrafos detallados  # Para posts largos
```

#### Modificar Hashtags

En la línea 41:
```python
- NO uses hashtags excesivos (máximo 3-4 relevantes)  # Cambia por:
- Incluye 5-7 hashtags populares de IA  # Para más hashtags
# O
- NO incluyas hashtags  # Para sin hashtags
```

### Cambiar el Modelo de IA

En la línea 49, puedes cambiar el modelo de Gemini:
```python
model='gemini-2.5-flash',  # Actual (rápido y económico)
# Opciones alternativas:
# 'gemini-2.5-pro'  # Más potente, más lento
# 'gemini-2.0-flash'  # Versión anterior
```

---

## 🌐 Agregar Nuevas Fuentes

Para agregar un nuevo sitio web como fuente de artículos:

### Paso 1: Crear Método de Scraping

En [backend/scraper.py](backend/scraper.py), agrega un nuevo método:

```python
def scrape_tu_sitio(self) -> List[Dict]:
    """Scrape artículos de Tu Sitio"""
    articles = []
    try:
        url = "https://tu-sitio.com/blog"
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Ajusta los selectores según la estructura HTML del sitio
        article_elements = soup.find_all('article', limit=5)

        for element in article_elements:
            title_elem = element.find('h2')
            link_elem = element.find('a', href=True)
            desc_elem = element.find('p')

            if title_elem and link_elem:
                articles.append({
                    'title': title_elem.get_text(strip=True),
                    'url': link_elem['href'],
                    'description': desc_elem.get_text(strip=True)[:300] if desc_elem else '',
                    'source': 'Tu Sitio',
                    'scraped_at': datetime.now().isoformat()
                })

    except Exception as e:
        print(f"Error scraping Tu Sitio: {e}")

    return articles
```

### Paso 2: Agregar a la Lista de Fuentes

En el método `get_ai_articles()`, línea 158-168:

```python
def get_ai_articles(self) -> List[Dict]:
    all_articles = []

    print("Scraping OpenAI blog...")
    all_articles.extend(self.scrape_openai_blog())

    print("Scraping Google AI blog...")
    all_articles.extend(self.scrape_google_ai_blog())

    # AGREGA TU NUEVA FUENTE AQUÍ
    print("Scraping Tu Sitio...")
    all_articles.extend(self.scrape_tu_sitio())

    # ... resto del código
```

---

## 🎯 Modificar el Prompt de Gemini

### Estructura Recomendada del Prompt

Un buen prompt tiene estas secciones:

```python
prompt = f"""
[1. IDENTIDAD]
Eres un [rol específico] con experiencia en [área].

[2. CONTEXTO]
Basándote en el siguiente artículo:
Título: {article['title']}
Fuente: {article['source']}
Descripción: {article['description']}

[3. TAREA]
Crea un post para LinkedIn que [objetivo específico].

[4. REQUISITOS]
- Requisito 1
- Requisito 2
- Requisito 3

[5. FORMATO]
- Estructura esperada
- Elementos a incluir/excluir

[6. RESTRICCIONES]
Genera SOLO el texto del post, sin comentarios adicionales.
"""
```

### Ejemplos de Prompts Personalizados

#### Para Posts de Opinión
```python
prompt = f"""Eres un líder de opinión en tecnología con 15 años de experiencia.

Artículo: {article['title']} de {article['source']}
Descripción: {article['description']}

Crea un post de opinión que:
- Presente tu perspectiva única sobre este avance
- Conecte con experiencias reales del sector
- Provoque debate constructivo

Formato:
1. Hook controversial
2. Tu opinión respaldada
3. Pregunta para debate

Sin emojis. Tono provocador pero profesional.
"""
```

#### Para Posts Educativos
```python
prompt = f"""Eres un educador que simplifica conceptos complejos de IA.

Artículo: {article['title']}
URL: {article['url']}

Crea un post educativo que:
- Explique el concepto principal en términos simples
- Use analogías cotidianas
- Incluya 3 puntos clave de aprendizaje

Formato:
• Introducción con analogía
• 3 puntos bullet con explicaciones
• Conclusión práctica

Incluye 2-3 emojis educativos (💡📚🎓).
"""
```

---

## ⚙️ Configuración Avanzada

### Modificar Almacenamiento de Posts

Por defecto, los posts se guardan en [data/posts.json](../data/posts.json).

Para cambiar la ubicación, edita [backend/agent.py](backend/agent.py), línea 14:
```python
def __init__(self, data_dir: str = "../data"):  # Cambia la ruta aquí
```

### Ajustar Formato de ID de Posts

En [backend/agent.py](backend/agent.py), línea 48:
```python
post['id'] = f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}"
# Personaliza el formato:
# post['id'] = f"linkedin_{article['source']}_{i}"  # Por fuente
# post['id'] = str(uuid.uuid4())  # UUID aleatorio
```

### Configurar Headers del Scraper

Para mejorar el scraping, puedes modificar los headers en [backend/scraper.py](backend/scraper.py), línea 14-23:

```python
self.headers = {
    'User-Agent': 'Tu User Agent Personalizado',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'es-ES,es;q=0.9',  # Cambiar idioma
    'Referer': 'https://google.com',  # Agregar referer
}
```

### Modificar Timeout de Requests

En los métodos de scraping, línea 31 y similares:
```python
response = requests.get(url, headers=self.headers, timeout=15)
# Cambia 15 por el número de segundos que prefieras
```

---

## 🚀 Ejecución y Testing

### Probar el Scraper Solo

```bash
cd backend
source venv/bin/activate
python scraper.py
```

### Probar el Generador Solo

```bash
cd backend
source venv/bin/activate
python generator.py
```

### Ejecutar el Agente Completo

```bash
cd backend
source venv/bin/activate
python agent.py
```

### Desde la Interfaz Web

1. Abre http://localhost:5173
2. Haz clic en "✨ Generar Nuevos Posts"
3. Observa el progreso en tiempo real

---

## 📝 Notas Importantes

1. **Siempre prueba los cambios** ejecutando primero `python scraper.py` o `python generator.py` antes del agente completo.

2. **Respeta los límites de las APIs**: Gemini tiene límites de requests por minuto en el plan gratuito.

3. **Backup de posts**: Los posts se sobrescriben en cada ejecución. Haz backup de `data/posts.json` si es necesario.

4. **Actualiza el servidor**: Después de cambios en el backend, reinicia el servidor con `Ctrl+C` y `python server.py`.

---

## 🐛 Troubleshooting

### El scraper no encuentra artículos
- Verifica tu conexión a internet
- Los sitios web pueden cambiar su estructura HTML
- Usa artículos de fallback mientras investigas

### Gemini devuelve errores 429
- Excediste la cuota gratuita
- Espera unos minutos o usa un modelo diferente

### Los posts no aparecen en la web
- Recarga la página (F5)
- Verifica que el servidor esté corriendo en puerto 5001
- Revisa la consola del navegador (F12) para errores

---

## 💡 Ideas de Personalización

1. **Multi-idioma**: Agrega un parámetro de idioma al prompt
2. **Categorías**: Filtra artículos por categoría antes de generar
3. **Programación**: Usa cron jobs para ejecutar automáticamente
4. **Calidad**: Agrega un sistema de puntuación de posts
5. **A/B Testing**: Genera múltiples versiones y compara

---

¿Necesitas ayuda con alguna personalización específica? Consulta el [README.md](README.md) principal o revisa el código fuente con comentarios.
