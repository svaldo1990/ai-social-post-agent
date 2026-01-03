#!/bin/bash

echo "🚀 AI Social Post Agent - Quick Start"
echo "===================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Verificar API key
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No se encontró archivo .env"
    echo "Por favor crea un archivo .env con tu GEMINI_API_KEY:"
    echo ""
    echo "GEMINI_API_KEY=tu-api-key-aqui"
    echo ""
    exit 1
fi

echo ""
echo "✅ Configuración completa"
echo ""
echo "Ahora puedes:"
echo "  1. Generar posts: python agent.py"
echo "  2. Iniciar servidor: python server.py"
echo ""
