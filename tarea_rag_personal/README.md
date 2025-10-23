# 🎓 Asistente Académico RAG

Sistema RAG (Retrieval-Augmented Generation) en Python para consultar sílabos académicos usando Chroma como base de datos vectorial.

## Inicio Rápido

```bash
# 1. Instalar dependencias
make install

# 2. Elegir proveedor de LLM
# Opción A: Ollama (local, recomendado, sin API key)
ollama pull llama2
ollama serve  # En otra terminal

# Opción B: OpenAI API
export OPENAI_API_KEY="sk-..."

# 3. Ejecutar
make run
```

## Instalación Detallada

### Paso 1: Instalar dependencias
```bash
make install
```

### Paso 2: Configurar el modelo de lenguaje

**Opción A: Ollama (Recomendado - Local, sin costo)**
```bash
# 1. Descargar e instalar desde https://ollama.ai
# 2. En terminal 1, ejecutar el servidor:
ollama serve

# 3. En terminal 2, descargar el modelo:
ollama pull llama2
```

**Opción B: OpenAI API**
```bash
# Exportar tu API key de OpenAI
export OPENAI_API_KEY="sk-..."

# O crear un archivo .env:
echo "OPENAI_API_KEY=sk-..." > .env
```

## Uso

### Modo Interactivo (Recomendado)
```bash
make run
```

Luego escribe preguntas como:
- "¿Qué cursos enseñan gestión de proyectos?"
- "¿En qué ciclo se aborda ética profesional?"
- "¿Cuál es la fórmula del promedio final?"

**Cada respuesta muestra automáticamente los chunks recuperados** para que verifiques que se está usando la información correcta.

### Desde código Python
```python
from rag_system import inicializar_sistema_rag, consultar_rag

cadena_rag, recuperador = inicializar_sistema_rag()

# Mostrar chunks recuperados
consultar_rag(cadena_rag, "¿Qué cursos enseñan gestión de proyectos?", recuperador)

# Sin mostrar chunks (más silencioso)
consultar_rag(cadena_rag, "Tu pregunta aquí")
```

## Estructura de archivos

```
.
├── config.py              # Configuración centralizada
├── load_documents.py      # Carga PDFs de sílabos en Chroma
├── rag_system.py          # Sistema RAG con búsqueda semántica
├── main.py               # Interfaz interactiva
├── requirements.txt      # Dependencias Python
├── Makefile             # Comandos útiles
├── .env.example         # Plantilla para variables de entorno
├── silabus/             # PDFs de sílabos de la carrera
└── chroma_db/          # BD vectorial Chroma (creada automáticamente)
```

## Características

✨ **Minimalista**: Solo ~150 líneas de código Python esencial
📚 **RAG Automático**: Recuperación por similitud semántica + generación
🗂️ **Chroma**: BD vectorial eficiente para búsqueda semántica
🤖 **Flexible**: Usa Ollama (local) o OpenAI API
🔍 **Búsqueda Inteligente**: Encuentra cursos relacionados por temas
📖 **Visualización de Chunks**: Ve exactamente qué información usa para responder
🔧 **Debugging Integrado**: Verifica si se están usando los datos correctos

## Cómo Funciona

1. **Indexación**: Los PDFs se dividen en fragmentos y se convierten a vectores
2. **Consulta**: El usuario pregunta sobre un tema
3. **Búsqueda**: Se buscan los 5 fragmentos más similares
4. **Generación**: El LLM responde con información estructurada:
   - Cursos que cubren el tema
   - Ciclo académico
   - Bibliografía
   - Nivel de dificultad

## Personalización

### Cambiar el prompt del asistente
Edita `rag_system.py`, variable `PROMPT_ACADEMICO`

### Cambiar modelo de embeddings
En `config.py`, modifica `MODELO_EMBEDDINGS`

### Ajustar tamaño de fragmentos
En `config.py`, modifica `TAMAÑO_CHUNK` y `OVERLAP_CHUNK`

## Solución de Problemas

**Error: "No se puede conectar a Ollama"**
```bash
# Verifica que el servidor está ejecutándose:
ollama serve
```

**Error: "OPENAI_API_KEY no configurada"**
```bash
# Configura tu clave:
export OPENAI_API_KEY="sk-..."
# Luego cambia USAR_OLLAMA = False en config.py
```

**La BD Chroma tarda mucho en crearse la primera vez**
- Esto es normal. Espera a que se complete.
- Las siguientes ejecuciones serán más rápidas.

## Requisitos

- Python 3.9+
- 2-4 GB de RAM disponible
- Ollama instalado (si usas Ollama)
- O API key de OpenAI (si usas OpenAI)
