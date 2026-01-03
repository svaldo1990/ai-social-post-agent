# 🧪 Guía de Testing

Esta guía explica cómo ejecutar los tests del proyecto.

---

## 📋 Tests Disponibles

### Backend (Python + pytest)
- ✅ Tests del scraper (artículos)
- ✅ Tests del generador (posts con Gemini)
- ✅ Tests de la API (endpoints Flask)

### Frontend (React + Vitest)
- ✅ Tests del componente App
- ✅ Tests de carga de datos
- ✅ Tests de interacciones de usuario

---

## 🚀 Ejecutar Tests del Backend

### Requisitos
```bash
cd backend
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install pytest pytest-flask  # Ya instalado si seguiste la guía
```

### Correr todos los tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Correr tests con detalles
```bash
pytest -v
```

### Correr tests con output detallado
```bash
pytest -v -s
```

### Correr un archivo específico
```bash
pytest tests/test_scraper.py
pytest tests/test_generator.py
pytest tests/test_server.py
```

### Correr un test específico
```bash
pytest tests/test_scraper.py::TestArticleScraper::test_scraper_initialization
```

### Ver cobertura de código
```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
# Abre htmlcov/index.html en tu navegador
```

---

## 🎨 Ejecutar Tests del Frontend

### Requisitos
```bash
cd frontend
npm install  # Las dependencias de testing ya están en package.json
```

### Correr todos los tests
```bash
cd frontend
npm test
```

### Correr tests en modo watch (se re-ejecutan al cambiar código)
```bash
npm test
```

### Correr tests con interfaz UI
```bash
npm run test:ui
```

### Ver cobertura de código
```bash
npm run test:coverage
```

### Correr tests una sola vez (para CI/CD)
```bash
npm test -- --run
```

---

## 📊 Estructura de Tests

```
agent-socialpost/
├── backend/
│   └── tests/
│       ├── __init__.py
│       ├── test_scraper.py      # Tests del web scraper
│       ├── test_generator.py    # Tests del generador de posts
│       └── test_server.py       # Tests de API endpoints
│
└── frontend/
    └── src/
        ├── test/
        │   └── setup.js         # Configuración de tests
        └── App.test.jsx         # Tests del componente principal
```

---

## ✅ Qué se está probando

### Backend

#### test_scraper.py
- ✓ Inicialización del scraper
- ✓ Scrape devuelve una lista
- ✓ Artículos tienen campos requeridos (title, url, description, source)
- ✓ Validación de tipos de datos
- ✓ No hay URLs duplicadas
- ✓ Artículos de fallback cuando scraping falla

#### test_generator.py
- ✓ Inicialización del generador
- ✓ Generación devuelve diccionario válido
- ✓ Posts tienen campos requeridos (id, post_text, article, generated_at)
- ✓ Parámetros adaptativos se aplican correctamente
- ✓ Manejo de artículos vacíos
- ✓ Formato correcto del ID del post

#### test_server.py
- ✓ Endpoint `/api/health` funciona
- ✓ Endpoint `/api/posts` devuelve lista de posts
- ✓ Endpoint `/api/stats` devuelve estadísticas
- ✓ Obtener post específico por ID
- ✓ Post inexistente devuelve 404
- ✓ Endpoints de metadata y custom sources
- ✓ Estado del agente autónomo
- ✓ Headers CORS presentes
- ✓ Content-Type es JSON

### Frontend

#### App.test.jsx
- ✓ Renderiza título principal
- ✓ Renderiza botones (generar, fuente personalizada)
- ✓ Muestra estado de carga
- ✓ Muestra posts cuando se cargan
- ✓ Muestra estadísticas correctamente
- ✓ Abre formulario de fuente personalizada
- ✓ Muestra estado vacío cuando no hay posts
- ✓ Renderiza footer con año actual
- ✓ Muestra mensaje de error cuando API falla
- ✓ Botón de reintentar aparece en errores

---

## 🐛 Solución de Problemas

### Backend: "ModuleNotFoundError"
```bash
# Asegúrate de estar en el entorno virtual
cd backend
source venv/bin/activate
pip install pytest pytest-flask
```

### Backend: "No module named 'google'"
```bash
# Instala las dependencias del proyecto
pip install -r requirements.txt
```

### Frontend: Tests no se ejecutan
```bash
# Reinstala dependencias
cd frontend
rm -rf node_modules
npm install
```

### Frontend: "Cannot find module '@testing-library/react'"
```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

---

## 📝 Escribir Nuevos Tests

### Ejemplo de test en Python
```python
# backend/tests/test_example.py
import pytest

def test_example():
    assert 1 + 1 == 2

def test_with_fixture(scraper):
    result = scraper.scrape_all()
    assert isinstance(result, list)
```

### Ejemplo de test en React
```jsx
// frontend/src/Example.test.jsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

---

## 🎯 Próximos Tests a Agregar

- [ ] Tests de integración (E2E) con Playwright o Cypress
- [ ] Tests del agente autónomo (agent_brain.py)
- [ ] Tests del componente CustomSourceInput
- [ ] Tests de la funcionalidad de copiar al portapapeles
- [ ] Mocks más completos para API de Gemini
- [ ] Tests de performance (tiempo de respuesta)
- [ ] Tests de accesibilidad (a11y)

---

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Testing Library](https://testing-library.com/)
- [Flask Testing](https://flask.palletsprojects.com/en/latest/testing/)

---

¿Preguntas sobre los tests? Revisa los archivos de test para ver ejemplos completos.
