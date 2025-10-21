# Daily Planner Agent - Setup con OpenAI

## Pre-requisitos

Debes tener una API key de OpenAI.

### Obtener API key

1. Ve a https://platform.openai.com/api-keys
2. Crea una nueva API key
3. Cópiala en un lugar seguro

## Instalación

```bash
pip install -r requirements_planner.txt
```

## Configuración

### Establecer API key de OpenAI

```bash
# macOS / Linux
export OPENAI_API_KEY='tu-clave-api-aqui'

# Windows (PowerShell)
$env:OPENAI_API_KEY='tu-clave-api-aqui'
```

O crear un archivo `.env`:

```
OPENAI_API_KEY=tu-clave-api-aqui
```

## Ejecución

```bash
python3 daily_planner_agent.py
```

El script:
1. Pide tu objetivo del día
2. Usa OpenAI API para generar el plan con ReAct
3. Guarda el resultado en `plan_YYYYMMDD_HHMMSS.txt`

## Archivos

- `daily_planner_agent.py` - Agente ReAct (182 líneas)
- `calendar_data.json` - Eventos
- `projects_data.json` - Proyectos
- `requirements_planner.txt` - Dependencias

## Modelo utilizado

- **gpt-4o-mini** - Rápido y económico (recomendado)
- Temperatura: 0.2 (respuestas consistentes)
- Max tokens: 2048
