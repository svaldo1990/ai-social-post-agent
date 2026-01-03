import { useState, useEffect } from 'react'
import './AgentStatus.css'

function AgentStatus() {
  const [agentStatus, setAgentStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAgentStatus()
    // Actualizar cada 30 segundos
    const interval = setInterval(fetchAgentStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchAgentStatus = async () => {
    try {
      setLoading(true)
      const response = await fetch('http://localhost:5001/api/agent/status')
      const data = await response.json()

      if (data.success) {
        setAgentStatus(data.agent)
        setError(null)
      } else {
        setError('Error al obtener estado del agente')
      }
    } catch (err) {
      setError('No se pudo conectar con el servidor')
    } finally {
      setLoading(false)
    }
  }

  if (loading && !agentStatus) {
    return (
      <div className="agent-status-container">
        <div className="agent-status-loading">Cargando estado del agente...</div>
      </div>
    )
  }

  if (error) {
    return null // No mostrar nada si hay error
  }

  if (!agentStatus) return null

  const { memory, decision, adaptive_params } = agentStatus
  const diversityPercentage = (memory.topic_diversity * 100).toFixed(0)

  return (
    <div className="agent-status-container">
      <div className="agent-status-header">
        <h3>🧠 Estado del Agente Autónomo</h3>
        <button onClick={fetchAgentStatus} className="refresh-button" title="Actualizar">
          🔄
        </button>
      </div>

      <div className="agent-status-grid">
        {/* Memoria */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-icon">📚</span>
            <h4>Memoria</h4>
          </div>
          <div className="status-metrics">
            <div className="metric">
              <span className="metric-value">{memory.total_generations}</span>
              <span className="metric-label">Generaciones</span>
            </div>
            <div className="metric">
              <span className="metric-value">{memory.articles_processed}</span>
              <span className="metric-label">Artículos procesados</span>
            </div>
            <div className="metric">
              <span className="metric-value">{memory.topics_covered}</span>
              <span className="metric-label">Tópicos cubiertos</span>
            </div>
          </div>
        </div>

        {/* Diversidad */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-icon">🎨</span>
            <h4>Diversidad</h4>
          </div>
          <div className="diversity-container">
            <div className="diversity-bar-container">
              <div
                className="diversity-bar"
                style={{ width: `${diversityPercentage}%` }}
              ></div>
            </div>
            <div className="diversity-percentage">{diversityPercentage}%</div>
            <div className="diversity-label">
              {diversityPercentage >= 70 ? '✅ Excelente' :
               diversityPercentage >= 50 ? '👍 Buena' :
               '⚠️ Mejorable'}
            </div>
          </div>
        </div>

        {/* Decisión */}
        <div className={`status-card decision-card ${decision.should_generate_now ? 'ready' : 'waiting'}`}>
          <div className="status-card-header">
            <span className="status-icon">🎯</span>
            <h4>Decisión</h4>
          </div>
          <div className="decision-content">
            <div className={`decision-status ${decision.should_generate_now ? 'yes' : 'no'}`}>
              {decision.should_generate_now ? '✅ Listo para generar' : '⏳ Esperando'}
            </div>
            <div className="decision-reason">{decision.reason}</div>
          </div>
        </div>

        {/* Parámetros Adaptativos */}
        <div className="status-card">
          <div className="status-card-header">
            <span className="status-icon">⚙️</span>
            <h4>Parámetros Adaptativos</h4>
          </div>
          <div className="adaptive-params">
            <div className="param">
              <span className="param-label">Tono:</span>
              <span className="param-value">{adaptive_params.tone}</span>
            </div>
            <div className="param">
              <span className="param-label">Párrafos:</span>
              <span className="param-value">{adaptive_params.paragraph_count}</span>
            </div>
            <div className="param">
              <span className="param-label">Hashtags:</span>
              <span className="param-value">{adaptive_params.hashtag_count}</span>
            </div>
            <div className="param">
              <span className="param-label">Emojis:</span>
              <span className="param-value">{adaptive_params.emoji_level}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default AgentStatus
