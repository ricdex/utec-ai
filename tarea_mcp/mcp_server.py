#!/usr/bin/env python3
"""
MCP Server via stdio - Gestor de Gastos con Llama 3.2
"""
import csv
import json
import re
import sys
import requests
from typing import Optional

EMAILS = [
    {"de": "alertas@bcp.com.pe", "cuerpo": "BCP: Compra aprobada S/ 45.90 en TOTTUS 2025-10-29", "fecha": "2025-10-29"},
    {"de": "alertas@visa.com", "cuerpo": "VISA: USD 12.00 – NETFLIX.COM – 2025-10-29", "fecha": "2025-10-29"},
    {"de": "alertas@mastercard.pe", "cuerpo": "Mastercard: S/. 9.5 UBER TRIP 2025/10/28", "fecha": "2025-10-28"},
    {"de": "alertas@interbank.com.pe", "cuerpo": "Interbank: Compra S/120.00 MERCADO PAGO 28-10-2025", "fecha": "2025-10-28"},
    {"de": "alertas@visa.com", "cuerpo": "VISA: USD 8.5 en SPOTIFY 2025-10-29", "fecha": "2025-10-29"},
]

def parse_with_llama(text: str) -> dict:
    prompt = f"""Extrae del siguiente texto de email:
- fecha (YYYY-MM-DD)
- comercio (nombre del lugar)
- monto (número)
- moneda (PEN o USD)

Email: {text}

Responde en JSON: {{"fecha": "...", "comercio": "...", "monto": 0.0, "moneda": "..."}}"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False},
        timeout=10
    )
    result = response.json()
    text_response = result.get("response", "").strip()
    json_match = re.search(r'\{.*\}', text_response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    raise ValueError("No se pudo extraer JSON")

def fetch_emails(provider: str = "simulado") -> list[dict]:
    return EMAILS

def extract_expenses(emails: list[dict]) -> list[dict]:
    gastos = []
    errors = []
    for email in emails:
        try:
            data = parse_with_llama(email["cuerpo"])
            data["fuente"] = email["de"].split("@")[0].upper()
            gastos.append(data)
        except Exception as e:
            errors.append(str(e))
            print(f"Error procesando email: {e}", file=sys.stderr)
            continue

    if errors and not gastos:
        raise RuntimeError(f"Ollama no disponible. Asegúrate de ejecutar: ollama run llama2\nError: {errors[0]}")

    return gastos

def export_expenses(rows: list[dict], path: str = "gastos.csv") -> str:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["fecha", "comercio", "monto", "moneda", "fuente"])
        writer.writeheader()
        if rows:
            writer.writerows(rows)
    print(f"CSV creado: {path} ({len(rows)} filas)", file=sys.stderr)
    return path

def summary_today() -> str:
    emails = fetch_emails()
    gastos = extract_expenses(emails)

    if not gastos:
        return "No hay gastos."

    totales = {}
    comercios = {}
    for g in gastos:
        totales[g["moneda"]] = totales.get(g["moneda"], 0) + g["monto"]
        comercios[g["comercio"]] = comercios.get(g["comercio"], 0) + g["monto"]

    top3 = sorted(comercios.items(), key=lambda x: x[1], reverse=True)[:3]

    res = f"📊 RESUMEN ({len(gastos)} transacciones):\n"
    for moneda, total in totales.items():
        res += f"   {moneda}: {total:.2f}\n"
    res += "Top 3:\n"
    for i, (comercio, monto) in enumerate(top3, 1):
        res += f"   {i}. {comercio}: {monto:.2f}\n"
    return res

def process_command(cmd: str, args: list) -> str:
    try:
        if cmd == "fetch_emails":
            result = fetch_emails(*args)
        elif cmd == "extract_expenses":
            result = extract_expenses(*args)
        elif cmd == "export_expenses":
            result = export_expenses(*args)
        elif cmd == "summary_today":
            result = summary_today()
        else:
            return json.dumps({"error": f"Unknown command: {cmd}"})
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            data = json.loads(line.strip())
            cmd = data.get("cmd")
            args = data.get("args", [])
            response = process_command(cmd, args)
            sys.stdout.write(response + "\n")
            sys.stdout.flush()
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({"error": "Invalid JSON"}) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()
