"""
retriever.py

Handles document retrieval from the Chroma vector database.

Responsibilities:
- Load the persisted Chroma database
- Perform similarity search
- Return the top-k relevant document chunks

This module does NOT know about:
- LLMs
- Prompts
- Reranking
- Conversation Memory
- Guardrails
"""

from langchain_core.documents import Document

from src.database.vector_store import load_vector_store


# ---------------------------------------------------------------------
# Default Configuration
# ---------------------------------------------------------------------

DEFAULT_TOP_K = 5


# ---------------------------------------------------------------------
# Initialize Vector Store Once
# ---------------------------------------------------------------------

vector_store = load_vector_store()


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

def retrieve_documents(
    query: str,
    k: int = DEFAULT_TOP_K,
) -> list[Document]:
    """
    Retrieve the most relevant document chunks.

    Args:
        query: User query.
        k: Number of chunks to retrieve.

    Returns:
        List of LangChain Document objects.
    """

    if not query.strip():
        return []

    documents = vector_store.similarity_search(
        query=query,
        k=k,
    )

    return documents