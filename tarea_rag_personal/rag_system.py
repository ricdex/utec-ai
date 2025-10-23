from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from config import (
    DB_DIR, NOMBRE_COLECCION,
    USAR_OLLAMA, MODELO_OLLAMA, OPENAI_API_KEY, MODELO_OPENAI
)
import re
from typing import List

# Plantilla de prompt del asistente académico
PROMPT_ACADEMICO = """Eres un asistente académico experto. Tu ÚNICA fuente de información es el contexto de sílabos proporcionado abajo.

INSTRUCCIONES CRÍTICAS:
1. LEE CUIDADOSAMENTE el contexto (secciones de sílabos reales)
2. BUSCA información sobre el curso/tema solicitado
3. EXTRAE directamente del contexto:
   - Nombre exacto del curso
   - Ciclo académico (nivel básico, intermedio, avanzado)
   - Datos generales (créditos, horas, prerequisitos)
   - Descripción y objetivos del curso
   - Resultados de aprendizaje
   - Metodología
   - Sistema de evaluación y fórmula del promedio final
   - Contenido programado por semanas
   - Bibliografía (básica y complementaria)

4. Si el usuario pregunta por un curso ESPECÍFICO:
   - Busca el nombre del curso en el contexto
   - Extrae TODOS los detalles disponibles
   - Cita la fuente (nombre del sílabo)

5. RESPONDE SIEMPRE basándote en el contexto:
   - NO inventes información
   - SI no está en el contexto, dilo explícitamente
   - CITA las fuentes (nombre del sílabo de origen)

6. Formato de respuesta:
   - Claro y estructurado
   - Usa secciones (Datos generales, Evaluación, Contenido, etc.)
   - Incluye la fuente (sílabo)

CONTEXTO DE LOS SÍLABOS (información verificada):
─────────────────────────────────────────────────
{context}
─────────────────────────────────────────────────

PREGUNTA DEL USUARIO:
─────────────────────────────────────────────────
{question}
─────────────────────────────────────────────────

RESPUESTA (basada ÚNICAMENTE en el contexto anterior):
─────────────────────────────────────────────────"""

class RecuperadorHibrido(BaseRetriever):
    """Recuperador híbrido que combina búsqueda semántica con coincidencia de palabras clave.

    Mejora la recuperación priorizando chunks que contienen el nombre exacto del curso
    buscado, combinado con la similitud semántica.
    """

    vectorstore_retriever: BaseRetriever
    vectorstore: Chroma

    class Config:
        arbitrary_types_allowed = True

    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae palabras clave significativas del texto"""
        # Convertir a minúsculas
        text = text.lower()
        # Eliminar caracteres especiales pero mantener espacios
        text = re.sub(r'[^a-záéíóúñ\s]', ' ', text)
        # Dividir en palabras
        palabras = text.split()
        # Filtrar palabras cortas (menos de 3 caracteres)
        return [p for p in palabras if len(p) >= 3]

    def _score_keyword_match(self, chunk_content: str, keywords: List[str]) -> tuple:
        """Calcula puntuación de coincidencia de palabras clave y detecta nombres de cursos.

        Retorna (puntuación_general, tiene_nombre_curso_especifico)
        """
        if not keywords:
            return (0.0, False)

        chunk_lower = chunk_content.lower()
        matches = sum(1 for kw in keywords if kw in chunk_lower)

        # Detectar si hay múltiples palabras clave consecutivas (posible nombre de curso)
        # Ej: "investigación operativa" tiene ambas palabras
        keywords_muy_especificos = ["investigación", "operativa", "ética", "deontología",
                                     "redes", "comunicaciones", "gestión", "calidad"]

        tiene_nombre_curso = any(
            kw in chunk_lower for kw in keywords
            if kw in keywords_muy_especificos
        )

        score = matches / len(keywords) if len(keywords) > 0 else 0.0
        return (score, tiene_nombre_curso)

    def _get_relevant_docs(self, query: str, k: int = 10) -> List[Document]:
        """Recupera y re-ordena documentos combinando semántica con palabras clave"""
        # Obtener documentos por similitud semántica (k+5 para tener más opciones)
        docs_semanticos = self.vectorstore_retriever.invoke(query)

        # Extraer palabras clave de la consulta
        keywords = self._extract_keywords(query)

        # Si no hay palabras clave significativas, devolver resultados semánticos
        if not keywords:
            return docs_semanticos[:k]

        # Re-ordenar documentos priorizando:
        # 1. Coincidencia de nombres de cursos específicos (boost alto)
        # 2. Similitud semántica
        # 3. Coincidencia de palabras clave generales
        docs_scored = []
        for i, doc in enumerate(docs_semanticos):
            keyword_score, tiene_nombre = self._score_keyword_match(doc.page_content, keywords)

            # Scoring estratégico:
            # - Si tiene nombre de curso específico: boost muy alto
            # - Si no, usar posición semántica como base
            if tiene_nombre:
                # Nombre de curso encontrado: dar máxima prioridad
                score = 1000.0 + keyword_score  # Boost masivo para nombres de curso
            else:
                # Puntuación basada en posición semántica + palabras clave
                score = (1.0 / (i + 1)) + (keyword_score * 0.5)

            docs_scored.append((doc, score))

        # Ordenar por puntuación combinada
        docs_scored.sort(key=lambda x: x[1], reverse=True)

        # Retornar solo los documentos (sin las puntuaciones)
        return [doc for doc, _ in docs_scored[:k]]

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        """Versión asíncrona de obtener documentos relevantes"""
        return self._get_relevant_docs(query)

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """Obtiene documentos relevantes usando búsqueda híbrida"""
        return self._get_relevant_docs(query)

def obtener_embeddings():
    """Obtiene el modelo de embeddings según la configuración"""
    if USAR_OLLAMA:
        return OllamaEmbeddings(model=MODELO_OLLAMA)
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada. Configúrala en .env o usa Ollama")
        return OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def inicializar_sistema_rag():
    """Inicializa el sistema RAG con Chroma y LLM"""

    # Cargar embeddings
    print("Cargando embeddings...")
    embeddings = obtener_embeddings()

    # Cargar base de datos Chroma
    print("Cargando base de datos Chroma...")
    vectorstore = Chroma(
        collection_name=NOMBRE_COLECCION,
        embedding_function=embeddings,
        persist_directory=str(DB_DIR)
    )

    # Crear recuperador semántico base
    recuperador_semantico = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 15}  # Aumentado a 15 para dar más opciones al recuperador híbrido
    )

    # Crear recuperador híbrido que combina semántica + palabras clave
    print("Usando recuperador híbrido (semántica + palabras clave)...")
    recuperador = RecuperadorHibrido(
        vectorstore_retriever=recuperador_semantico,
        vectorstore=vectorstore
    )

    # Inicializar LLM
    print("Inicializando modelo de lenguaje...")
    if USAR_OLLAMA:
        llm = ChatOllama(model=MODELO_OLLAMA, temperature=0.3)
        print(f"Usando Ollama con modelo: {MODELO_OLLAMA}")
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada. Configúrala en .env o usa Ollama")
        llm = ChatOpenAI(model=MODELO_OPENAI, temperature=0.3, api_key=OPENAI_API_KEY)
        print(f"Usando OpenAI con modelo: {MODELO_OPENAI}")

    # Crear plantilla de prompt
    prompt = PromptTemplate(
        template=PROMPT_ACADEMICO,
        input_variables=["context", "question"]
    )

    # Crear cadena RAG
    cadena_rag = (
        {
            "context": recuperador | (lambda docs: "\n\n".join([doc.page_content for doc in docs])),
            "question": lambda x: x
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return cadena_rag, recuperador

def consultar_rag(cadena_rag, pregunta: str, recuperador=None):
    """Consulta el sistema RAG y muestra los chunks utilizados"""
    print(f"\n📚 Pregunta: {pregunta}\n")

    # Mostrar chunks recuperados si se proporciona el recuperador
    if recuperador:
        print("=" * 80)
        print("📖 CHUNKS RECUPERADOS DE LA BASE DE DATOS")
        print("=" * 80)

        documentos_recuperados = recuperador.invoke(pregunta)

        for i, doc in enumerate(documentos_recuperados, 1):
            # Obtener información del documento
            fuente = doc.metadata.get('source', 'Desconocida')
            nombre_archivo = fuente.split('/')[-1] if '/' in fuente else fuente

            print(f"\n[CHUNK {i}] Fuente: {nombre_archivo}")
            print("-" * 80)
            print(f"Contenido:\n{doc.page_content}")
            print("-" * 80)

        print("\n" + "=" * 80)
        print("🤖 RESPUESTA GENERADA")
        print("=" * 80 + "\n")

    # Generar respuesta
    respuesta = cadena_rag.invoke(pregunta)
    print(f"{respuesta}\n")

    return respuesta
