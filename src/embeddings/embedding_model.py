"""
embedding_model.py

This module initializes the embedding model once and exposes a
single shared instance that can be imported throughout the project.

Example:
    from src.embeddings.embedding_model import embeddings_model
"""

from langchain_huggingface import HuggingFaceEmbeddings


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

EMBEDDING_MODEL_NAME = "BAAI/bge-base-en-v1.5"


# -----------------------------------------------------------------------------
# Load Embedding Model (Only Once)
# -----------------------------------------------------------------------------

print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}...")

embeddings_model = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={
        "device": "cpu",  # Change to "cuda" if GPU is available
    },
    encode_kwargs={
        "normalize_embeddings": True,
    },
)

print("Embedding model loaded successfully.")