import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from './App'

// Mock fetch global
global.fetch = vi.fn()

describe('App Component', () => {
  beforeEach(() => {
    // Reset mocks before each test
    fetch.mockClear()
  })

  it('renders the main title', async () => {
    // Mock successful API responses
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    const title = await screen.findByText(/AI Social Post Agent/i)
    expect(title).toBeInTheDocument()
  })

  it('renders generate posts button', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    const generateButton = await screen.findByText(/Generar Nuevos Posts/i)
    expect(generateButton).toBeInTheDocument()
  })

  it('renders custom source button', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    const customSourceButton = await screen.findByText(/Fuente Personalizada/i)
    expect(customSourceButton).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    fetch.mockImplementation(() => new Promise(() => {})) // Never resolves

    render(<App />)

    expect(screen.getByText(/Cargando posts.../i)).toBeInTheDocument()
  })

  it('displays posts when loaded', async () => {
    const mockPosts = [
      {
        id: 'post_1',
        post_text: 'Test post content',
        article: {
          title: 'Test Article',
          url: 'https://example.com',
          source: 'Test Source'
        },
        generated_at: '2026-01-03T12:00:00'
      }
    ]

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: mockPosts })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 1, sources: { 'Test Source': 1 } } })
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('Test Article')).toBeInTheDocument()
    })
  })

  it('displays statistics correctly', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        stats: {
          total_posts: 5,
          sources: {
            'OpenAI Blog': 3,
            'Google AI Blog': 2
          }
        }
      })
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText('5')).toBeInTheDocument()
      expect(screen.getByText('OpenAI Blog')).toBeInTheDocument()
      expect(screen.getByText('Google AI Blog')).toBeInTheDocument()
    })
  })

  it('shows custom source form when button clicked', async () => {
    const user = userEvent.setup()

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    const customSourceButton = await screen.findByText(/Fuente Personalizada/i)
    await user.click(customSourceButton)

    // Should show the close button after opening
    await waitFor(() => {
      expect(screen.getByText(/Cerrar/i)).toBeInTheDocument()
    })
  })

  it('displays empty state when no posts', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/No hay posts generados aún/i)).toBeInTheDocument()
    })
  })

  it('renders footer with current year', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, posts: [] })
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, stats: { total_posts: 0, sources: {} } })
    })

    render(<App />)

    const currentYear = new Date().getFullYear()
    const footer = await screen.findByText(new RegExp(currentYear.toString()))
    expect(footer).toBeInTheDocument()
  })

  it('shows error message when API fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))
      .mockRejectedValueOnce(new Error('Network error'))

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText(/No se pudo conectar con el servidor/i)).toBeInTheDocument()
    })
  })

  it('has retry button when error occurs', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))
      .mockRejectedValueOnce(new Error('Network error'))

    render(<App />)

    await waitFor(() => {
      const retryButton = screen.getByText(/Reintentar/i)
      expect(retryButton).toBeInTheDocument()
    })
  })
})
