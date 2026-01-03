# 📎 Fuentes Personalizadas - Guía de Uso

## ¿Qué son las Fuentes Personalizadas?

Además de generar posts automáticamente desde las fuentes configuradas (OpenAI, Google AI), ahora puedes **agregar cualquier artículo específico** desde cualquier URL para generar un post instantáneo.

---

## 🎯 ¿Cuándo usar Fuentes Personalizadas?

- Encontraste un artículo específico sobre IA que quieres convertir en post
- Quieres generar un post de un blog no incluido en las fuentes automáticas
- Necesitas un post urgente de una noticia reciente
- Quieres probar el generador con contenido específico

---

## 🚀 Cómo Usar (Interfaz Web)

### Paso 1: Abrir el Formulario
1. Abre la aplicación web: http://localhost:5173
2. Haz clic en el botón **"📎 Fuente Personalizada"**

### Paso 2: Agregar URL
1. **Pega la URL** del artículo en el campo "URL del Artículo"
2. (Opcional) Haz clic en **"🔍 Auto"** para detectar automáticamente el título y descripción
3. O escribe manualmente el título y descripción

### Paso 3: Generar
1. Haz clic en **"✨ Agregar Fuente"**
2. El sistema:
   - Extrae metadata automáticamente si no la proporcionaste
   - Genera el post usando **parámetros adaptativos** del agente autónomo
   - Guarda el post con fuente "Fuente Personalizada"
   - **Aprende** de esta generación (actualiza memoria del agente)
3. El post aparecerá inmediatamente en tu lista

---

## 💡 Detección Automática de Metadata

El sistema intenta extraer automáticamente:

- **Título**: De meta tags Open Graph o tag `<title>`
- **Descripción**: De meta tags Open Graph o meta description

### Ejemplo:
```
URL: https://openai.com/blog/chatgpt-vision
```

El sistema detectará:
- Título: "ChatGPT can now see, hear, and speak"
- Descripción: "ChatGPT can now see images, hear and speak..."

---

## 🧠 Integración con Agente Autónomo

Cuando agregas una fuente personalizada:

1. **Parámetros Adaptativos**: Usa los mismos parámetros que el agente autónomo (tono, formato, etc.)
2. **Aprendizaje**: El agente **registra** el artículo en su memoria
3. **Scoring**: El próximo scraping considerará esta fuente en su balance
4. **Evita Duplicados**: Si intentas agregar el mismo artículo dos veces, el agente lo recordará

---

## 📡 Uso por API (Programático)

### Obtener Metadata de una URL

```bash
curl "http://localhost:5001/api/fetch-metadata?url=https://ejemplo.com/articulo"
```

**Respuesta:**
```json
{
  "success": true,
  "metadata": {
    "title": "Título del artículo",
    "description": "Descripción extraída automáticamente"
  }
}
```

### Agregar Fuente y Generar Post

```bash
curl -X POST http://localhost:5001/api/custom-source \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://ejemplo.com/articulo-ia",
    "title": "Título opcional",
    "description": "Descripción opcional"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "article": {
    "title": "Título del artículo",
    "url": "https://ejemplo.com/articulo-ia",
    "description": "Descripción...",
    "source": "Fuente Personalizada",
    "scraped_at": "2026-01-03T12:00:00"
  },
  "post": {
    "id": "post_20260103_120000_custom",
    "post_text": "Post generado...",
    "article": { ... },
    "generated_at": "2026-01-03T12:00:00"
  },
  "message": "Post generado exitosamente desde fuente personalizada"
}
```

---

## 🎨 Ejemplo de Uso Completo

### Escenario: Quieres un post sobre un artículo de TechCrunch

1. **Encuentra el artículo**: https://techcrunch.com/2024/01/15/ai-breakthrough
2. **Abre la app web**
3. **Clic en "📎 Fuente Personalizada"**
4. **Pega la URL**
5. **Clic en "🔍 Auto"** (detecta título y descripción)
6. **Clic en "✨ Agregar Fuente"**
7. **¡Listo!** Tu post aparece en la lista con fuente "Fuente Personalizada"

---

## 📊 Ventajas vs Scraping Automático

| Característica | Scraping Automático | Fuente Personalizada |
|----------------|---------------------|----------------------|
| **Velocidad** | Busca múltiples fuentes | Instantáneo |
| **Control** | Artículos que el scraper encuentra | Tú eliges exactamente |
| **Fuentes** | OpenAI, Google AI (configuradas) | Cualquier URL |
| **Momento** | Cuando el agente decide | Cuando tú quieras |
| **Cantidad** | Múltiples posts | Un post específico |

---

## 🛠️ Personalización Avanzada

### Modificar Fuente por Defecto

En `backend/server.py`, línea 356:

```python
'source': 'Fuente Personalizada',  # Cambia esto
```

### Agregar Validación de URLs

Puedes agregar validación para solo permitir ciertos dominios:

```python
allowed_domains = ['techcrunch.com', 'wired.com', 'theverge.com']
domain = urlparse(url).netloc

if domain not in allowed_domains:
    return jsonify({
        'success': False,
        'error': f'Dominio {domain} no permitido'
    }), 400
```

---

## 🔍 Troubleshooting

### "No se pudo obtener metadata automáticamente"

**Causa**: El sitio web bloquea scraping o no tiene meta tags.

**Solución**: Escribe manualmente el título y descripción.

### "Error al procesar fuente"

**Causas posibles**:
- URL inválida
- Sitio web no accesible
- Timeout de conexión

**Solución**: Verifica que la URL sea válida y el sitio esté accesible.

### El post no aparece

**Solución**: Recarga la página (F5) o verifica la consola del navegador para errores.

---

## 💡 Tips y Mejores Prácticas

1. **Usa "🔍 Auto"**: Ahorra tiempo dejando que el sistema detecte metadata
2. **URLs completas**: Asegúrate de incluir `https://`
3. **Artículos en inglés**: El agente puede generar posts en español de artículos en inglés
4. **Fuentes confiables**: Mejor usar artículos de blogs reconocidos de IA
5. **Evita duplicados**: El agente recordará si ya procesaste ese artículo

---

## 🎓 Casos de Uso

### 1. Monitoreo Manual
```
Encuentras un artículo importante en Reddit/HackerNews
→ Copias URL
→ Agregas como fuente personalizada
→ Post listo en segundos
```

### 2. Cliente Solicita Post Específico
```
Cliente: "Necesito un post sobre este artículo de Anthropic"
→ Pegas URL del cliente
→ Generas y envías
```

### 3. Fuentes No Configuradas
```
Quieres posts de MIT Technology Review (no configurado)
→ Usas fuentes personalizadas para cada artículo
→ Sin necesidad de configurar scraper
```

---

## 📝 Nota sobre el Agente Autónomo

Las fuentes personalizadas **se integran completamente** con el agente autónomo:

- El agente **aprende** del artículo (actualiza su memoria)
- Usa **parámetros adaptativos** para generar el post
- **Evita duplicados** en futuras generaciones automáticas
- Contribuye al **balance de fuentes** en estadísticas

**¡Es como si el agente hubiera encontrado ese artículo por sí mismo!**

---

## 🚀 ¿Qué sigue?

- **Bulk upload**: Subir múltiples URLs a la vez
- **Scheduled posts**: Programar cuándo generar desde URLs guardadas
- **RSS feeds personalizados**: Agregar feeds RSS como fuentes
- **Browser extension**: Botón "Generar post" desde cualquier página

---

¿Tienes ideas para mejorar esta funcionalidad? ¡Comparte tu feedback!
