# Guía de Contexto para Claude Code

Este documento proporciona contexto sobre el proyecto AI Social Post Agent para ayudar a Claude Code a entender la arquitectura, decisiones técnicas y flujos de trabajo del proyecto.

> **🤖 Auto-inicialización**: Este archivo se lee automáticamente al iniciar Claude Code gracias a los archivos `.clinerules` y `.cursorrules` configurados en el proyecto.

## Resumen del Proyecto

**AI Social Post Agent** es una aplicación que genera posts de LinkedIn automáticamente usando IA. El agente es autónomo: decide cuándo generar, qué artículos seleccionar y cómo adaptar el tono basándose en su memoria y aprendizaje.

### Stack Tecnológico

- **Frontend**: React + Vite, deployado en Vercel
- **Backend**: Python + Flask, pendiente de deploy (actualmente local)
- **IA**: Google Gemini API
- **Scraping**: BeautifulSoup4 + Requests

## Estructura del Proyecto

```
agent-socialpost/
├── backend/                    # API Flask y lógica del agente
│   ├── server.py              # API REST endpoints
│   ├── agent_brain.py         # Sistema autónomo del agente
│   ├── agent.py               # Agente principal
│   ├── generator.py           # Generador de posts con Gemini
│   ├── scraper.py             # Web scraping de artículos
│   ├── requirements.txt       # Dependencias Python
│   └── tests/                 # Tests del backend
├── frontend/                   # Interfaz React
│   ├── src/
│   │   ├── App.jsx            # Componente principal
│   │   ├── config.js          # Configuración de API URL
│   │   └── components/
│   │       ├── AgentStatus.jsx        # Estado del agente
│   │       └── CustomSourceInput.jsx  # Entrada de fuentes custom
│   ├── package.json
│   └── vite.config.js
├── data/                       # Almacenamiento de datos
│   ├── posts.json             # Posts generados
│   └── agent_memory.json      # Memoria del agente (sensible)
├── .clinerules                 # Configuración para Claude Code
├── .cursorrules                # Configuración para Cursor IDE
└── vercel.json                # Configuración de deployment
```

## Componentes Clave del Backend

### 1. Agent Brain (`agent_brain.py`)
Sistema autónomo que:
- **Decide cuándo generar** posts (no genera todos los días)
- **Selecciona artículos** inteligentemente
- **Adapta parámetros** (tono, hashtags, emojis) según contexto
- **Aprende** de generaciones anteriores
- **Mantiene memoria** persistente

### 2. API Endpoints (`server.py`)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/posts` | GET | Lista todos los posts generados |
| `/api/posts/<id>` | GET | Obtiene un post específico |
| `/api/stats` | GET | Estadísticas de posts |
| `/api/health` | GET | Health check |
| `/api/generate` | POST | Inicia generación de posts (async) |
| `/api/generate/status` | GET | Estado de generación en progreso |
| `/api/agent/status` | GET | Estado del agente autónomo |
| `/api/agent/memory` | GET | Memoria completa del agente |
| `/api/custom-source` | POST | Agrega fuente personalizada |
| `/api/fetch-metadata` | GET | Obtiene metadata de URL |

### 3. Generador de Posts (`generator.py`)
- Usa Google Gemini API
- Genera posts estilo LinkedIn
- Parámetros adaptativos (tono, longitud, hashtags)

### 4. Scraper (`scraper.py`)
- Obtiene artículos de fuentes predefinidas
- Extrae título, descripción, URL

## Frontend

### Configuración de API

El frontend usa una variable de entorno para la URL del backend:

```javascript
// frontend/src/config.js
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';
```

**Importante**: Todos los componentes importan `API_URL` de `config.js` y lo usan para fetch:

```javascript
import { API_URL } from '../config'
const response = await fetch(`${API_URL}/api/posts`)
```

### Variables de Entorno

**Local** (`frontend/.env.local`):
```
VITE_API_URL=http://localhost:5001
```

**Producción** (Vercel):
- Configurar `VITE_API_URL` con la URL del backend deployado
- Ejemplo: `https://agent-socialpost-backend.railway.app`

## Estado Actual del Deployment

### ✅ Frontend (Vercel)
- **URL**: https://agent-socialpost.vercel.app
- **Estado**: Deployado y funcionando
- **Configuración**: Solo build del frontend
- **Problema actual**: No tiene backend conectado (usa localhost por defecto)

### ❌ Backend (Local)
- **Puerto**: 5001
- **Estado**: Solo funciona localmente
- **Pendiente**: Deploy a Railway, Render o similar

## Próximos Pasos de Deployment

### Para conectar Frontend + Backend:

1. **Deployar Backend** (opción recomendada: Railway)
   - Crear proyecto en Railway
   - Conectar repositorio
   - Configurar variable `GEMINI_API_KEY`
   - Railway auto-detecta Flask

2. **Configurar Frontend en Vercel**
   - Ir a Settings → Environment Variables
   - Agregar `VITE_API_URL` = `<URL_DE_RAILWAY>`
   - Re-deployar: `vercel --prod`

3. **Configurar CORS en Backend**
   - Verificar que CORS permita el dominio de Vercel
   - Ya está configurado con `flask-cors`

## Archivos Importantes

### No Commitear (`.gitignore`)
- `.env` - Variables de entorno sensibles
- `data/agent_memory.json` - Memoria del agente
- `.vercel/` - Archivos de deployment

### Sí Commitear
- `.clinerules` - Configuración de Claude Code
- `.cursorrules` - Configuración de Cursor
- `claude.md` - Este archivo (contexto del proyecto)

### Variables de Entorno Requeridas

**Backend**:
```bash
GEMINI_API_KEY=your-api-key-here
```

**Frontend**:
```bash
VITE_API_URL=http://localhost:5001  # local
VITE_API_URL=https://your-backend.railway.app  # producción
```

## Características del Agente Autónomo

### Sistema de Decisión
- Evalúa si debe generar basándose en:
  - Tiempo desde última generación
  - Diversidad de tópicos
  - Patrones históricos

### Sistema de Aprendizaje
- Rastrea qué funciona
- Ajusta parámetros dinámicamente
- Mejora selección de artículos

### Memoria Persistente
Almacena en `data/agent_memory.json`:
- Total de generaciones
- Historial de artículos
- Tópicos cubiertos
- Fuentes utilizadas
- Última generación

## Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

## Comandos Útiles

### Desarrollo Local
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python server.py

# Frontend
cd frontend
npm install
npm run dev
```

### Deployment
```bash
# Frontend a Vercel
vercel

# Ver logs
vercel logs

# Re-deploy
vercel --prod
```

## Decisiones Técnicas Importantes

### ¿Por qué Flask y no FastAPI?
- Simplicidad para el proyecto inicial
- CORS fácil con `flask-cors`
- Buen soporte para threading (generación async)

### ¿Por qué Vercel solo para Frontend?
- Backend usa threading y estado global
- No compatible con serverless functions de Vercel
- Railway/Render mejor para Flask con estado

### ¿Por qué Gemini y no OpenAI?
- API más económica
- Buen rendimiento para generación de texto
- Fácil integración con `google-genai`

## Problemas Conocidos y Soluciones

### Problema: CORS en producción
**Solución**: El backend ya tiene `CORS(app)` habilitado para todos los orígenes.

### Problema: Threading en serverless
**Solución**: No usar Vercel para backend, usar Railway/Render.

### Problema: Rate limiting de Gemini
**Solución**: El agente ya implementa decisiones inteligentes para no generar excesivamente.

## Contacto y Documentación Adicional

- [README.md](README.md) - Información general del proyecto
- [INSTRUCCIONES_AGENTE.md](INSTRUCCIONES_AGENTE.md) - Detalles del sistema autónomo
- [AGENTE_AUTONOMO.md](AGENTE_AUTONOMO.md) - Arquitectura del agente
- [FUENTES_PERSONALIZADAS.md](FUENTES_PERSONALIZADAS.md) - Guía de fuentes custom
- [TESTING.md](TESTING.md) - Documentación de tests

---

**Última actualización**: 2026-01-08
**Estado del proyecto**: Funcional en local, frontend deployado en Vercel, backend pendiente de deploy
