"""
Configuración de pytest para los tests del backend
"""
import sys
import os

# Agregar el directorio backend al Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
