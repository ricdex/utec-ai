# 🗓️ Asistente de Planificación Diaria con LangGraph + Llama 3.2

## 📝 Descripción

Sistema agéntico que ayuda a planificar el día de forma inteligente usando:
- **LangGraph**: Define un workflow con 3 nodos
- **Llama 3.2**: Analiza actividades y valida descansos mediante IA
- **Validador**: Rechaza planes sin descansos adecuados después de actividades intensas

El flujo es: **Usuario → Analizador (Llama) → Planificador → Validador (Llama) → Plan Final**

---

## 🚀 Instalación y Ejecución

### 1. Instalar Ollama
Descarga desde [ollama.ai](https://ollama.ai)

### 2. Descargar Modelo Llama 3.2
```bash
ollama pull llama3.2
```

### 3. Instalar Dependencias Python
```bash
pip install -r requirements.txt
```

### 4. Iniciar Servidor Ollama (Terminal 1)
```bash
ollama serve
```

### 5. Ejecutar el Programa (Terminal 2)
```bash
python daily_planner_with_llama.py
```

---

## 💡 Ejemplo de Ejecución

**Input:**
```
Describe tu día: Tengo clases de IA, gimnasio y debo estudiar
```

**Output:**
```
ACTIVIDADES DETECTADAS (por Llama 3.2):
  • CLASES: 60 min
  • EJERCICIO: 60 min
  • ESTUDIO: 60 min

📅 PLAN DIARIO PERSONALIZADO
==================================================

HORARIO:
✓ 07:00-08:00    → Desayuno
✓ 08:00-12:00    → Clases/Trabajo
  12:00-13:30    → Almuerzo
✓ 13:30-15:30    → Estudio
  15:30-16:00    → Pausa
✓ 16:00-17:30    → Ejercicio
  17:30-19:00    → Personal
  19:00-20:00    → Cena
  20:00-22:00    → Relax
  22:00+         → Dormir

==================================================
💡 RECOMENDACIONES:
• Descarga diapositivas
• Estudia 50 min + descanso
• Mantente hidratado
• 7-8 horas sueño

==================================================
¡Buen día! 💪

============================================================
VALIDACIÓN (por Llama 3.2):
------------------------------------------------------------
✅ PLAN APROBADO - Descansos adecuados (validado por Llama 3.2)
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│              ENTRADA DEL USUARIO                │
│         "Clases, gimnasio, estudiar"            │
└─────────────────┬───────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │   NODO 1           │
        │   ANALIZADOR       │
        ├────────────────────┤
        │ Llama 3.2 extrae   │
        │ actividades        │
        │ → JSON             │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   NODO 2           │
        │   PLANIFICADOR     │
        ├────────────────────┤
        │ Genera horario     │
        │ + recomendaciones  │
        │ → Plan             │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   NODO 3           │
        │   VALIDADOR        │
        ├────────────────────┤
        │ Llama 3.2 valida   │
        │ descansos          │
        │ → APROBADO/        │
        │   RECHAZADO        │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │   PLAN FINAL       │
        │ + VALIDACIÓN       │
        └────────────────────┘
```

---

## 🔑 Componentes Principales

### Nodo 1: Analizador (con Llama 3.2)
- Lee entrada del usuario
- Usa Llama 3.2 para extraer actividades de forma inteligente
- Devuelve JSON con actividades clasificadas

### Nodo 2: Planificador
- Recibe actividades
- Genera horario (07:00-22:00+)
- Incluye recomendaciones personalizadas

### Nodo 3: Validador (con Llama 3.2)
- Verifica descansos adecuados
- Rechaza planes sin pausas tras clases/ejercicio/trabajo
- Aprueba planes saludables

---

## 🦙 Uso de Llama 3.2

El proyecto usa Llama 3.2 explícitamente en:

```python
# Inicialización (Línea 16)
from langchain.llms import Ollama
llm = Ollama(model="llama3.2", temperature=0.7)

# Nodo 1: Análisis de actividades
response = llm.invoke(prompt)  # Llama 3.2 analiza

# Nodo 3: Validación de descansos
response = llm.invoke(prompt)  # Llama 3.2 valida
```

---

## 📊 Validaciones

- ✅ **Aprobado**: Plan con descansos adecuados
- ⚠️ **Advertencia**: Pocas pausas con múltiples actividades
- ❌ **Rechazado**: Falta descanso tras clases/ejercicio/trabajo

---

## 🛠️ Requisitos del Sistema

- **Python**: 3.8+
- **RAM**: 8GB+ (para Llama 3.2)
- **Espacio**: ~5GB (modelo Llama 3.2)

---

## 📦 Archivos Incluidos

- `daily_planner_with_llama.py` - Código principal (177 líneas)
- `requirements.txt` - Dependencias
- `README.md` - Esta documentación

---

## 🎯 Características

✅ Análisis inteligente de actividades con Llama 3.2
✅ Validación automática de descansos
✅ Generación de plan personalizado
✅ Recomendaciones basadas en actividades
✅ Interfaz clara y fácil de usar
✅ LangGraph para arquitectura modular

---

## 📝 Notas

- El análisis tarda 15-20 segundos (debido a Llama 3.2 en CPU)
- Más rápido con GPU
- Requiere servidor Ollama ejecutándose en segundo plano
