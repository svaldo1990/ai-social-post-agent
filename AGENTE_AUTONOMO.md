# 🧠 Agente Autónomo de Posts - Documentación

## ¿Qué es un Agente Autónomo?

Tu sistema ahora es un **verdadero agente de IA autónomo** que puede:

- 🧠 **Tomar decisiones por sí mismo** sobre cuándo generar posts
- 📚 **Recordar** lo que ha hecho anteriormente (memoria persistente)
- 📊 **Aprender** de cada generación para mejorar con el tiempo
- 🎯 **Establecer objetivos** como diversidad de contenido y balance de fuentes
- 🔄 **Adaptarse** cambiando su comportamiento según los resultados

---

## 🆚 Diferencias: Sistema Anterior vs Agente Autónomo

### Sistema Anterior (Automatizado)
```
Usuario presiona botón → Scrape → Generar → Guardar
```
- **Pasivo**: Solo actúa cuando el usuario lo ordena
- **Sin memoria**: No recuerda posts anteriores
- **Estático**: Siempre usa los mismos parámetros
- **Sin criterio**: Procesa todos los artículos sin discriminar

### Agente Autónomo Actual
```
Agente evalúa → Decide → Selecciona mejores artículos →
Adapta parámetros → Genera → Aprende → Mejora futuro
```
- **Proactivo**: Decide si es momento óptimo para generar
- **Con memoria**: Recuerda artículos, tópicos y patrones
- **Adaptativo**: Ajusta tono, formato y estilo dinámicamente
- **Inteligente**: Selecciona los mejores artículos con scoring

---

## 🏗️ Arquitectura del Sistema Autónomo

```
┌─────────────────────────────────────────────────────────┐
│                  AGENTE AUTÓNOMO                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   MEMORIA    │  │  DECISIONES  │  │ APRENDIZAJE  │ │
│  │              │  │              │  │              │ │
│  │ • Historial  │  │ • Cuándo     │  │ • Análisis   │ │
│  │ • Tópicos    │  │ • Qué usar   │  │ • Patrones   │ │
│  │ • Fuentes    │  │ • Scoring    │  │ • Mejoras    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
           ↓                    ↓                ↓
    [Persistencia]        [Evaluación]    [Adaptación]
```

---

## 📚 Sistema de Memoria

El agente mantiene un archivo `data/agent_memory.json` con:

### 1. **Historial de Artículos**
```json
{
  "article_history": [
    {
      "url": "https://...",
      "title": "GPT-4 Turbo",
      "source": "OpenAI Blog",
      "processed_at": "2026-01-02T23:51:01"
    }
  ]
}
```

### 2. **Tópicos Cubiertos**
```json
{
  "topics_covered": {
    "gpt": 15,
    "gemini": 12,
    "vision": 8,
    "multimodal": 5
  }
}
```

### 3. **Balance de Fuentes**
```json
{
  "sources_used": {
    "OpenAI Blog": 20,
    "Google AI Blog": 18,
    "Anthropic News": 15
  }
}
```

### 4. **Métricas de Generación**
- Total de generaciones
- Última fecha de generación
- Score de diversidad de tópicos (0-1)

---

## 🎯 Motor de Decisiones

### ¿Cuándo genera el agente?

El agente **evalúa automáticamente** si debe generar posts basándose en:

#### 1. **Reglas Temporales**
- ✅ **Primera ejecución**: Siempre genera
- ✅ **>24 horas desde última generación**: Genera
- ❌ **<4 horas desde última generación**: NO genera (muy reciente)

#### 2. **Diversidad de Contenido**
- Si la diversidad de tópicos < 50%: Fuerza generación para balancear

#### 3. **Ejemplo de Decisión**
```python
# El agente evalúa:
should_run, reason = agent.should_generate_now()

# Resultado:
✅ True: "Han pasado 25.3 horas desde la última generación"
❌ False: "Demasiado reciente (2.1 horas). Esperar al menos 4 horas"
```

### Scoring de Artículos

Cada artículo recibe un puntaje de 0-100:

| Criterio | Puntos | Descripción |
|----------|--------|-------------|
| **Novedad** | 40 pts | Artículo nunca procesado antes |
| **Balance de fuentes** | 30 pts | Fuentes poco usadas obtienen más puntos |
| **Calidad contenido** | 30 pts | Descripción detallada + título largo |

**Ejemplo:**
```
📄 GPT-4 Turbo with Vision
   Score: 85.0/100
   ✓ Artículo nuevo (nunca procesado)
   ✓ Fuente poco usada (3 veces, 15%)
   ✓ Descripción detallada disponible
   ✓ Título descriptivo
```

---

## 🎓 Sistema de Aprendizaje

### Parámetros Adaptativos

El agente **ajusta automáticamente** cómo genera los posts:

#### 1. **Tono Dinámico**
```python
# Si detecta muchos tópicos técnicos:
params['tone'] = 'más técnico y detallado'

# Por defecto:
params['tone'] = 'profesional pero accesible'
```

#### 2. **Variación de Formato**
```python
# Rotación basada en número de generaciones:
Generación #1, #4, #7: "2-3 párrafos cortos"
Generación #2, #5, #8: "1 párrafo impactante"
Generación #3, #6, #9: "4-5 párrafos detallados"
```

#### 3. **Análisis de Desempeño**
```python
{
  'total_posts_generated': 45,
  'sources_balance': {
    'OpenAI Blog': 20,
    'Google AI Blog': 15
  },
  'recommendations': [
    '⚠️ Desbalance en fuentes: algunas tienen 3x más posts',
    '💡 Poca diversidad de tópicos. Buscar fuentes variadas'
  ]
}
```

---

## 🚀 Cómo Usar el Agente Autónomo

### Opción 1: Modo Terminal (Interactivo)

```bash
cd backend
python3 agent.py
```

**El agente:**
1. Muestra reporte completo de su estado
2. Evalúa si debe generar
3. Te pide confirmación antes de proceder
4. Selecciona mejores artículos con scoring
5. Genera con parámetros adaptativos
6. Aprende y actualiza su memoria

**Output esperado:**
```
🤖 AI Social Post Agent
🧠 MODO AUTÓNOMO ACTIVADO
══════════════════════════════════════════════════════════

🤖 REPORTE DE ESTADO DEL AGENTE AUTÓNOMO
══════════════════════════════════════════════════════════

📊 Memoria:
   • Generaciones totales: 3
   • Artículos procesados: 9
   • Tópicos cubiertos: 12
   • Diversidad de tópicos: 67.50%
   • Última generación: 2026-01-02 23:51:23

📈 Desempeño:
   • Posts generados total: 8
   • Balance de fuentes:
     - OpenAI Blog: 3 posts
     - Google AI Blog: 5 posts

🎯 Decisión autónoma:
   • Generar ahora: ✅ SÍ
   • Razón: Han pasado 25.3 horas desde la última generación

⚙️  Parámetros adaptativos actuales:
   • tone: profesional pero accesible
   • emoji_level: sutil (1-2 máximo)
   • hashtag_count: 3-4
   • paragraph_count: 2-3

══════════════════════════════════════════════════════════

✅ El agente decide generar nuevos posts:
   Razón: Han pasado 25.3 horas desde la última generación

⏸  Presiona Enter para continuar...
```

### Opción 2: Modo Web (Interfaz)

```bash
# Terminal 1: Servidor backend
cd backend
python3 server.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Abrir:** http://localhost:5173

**Nuevas funcionalidades web:**
- El botón "Generar Posts" ahora usa el agente autónomo
- Muestra mensajes como: "🧠 Evaluando con sistema autónomo..."
- Puedes ver el estado del agente en la consola del servidor

### Opción 3: API Directa

#### Ver Estado del Agente
```bash
curl http://localhost:5001/api/agent/status
```

**Respuesta:**
```json
{
  "success": true,
  "agent": {
    "memory": {
      "total_generations": 3,
      "articles_processed": 9,
      "topics_covered": 12,
      "topic_diversity": 0.675,
      "last_generation": "2026-01-02T23:51:01",
      "sources_used": {
        "OpenAI Blog": 3,
        "Google AI Blog": 5
      }
    },
    "decision": {
      "should_generate_now": true,
      "reason": "Han pasado 25.3 horas desde la última generación"
    },
    "performance": {
      "total_posts_generated": 8,
      "recommendations": []
    },
    "adaptive_params": {
      "tone": "profesional pero accesible",
      "emoji_level": "sutil (1-2 máximo)",
      "hashtag_count": "3-4",
      "paragraph_count": "2-3"
    }
  }
}
```

#### Ver Memoria Completa
```bash
curl http://localhost:5001/api/agent/memory
```

---

## 📊 Nuevos Endpoints de API

### `GET /api/agent/status`
Retorna el estado completo del agente autónomo.

**Campos:**
- `memory`: Estadísticas de memoria
- `decision`: Decisión actual sobre generación
- `performance`: Análisis de desempeño histórico
- `adaptive_params`: Parámetros adaptativos actuales

### `GET /api/agent/memory`
Retorna la memoria completa sin procesar del agente.

---

## 🎮 Modo Autónomo vs Modo Manual

### Activar/Desactivar Modo Autónomo

En `backend/agent.py`:

```python
# Modo autónomo (por defecto)
agent = SocialPostAgent(autonomous=True)

# Modo manual (comportamiento antiguo)
agent = SocialPostAgent(autonomous=False)
```

### Diferencias

| Característica | Autónomo | Manual |
|----------------|----------|--------|
| Decide cuándo generar | ✅ | ❌ |
| Selecciona artículos | ✅ Scoring | ❌ Todos |
| Parámetros adaptativos | ✅ | ❌ |
| Aprende y mejora | ✅ | ❌ |
| Memoria persistente | ✅ | ❌ |

---

## 🔧 Personalización del Agente

### 1. Ajustar Reglas de Decisión

En `backend/agent_brain.py`, método `should_generate_now()`:

```python
# Cambiar mínimo de horas entre generaciones
if hours_passed >= 24:  # Cambia este número
    return True, f"Han pasado {hours_passed:.1f} horas"

# Ajustar umbral de diversidad
if diversity < 0.5:  # Cambia este umbral (0-1)
    return True, f"Baja diversidad de tópicos"
```

### 2. Modificar Sistema de Scoring

En `backend/agent_brain.py`, método `score_article()`:

```python
# Puntos por novedad
if not self.memory.was_article_processed(article['url']):
    score += 40  # Cambia estos valores

# Puntos por balance de fuentes
if source_ratio < 0.3:
    score += 30  # Ajusta según importancia
```

### 3. Cambiar Parámetros Adaptativos

En `backend/agent_brain.py`, método `get_adaptive_prompt_params()`:

```python
# Personalizar rotación de formatos
if gen_count % 3 == 0:
    params['paragraph_count'] = '1 párrafo impactante'
elif gen_count % 3 == 1:
    params['paragraph_count'] = '3 párrafos medios'  # Personaliza
```

---

## 🐛 Troubleshooting

### El agente decide NO generar

**Causa:** Reglas temporales o de diversidad no cumplidas.

**Solución:**
```bash
# Ver por qué decidió no generar
curl http://localhost:5001/api/agent/status | jq '.agent.decision'

# Resultado:
{
  "should_generate_now": false,
  "reason": "Demasiado reciente (2.1 horas). Esperar al menos 4 horas"
}
```

**Forzar generación:** Ajusta las reglas en `agent_brain.py` o espera el tiempo indicado.

### Memoria corrupta

```bash
# Resetear memoria del agente
rm data/agent_memory.json

# El agente creará una nueva en la siguiente ejecución
```

### Artículos duplicados

El agente **evita automáticamente** artículos ya procesados gracias a su memoria. Si ves duplicados:

```bash
# Verificar memoria
curl http://localhost:5001/api/agent/memory | jq '.memory.article_history'
```

---

## 📈 Mejoras Futuras Sugeridas

### 1. **Feedback Loop Real**
Conectar con LinkedIn API para obtener métricas reales:
- Likes, comentarios, shares
- Usar estas métricas para mejorar scoring

### 2. **Objetivos Dinámicos**
```python
# Ejemplo:
agent.set_goal("Aumentar engagement en posts técnicos")
agent.set_goal("Mantener 33% balance entre fuentes")
```

### 3. **A/B Testing Automático**
Generar múltiples variantes de un post y aprender cuál funciona mejor.

### 4. **Scheduling Inteligente**
Decidir la mejor hora del día para publicar basándose en patrones históricos.

### 5. **Multi-Platform**
Expandir a otras redes: Twitter, Medium, etc., adaptando el tono por plataforma.

---

## 💡 Ejemplos de Uso Avanzado

### Escenario 1: Ejecutar en Cron Job

```bash
# Agregar a crontab (ejecutar diariamente a las 9am)
0 9 * * * cd /ruta/proyecto/backend && python3 agent.py
```

**El agente evaluará** automáticamente si debe generar, basándose en sus reglas.

### Escenario 2: Monitorear Desde Python

```python
from agent_brain import AutonomousAgent

# Crear agente
brain = AutonomousAgent()

# Verificar decisión
should_run, reason = brain.decision_engine.should_generate_now()
print(f"Generar: {should_run} - {reason}")

# Ver diversidad
diversity = brain.memory.get_topic_diversity_score()
print(f"Diversidad: {diversity:.2%}")

# Análisis completo
brain.print_status_report()
```

### Escenario 3: Integración con Webhook

```python
# En server.py, agregar:
@app.route('/webhook/linkedin', methods=['POST'])
def linkedin_webhook():
    """Recibe datos de engagement de LinkedIn"""
    data = request.json
    # Usar data para mejorar sistema de aprendizaje
    # ... implementación futura
```

---

## 🎯 Conclusión

Ahora tienes un **verdadero agente de IA autónomo** que:

- ✅ Toma decisiones inteligentes por sí mismo
- ✅ Recuerda todo lo que ha hecho
- ✅ Aprende y se adapta continuamente
- ✅ Optimiza diversidad y calidad de contenido
- ✅ Mejora con cada ejecución

**No es solo un script automatizado**, es un agente que **piensa, aprende y evoluciona**.

---

## 📚 Recursos

- **Código del cerebro:** [backend/agent_brain.py](backend/agent_brain.py)
- **Agente principal:** [backend/agent.py](backend/agent.py)
- **API Server:** [backend/server.py](backend/server.py)
- **Instrucciones generales:** [INSTRUCCIONES_AGENTE.md](INSTRUCCIONES_AGENTE.md)

---

**¿Preguntas?** El agente está listo para ser ejecutado y comenzar a aprender.
