#!/usr/bin/env python3
"""
Cliente MCP - Consume el servidor MCP
Se comunica via stdin/stdout
"""
import json
import subprocess
import sys
import os
from typing import Any

class MCPClient:
    def __init__(self, server_path: str = "mcp_server.py"):
        self.process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def send_command(self, cmd: str, args: list = None) -> Any:
        if args is None:
            args = []

        payload = json.dumps({"cmd": cmd, "args": args})
        self.process.stdin.write(payload + "\n")
        self.process.stdin.flush()

        response_line = self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from server")

        response = json.loads(response_line.strip())
        if "error" in response:
            raise Exception(response["error"])
        return response.get("result")

    def fetch_emails(self, provider: str = "simulado") -> list[dict]:
        return self.send_command("fetch_emails", [provider])

    def extract_expenses(self, emails: list[dict]) -> list[dict]:
        return self.send_command("extract_expenses", [emails])

    def export_expenses(self, rows: list[dict], path: str = "gastos.csv") -> str:
        return self.send_command("export_expenses", [rows, path])

    def summary_today(self) -> str:
        return self.send_command("summary_today", [])

    def close(self):
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.terminate()

if __name__ == "__main__":
    print("Iniciando cliente MCP...")
    client = MCPClient()

    try:
        # 1. Obtener emails
        print("\n📧 Obteniendo correos...")
        emails = client.fetch_emails()
        print(f"   ✓ {len(emails)} correos obtenidos")

        # 2. Extraer gastos
        print("\n💰 Extrayendo gastos con Llama 3.2...")
        gastos = client.extract_expenses(emails)
        print(f"   ✓ {len(gastos)} gastos extraídos")

        if not gastos:
            print("\n⚠️  No se extrajeron gastos. Verifica que Ollama esté corriendo:")
            print("   Terminal 1: ollama run llama2")
            sys.exit(1)

        for i, g in enumerate(gastos[:3], 1):
            print(f"      {i}. {g['fecha']} | {g['comercio']} | {g['monto']} {g['moneda']}")

        # 3. Exportar
        print("\n📁 Exportando a CSV...")
        csv_path = client.export_expenses(gastos, "gastos.csv")
        print(f"   ✓ Archivo: {csv_path}")

        # Validar que el CSV se creó
        if os.path.exists(csv_path):
            with open(csv_path, 'r') as f:
                lines = f.readlines()
            print(f"   ✓ CSV verificado: {len(lines)-1} datos + 1 header")
            print(f"\n   Contenido del CSV:")
            for line in lines[:4]:  # Mostrar primeras 4 líneas
                print(f"   {line.strip()}")
        else:
            print(f"   ❌ CSV NO ENCONTRADO en {csv_path}")
            print(f"   Archivos en directorio: {os.listdir('.')}")

        # 4. Resumen
        print("\n📊 Resumen del día:")
        summary = client.summary_today()
        print(summary)

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        client.close()
