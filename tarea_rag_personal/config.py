import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).parent
SILABUS_DIR = BASE_DIR / "silabus"
DB_DIR = BASE_DIR / "chroma_db"

# Crear directorios si no existen
DB_DIR.mkdir(exist_ok=True)

# Configuración del modelo - elige el proveedor
# Opción 1: Ollama (local, sin API key) - recomendado
USAR_OLLAMA = True
MODELO_OLLAMA = "llama3.1"  # alternativas: neural-chat, mistral, etc.

# Opción 2: OpenAI API (configura OPENAI_API_KEY como variable de entorno)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODELO_OPENAI = "gpt-4"  # alternativas: gpt-3.5-turbo

# Configuración de Chroma
# Nota: Se aumentó TAMAÑO_CHUNK para mantener secciones completas de evaluación
NOMBRE_COLECCION = "silabus_collection"
TAMAÑO_CHUNK = 2000  # Aumentado de 1000 para capturar secciones de evaluación completas
OVERLAP_CHUNK = 400  # Aumentado para mejor contexto entre chunks
