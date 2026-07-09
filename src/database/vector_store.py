
"""
vector_store.py

Handles all interactions with the Chroma vector database.

Responsibilities:
- Create a Chroma database
- Persist embeddings
- Load an existing database

This module does NOT know where the documents came from.
It only works with LangChain Document chunks.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.embeddings.embedding_model import embeddings_model


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

CHROMA_DB_PATH = Path("data/processed/chroma_db")
COLLECTION_NAME = "portfolio"


# ---------------------------------------------------------------------
# Create Vector Store
# ---------------------------------------------------------------------

def create_vector_store(chunks: list[Document]) -> Chroma:
    """
    Create a new Chroma vector store from document chunks.

    Args:
        chunks: List of LangChain Document chunks.

    Returns:
        Chroma vector store instance.
    """

    if not chunks:
        raise ValueError("No document chunks provided.")

    CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=str(CHROMA_DB_PATH),
        collection_name=COLLECTION_NAME,
    )

    return vector_store


# ---------------------------------------------------------------------
# Load Existing Vector Store
# ---------------------------------------------------------------------

def load_vector_store() -> Chroma:
    """
    Load an existing Chroma database.

    Returns:
        Chroma vector store instance.
    """

    if not CHROMA_DB_PATH.exists():
        raise FileNotFoundError(
            f"Vector database not found at: {CHROMA_DB_PATH}"
        )

    return Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings_model,
        collection_name=COLLECTION_NAME,
    )


# ---------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------

def vector_store_exists() -> bool:
    """
    Check whether a persisted Chroma database exists.

    Returns:
        True if the database directory exists.
    """

    return CHROMA_DB_PATH.exists()