#!/usr/bin/env python3
"""Sistema RAG para consultar sílabos académicos"""

import sys
from pathlib import Path
from load_documents import cargar_e_indexar_documentos
from rag_system import inicializar_sistema_rag, consultar_rag
from config import DB_DIR

def main():
    """Ejecuta el sistema RAG"""

    # Verificar si la BD existe, si no, cargar documentos primero
    if not (DB_DIR / "chroma.sqlite3").exists():
        print("=" * 50)
        print("🔄 Inicializando base de datos...")
        print("=" * 50)
        cargar_e_indexar_documentos()
    else:
        print("✓ Usando base de datos existente")

    print("\n" + "=" * 50)
    print("🎓 ASISTENTE ACADÉMICO RAG")
    print("=" * 50)
    print("Escribe 'salir' para terminar\n")

    # Inicializar sistema RAG
    cadena_rag, recuperador = inicializar_sistema_rag()

    # Loop interactivo
    while True:
        try:
            pregunta = input("❓ Pregunta: ").strip()

            if pregunta.lower() in ["salir", "quit", "exit", "q"]:
                print("¡Hasta luego! 👋")
                break

            if not pregunta:
                continue

            # Pasar el recuperador para mostrar los chunks
            consultar_rag(cadena_rag, pregunta, recuperador)

        except KeyboardInterrupt:
            print("\n\n¡Hasta luego! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Asegúrate de que Ollama esté ejecutándose o configura OPENAI_API_KEY")

if __name__ == "__main__":
    main()
