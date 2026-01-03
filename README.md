# 🧠 AI Social Post Agent - **AGENTE AUTÓNOMO**

**Verdadero agente de IA autónomo** que busca artículos sobre Inteligencia Artificial, **toma decisiones inteligentes**, **aprende de cada generación** y genera posts optimizados para LinkedIn usando Google Gemini.

## 🆕 ¡Ahora con Capacidades Autónomas!

Este no es solo un script automatizado. Es un **agente autónomo real** que:

- 🧠 **Toma decisiones por sí mismo** sobre cuándo generar posts
- 📚 **Tiene memoria persistente** - recuerda artículos, tópicos y patrones
- 📊 **Aprende continuamente** - se adapta y mejora con cada ejecución
- 🎯 **Establece objetivos** - optimiza diversidad de contenido y balance de fuentes
- 🔄 **Se adapta dinámicamente** - ajusta tono, formato y estilo automáticamente

**📖 Ver [AGENTE_AUTONOMO.md](AGENTE_AUTONOMO.md) para documentación completa del sistema autónomo**

## Estructura del Proyecto

```
agent-socialpost/
├── backend/              # Agente Python (scraping + generación)
│   ├── agent.py         # Agente principal con capacidades autónomas
│   ├── agent_brain.py   # 🧠 Sistema autónomo (memoria, decisiones, aprendizaje)
│   ├── scraper.py       # Web scraper para artículos de AI
│   ├── generator.py     # Generador de posts con Gemini (adaptativo)
│   └── server.py        # API Flask con endpoints autónomos
├── frontend/            # Interfaz React
├── data/
│   ├── posts.json       # Posts generados
│   └── agent_memory.json # 🧠 Memoria persistente del agente
├── AGENTE_AUTONOMO.md   # 📖 Documentación del sistema autónomo
├── INSTRUCCIONES_AGENTE.md # Instrucciones de personalización
└── README.md
```

## Requisitos Previos

- Python 3.8+
- Node.js 16+
- API Key de Google Gemini ([obtener aquí](https://makersuite.google.com/app/apikey))

## Instalación Rápida

### 1. Configurar Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Crear archivo `.env` con tu API key:
```bash
# En backend/.env
GEMINI_API_KEY=tu-api-key-aqui
```

### 2. Configurar Frontend

```bash
cd frontend
npm install
```

## Uso

### Opción A: Ejecución Manual (3 terminales)

**Terminal 1 - Generar Posts:**
```bash
cd backend
source venv/bin/activate
python agent.py
```

**Terminal 2 - API Server:**
```bash
cd backend
source venv/bin/activate
python server.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm run dev
```

Luego abre http://localhost:5173 en tu navegador.

### Opción B: Solo Ver Posts Existentes (2 terminales)

Si ya generaste posts, solo necesitas:

**Terminal 1:**
```bash
cd backend
source venv/bin/activate
python server.py
```

**Terminal 2:**
```bash
cd frontend
npm run dev
```

## Funcionalidades

### 🧠 Capacidades Autónomas (NUEVO)
- **Toma de decisiones**: Evalúa automáticamente cuándo es óptimo generar posts
- **Memoria persistente**: Recuerda artículos procesados, tópicos cubiertos y patrones exitosos
- **Scoring inteligente**: Califica artículos por novedad, balance de fuentes y calidad (0-100 puntos)
- **Aprendizaje continuo**: Adapta parámetros de generación basándose en historial
- **Análisis de desempeño**: Monitorea diversidad de tópicos y balance de fuentes
- **Parámetros adaptativos**: Ajusta tono, formato y estilo dinámicamente

### 📎 Fuentes Personalizadas (NUEVO)
- **Agregar cualquier URL**: Genera posts desde cualquier artículo web, no solo fuentes configuradas
- **Detección automática**: Extrae título y descripción automáticamente con un clic
- **Generación instantánea**: Post listo en segundos desde la interfaz web
- **Integración con agente**: El agente aprende de las fuentes personalizadas y las integra en su memoria
- **API disponible**: Endpoints para automatizar la adición de fuentes

### 📰 Funcionalidades Core
- 🔍 **Scraping Automático**: Extrae artículos de blogs de AI (OpenAI, Google AI)
- 🤖 **Generación con IA**: Crea posts profesionales de LinkedIn con Google Gemini
- 💾 **Almacenamiento**: Guarda posts en JSON para persistencia
- 🌐 **Interfaz Web**: Visualiza y gestiona todos los posts generados
- 📋 **Copiar al Portapapeles**: Un clic para copiar posts
- 📊 **Estadísticas**: Ve cuántos posts tienes por fuente
- 🔗 **Links**: Acceso directo a los artículos originales

## Arquitectura

```
┌─────────────┐
│   Scraper   │  Busca artículos en blogs de AI
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Generator  │  Gemini genera posts de LinkedIn
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ JSON Store  │  Almacena posts generados
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Flask API  │  Sirve posts vía REST
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  React UI   │  Muestra posts en el navegador
└─────────────┘
```

## API Endpoints

### Posts
- `GET /api/posts` - Lista todos los posts
- `GET /api/posts/<id>` - Obtiene un post específico
- `GET /api/stats` - Estadísticas de posts
- `GET /api/health` - Health check

### Generación
- `POST /api/generate` - Genera nuevos posts (con sistema autónomo)
- `GET /api/generate/status` - Estado de la generación en progreso

### 🧠 Agente Autónomo (NUEVO)
- `GET /api/agent/status` - Estado completo del agente (memoria, decisiones, desempeño)
- `GET /api/agent/memory` - Memoria persistente del agente

### 📎 Fuentes Personalizadas (NUEVO)
- `GET /api/fetch-metadata?url=<url>` - Obtener metadata de una URL (título, descripción)
- `POST /api/custom-source` - Agregar fuente personalizada y generar post instantáneamente

## Personalización

### Agregar más fuentes de artículos

Edita [backend/scraper.py](backend/scraper.py) y agrega nuevos métodos:

```python
def scrape_new_source(self) -> List[Dict]:
    # Tu código de scraping aquí
    pass
```

### Modificar el estilo de posts

Edita el prompt en [backend/generator.py](backend/generator.py:21) para cambiar el tono o formato de los posts.

### Cambiar el diseño de la UI

Modifica los estilos en [frontend/src/App.css](frontend/src/App.css).

## Solución de Problemas

**Error: "GEMINI_API_KEY no está configurada"**
- Crea un archivo `.env` en el directorio `backend/` con tu API key de Gemini

**Error: "No se pudo conectar con el servidor"**
- Asegúrate de que el servidor Flask esté corriendo en el puerto 5000
- Verifica que no haya firewall bloqueando el puerto

**No se encontraron artículos**
- Algunos sitios pueden cambiar su estructura HTML
- Verifica tu conexión a internet
- Los selectores CSS en el scraper pueden necesitar actualización

## 🎯 Próximas Mejoras

### Fase 2: Agente más Inteligente
- [ ] Feedback loop real con LinkedIn API (likes, shares, comentarios)
- [ ] A/B testing automático de múltiples variantes de posts
- [ ] Scheduling inteligente (mejor hora del día para publicar)
- [ ] Objetivos dinámicos configurables por el usuario
- [ ] Multi-platform (adaptar posts para Twitter, Medium, etc.)

### Mejoras Generales
- [ ] Programar ejecución automática (cron job) - ✅ El agente ya decide cuándo generar
- [ ] Agregar más fuentes de noticias
- [ ] Filtrado de posts por fuente/fecha en UI
- [ ] Exportar posts a CSV
- [ ] Publicación directa a LinkedIn (usando API)
- [ ] Base de datos SQLite para mejor escalabilidad
- [ ] Docker compose para deployment fácil

## Licencia

MIT
