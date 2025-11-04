# MCP Server + Cliente - Gestor de Gastos con Llama 3.2

Servidor MCP que extrae gastos de correos usando Llama 3.2. Incluye cliente Python para consumir el servidor.

## Requisitos

```bash
pip install requests
```

## Pasos de Uso

### 1. Inicia Ollama (Terminal 1)

```bash
ollama run llama2
```

### 2. Ejecuta el Cliente (Terminal 2)

```bash
python3 mcp_client.py
```

El cliente automáticamente:
- Inicia el servidor MCP
- Obtiene 5 correos simulados
- Extrae gastos con Llama 3.2 (via Ollama)
- Exporta a gastos.csv
- Muestra resumen de totales

## Salida Esperada

```
Iniciando cliente MCP...

📧 Obteniendo correos...
   ✓ 5 correos obtenidos

💰 Extrayendo gastos con Llama 3.2...
   ✓ 5 gastos extraídos
      1. 2025-10-29 | TOTTUS | 45.9 PEN
      2. 2025-10-29 | Desconocido | 12.0 USD
      3. 2025-10-28 | Desconocido | 9.5 PEN

📁 Exportando a CSV...
   ✓ Archivo: gastos.csv

📊 Resumen del día:
📊 RESUMEN (5 transacciones):
   PEN: 175.40
   USD: 20.50
Top 3:
   1. Desconocido: 141.50
   2. TOTTUS: 45.90
   3. SPOTIFY: 8.50
```

## Arquitectura

```
mcp_client.py
     ↓ (stdin/stdout)
mcp_server.py
     ↓ (HTTP POST)
Ollama (Llama 3.2)
```

El cliente se comunica con el servidor via stdin/stdout (protocolo MCP). El servidor consume Ollama para parsing inteligente.

## Archivos

- **mcp_server.py** — Servidor MCP (comunica via stdin/stdout)
- **mcp_client.py** — Cliente que consume el servidor MCP
- **gastos.csv** — Salida generada con los gastos

## Notas

- Requiere Ollama corriendo en http://localhost:11434
- Solo usa Llama 3.2 para parsing (sin fallback a regex)
- Separación clara: servidor y cliente en dos procesos independientes
