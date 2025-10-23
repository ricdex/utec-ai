.PHONY: help install run clean

help:
	@echo "🎓 Asistente Académico RAG"
	@echo "============================"
	@echo ""
	@echo "make install    - Instalar dependencias de Python"
	@echo "make run        - Ejecutar el asistente RAG"
	@echo "make clean      - Limpiar base de datos y caché"
	@echo ""
	@echo "Configuración inicial:"
	@echo "  1. make install"
	@echo "  2. Opción A - Ollama (recomendado, sin API key):"
	@echo "     ollama pull llama2"
	@echo "     ollama serve  # En otra terminal"
	@echo "  3. Opción B - OpenAI API:"
	@echo "     export OPENAI_API_KEY='sk-...'"
	@echo "  4. make run"
	@echo ""

install:
	python3 -m pip install -r requirements.txt

run:
	python3 main.py

clean:
	rm -rf chroma_db
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
