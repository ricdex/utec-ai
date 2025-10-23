from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from config import (
    SILABUS_DIR, DB_DIR, NOMBRE_COLECCION, TAMAÑO_CHUNK, OVERLAP_CHUNK,
    USAR_OLLAMA, MODELO_OLLAMA, OPENAI_API_KEY, MODELO_OPENAI
)

def obtener_embeddings():
    """Obtiene el modelo de embeddings según la configuración"""
    if USAR_OLLAMA:
        print(f"Usando embeddings de Ollama: {MODELO_OLLAMA}")
        return OllamaEmbeddings(model=MODELO_OLLAMA)
    else:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada. Configúrala en .env o usa Ollama")
        print(f"Usando embeddings de OpenAI: {MODELO_OPENAI}")
        return OpenAIEmbeddings(api_key=OPENAI_API_KEY)

def chunking_estructurado(documentos):
    """
    Chunking inteligente que respeta la estructura de sílabos académicos.

    En lugar de dividir solo por caracteres, respeta las secciones naturales:
    - Datos generales (I.)
    - Evaluación (VI.)
    - Contenido programado (VII.)
    - Bibliografía (VIII.)
    """
    print("Aplicando chunking estructurado basado en secciones del documento...")

    fragmentos = []

    for doc in documentos:
        contenido = doc.page_content
        metadata = doc.metadata

        # Dividir por secciones principales del sílabo (Roman numerals)
        # Patrón: "I.", "II.", "III.", etc.
        import re

        # Separadores de sección: "Roman numeral. Section name"
        patron_seccion = r'(?=\n[IVX]+\.\s)'
        secciones = re.split(patron_seccion, contenido)

        for seccion in secciones:
            if len(seccion.strip()) < 50:
                # Ignorar fragmentos muy pequeños
                continue

            # Para secciones muy largas (>3000 caracteres), dividirlas más
            if len(seccion) > 3000:
                # Dividir subsecciones (por temas numerados como "1.", "2.", etc.)
                patron_subseccion = r'(?=\n\d+[\.\)]\s)'
                subsecciones = re.split(patron_subseccion, seccion)

                for subseccion in subsecciones:
                    if len(subseccion.strip()) > 50:
                        fragmentos.append({
                            'page_content': subseccion.strip(),
                            'metadata': metadata
                        })
            else:
                fragmentos.append({
                    'page_content': seccion.strip(),
                    'metadata': metadata
                })

    # Convertir a formato compatible con LangChain
    from langchain_core.documents import Document

    docs_procesados = [
        Document(page_content=f['page_content'], metadata=f['metadata'])
        for f in fragmentos
    ]

    print(f"Se crearon {len(docs_procesados)} fragmentos estructurados")
    return docs_procesados

def cargar_e_indexar_documentos():
    """Carga PDFs de sílabos e indexa en Chroma"""
    print(f"Cargando PDFs desde {SILABUS_DIR}...")

    # Cargar todos los PDFs de la carpeta sílabos
    loader = PyPDFDirectoryLoader(str(SILABUS_DIR))
    documentos = loader.load()
    print(f"Se cargaron {len(documentos)} páginas de PDFs")

    # Usar chunking estructurado en lugar del genérico
    print("Dividiendo documentos en fragmentos con estrategia estructurada...")
    fragmentos = chunking_estructurado(documentos)
    print(f"Se crearon {len(fragmentos)} fragmentos")

    # Crear embeddings
    print("Generando embeddings...")
    embeddings = obtener_embeddings()

    # Crear e indexar en Chroma
    print("Indexando fragmentos en Chroma...")
    vectorstore = Chroma.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        collection_name=NOMBRE_COLECCION,
        persist_directory=str(DB_DIR)
    )

    print(f"✓ Documentos indexados correctamente. BD guardada en {DB_DIR}")
    return vectorstore

if __name__ == "__main__":
    cargar_e_indexar_documentos()
