import { useState } from 'react'
import './CustomSourceInput.css'
import { API_URL } from '../config'

function CustomSourceInput({ onSourceAdded }) {
  const [sourceUrl, setSourceUrl] = useState('')
  const [sourceTitle, setSourceTitle] = useState('')
  const [sourceDescription, setSourceDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!sourceUrl.trim()) {
      setError('La URL es requerida')
      return
    }

    try {
      setLoading(true)
      setError(null)
      setSuccess(false)

      const response = await fetch(`${API_URL}/api/custom-source`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: sourceUrl.trim(),
          title: sourceTitle.trim() || undefined,
          description: sourceDescription.trim() || undefined
        })
      })

      const data = await response.json()

      if (data.success) {
        setSuccess(true)
        setSourceUrl('')
        setSourceTitle('')
        setSourceDescription('')

        if (onSourceAdded) {
          onSourceAdded(data.article)
        }

        // Limpiar mensaje de éxito después de 3 segundos
        setTimeout(() => setSuccess(false), 3000)
      } else {
        setError(data.error || 'Error al procesar la fuente')
      }
    } catch (err) {
      setError('Error de conexión con el servidor')
    } finally {
      setLoading(false)
    }
  }

  const handleFetchMetadata = async () => {
    if (!sourceUrl.trim()) {
      setError('Ingresa una URL primero')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetch(`${API_URL}/api/fetch-metadata?url=${encodeURIComponent(sourceUrl.trim())}`)
      const data = await response.json()

      if (data.success) {
        setSourceTitle(data.metadata.title || '')
        setSourceDescription(data.metadata.description || '')
      } else {
        setError('No se pudo obtener metadata automáticamente')
      }
    } catch (err) {
      setError('Error al obtener metadata')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="custom-source-input">
      <div className="custom-source-header">
        <h3>📎 Agregar Fuente Personalizada</h3>
        <p className="custom-source-subtitle">
          Agrega un artículo específico desde cualquier URL para generar un post
        </p>
      </div>

      <form onSubmit={handleSubmit} className="custom-source-form">
        <div className="form-group">
          <label htmlFor="sourceUrl">URL del Artículo *</label>
          <div className="url-input-group">
            <input
              type="url"
              id="sourceUrl"
              value={sourceUrl}
              onChange={(e) => setSourceUrl(e.target.value)}
              placeholder="https://ejemplo.com/articulo-sobre-ia"
              className="form-input"
              disabled={loading}
            />
            <button
              type="button"
              onClick={handleFetchMetadata}
              disabled={loading || !sourceUrl.trim()}
              className="fetch-metadata-btn"
              title="Obtener información automáticamente"
            >
              🔍 Auto
            </button>
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="sourceTitle">Título (opcional)</label>
          <input
            type="text"
            id="sourceTitle"
            value={sourceTitle}
            onChange={(e) => setSourceTitle(e.target.value)}
            placeholder="Se detectará automáticamente si se deja vacío"
            className="form-input"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="sourceDescription">Descripción (opcional)</label>
          <textarea
            id="sourceDescription"
            value={sourceDescription}
            onChange={(e) => setSourceDescription(e.target.value)}
            placeholder="Se detectará automáticamente si se deja vacío"
            className="form-textarea"
            rows="3"
            disabled={loading}
          />
        </div>

        {error && (
          <div className="alert alert-error">
            ⚠️ {error}
          </div>
        )}

        {success && (
          <div className="alert alert-success">
            ✅ Fuente agregada exitosamente. Ahora puedes generar posts.
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !sourceUrl.trim()}
          className="submit-source-btn"
        >
          {loading ? (
            <>
              <div className="btn-spinner"></div>
              Procesando...
            </>
          ) : (
            <>✨ Agregar Fuente</>
          )}
        </button>
      </form>

      <div className="custom-source-info">
        <p>💡 <strong>Tip:</strong> Puedes pegar cualquier URL de un artículo sobre IA y el agente intentará extraer automáticamente el título y descripción.</p>
      </div>
    </div>
  )
}

export default CustomSourceInput
