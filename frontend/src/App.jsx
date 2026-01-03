import { useState, useEffect } from 'react'
import './App.css'
import CustomSourceInput from './components/CustomSourceInput'

function App() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [stats, setStats] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [generationProgress, setGenerationProgress] = useState('')
  const [showCustomSource, setShowCustomSource] = useState(false)

  useEffect(() => {
    fetchPosts()
    fetchStats()
  }, [])

  const fetchPosts = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:5001/api/posts')
      const data = await response.json()

      if (data.success) {
        setPosts(data.posts)
      } else {
        setError('Error al cargar los posts')
      }
    } catch (err) {
      setError('No se pudo conectar con el servidor. Asegúrate de que el backend esté corriendo.')
    } finally {
      setLoading(false)
    }
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/stats')
      const data = await response.json()
      if (data.success) {
        setStats(data.stats)
      }
    } catch (err) {
      console.error('Error fetching stats:', err)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    alert('Post copiado al portapapeles!')
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const generateNewPosts = async () => {
    try {
      setGenerating(true)
      setGenerationProgress('Iniciando generación...')

      const response = await fetch('http://localhost:5001/api/generate', {
        method: 'POST'
      })

      const data = await response.json()

      if (!data.success) {
        alert(data.error || 'Error al iniciar generación')
        setGenerating(false)
        return
      }

      // Polling para verificar el progreso
      const checkStatus = setInterval(async () => {
        try {
          const statusResponse = await fetch('http://localhost:5001/api/generate/status')
          const statusData = await statusResponse.json()

          if (statusData.success) {
            const status = statusData.status
            setGenerationProgress(status.progress)

            if (!status.is_generating) {
              clearInterval(checkStatus)
              setGenerating(false)

              if (status.error) {
                alert('Error: ' + status.error)
              } else {
                // Recargar posts y stats
                await fetchPosts()
                await fetchStats()
                setGenerationProgress('')
              }
            }
          }
        } catch (err) {
          console.error('Error checking status:', err)
        }
      }, 2000) // Verificar cada 2 segundos

    } catch (err) {
      setGenerating(false)
      alert('Error al generar posts: ' + err.message)
    }
  }

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Cargando posts...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤖 AI Social Post Agent</h1>
        <p>Posts de LinkedIn generados automáticamente sobre Inteligencia Artificial</p>

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            className="generate-button"
            onClick={generateNewPosts}
            disabled={generating}
          >
            {generating ? (
              <>
                <div className="button-spinner"></div>
                {generationProgress || 'Generando...'}
              </>
            ) : (
              <>✨ Generar Nuevos Posts</>
            )}
          </button>

          <button
            className="generate-button"
            onClick={() => setShowCustomSource(!showCustomSource)}
            style={{ background: showCustomSource ? '#666' : 'linear-gradient(135deg, #0a66c2, #57a0d3)' }}
          >
            {showCustomSource ? '✕ Cerrar' : '📎 Fuente Personalizada'}
          </button>
        </div>

        {stats && (
          <div className="stats">
            <div className="stat-card">
              <span className="stat-number">{stats.total_posts}</span>
              <span className="stat-label">Posts totales</span>
            </div>
            {Object.entries(stats.sources).map(([source, count]) => (
              <div key={source} className="stat-card">
                <span className="stat-number">{count}</span>
                <span className="stat-label">{source}</span>
              </div>
            ))}
          </div>
        )}
      </header>

      {showCustomSource && (
        <CustomSourceInput
          onSourceAdded={() => {
            // Recargar posts y estadísticas
            fetchPosts()
            fetchStats()
            // Cerrar formulario después de un momento
            setTimeout(() => setShowCustomSource(false), 2500)
          }}
        />
      )}

      {error && (
        <div className="error">
          <p>{error}</p>
          <button onClick={fetchPosts}>Reintentar</button>
        </div>
      )}

      {posts.length === 0 ? (
        <div className="empty-state">
          <h2>No hay posts generados aún</h2>
          <p>Ejecuta el agente para generar posts:</p>
          <code>cd backend && python agent.py</code>
        </div>
      ) : (
        <div className="posts-container">
          {posts.map((post) => (
            <article key={post.id} className="post-card">
              <div className="post-header">
                <div className="post-source">
                  <span className="source-badge">{post.article.source}</span>
                  <span className="post-date">{formatDate(post.generated_at)}</span>
                </div>
                <button
                  className="copy-button"
                  onClick={() => copyToClipboard(post.post_text)}
                  title="Copiar al portapapeles"
                >
                  📋 Copiar
                </button>
              </div>

              <h2 className="article-title">{post.article.title}</h2>

              <div className="post-content">
                <pre>{post.post_text}</pre>
              </div>

              <div className="post-footer">
                <a
                  href={post.article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="article-link"
                >
                  Ver artículo original →
                </a>
              </div>
            </article>
          ))}
        </div>
      )}

      <footer className="footer">
        <p>Generado con Claude · {new Date().getFullYear()}</p>
      </footer>
    </div>
  )
}

export default App
