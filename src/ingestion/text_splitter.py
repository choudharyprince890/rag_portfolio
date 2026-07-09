
"""
text_splitter.py

Splits LangChain Document objects into smaller chunks for embedding.

Responsibilities:
- Split documents into chunks
- Add configurable overlap
- Return chunked Document objects
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# ---------------------------------------------------------------------
# Initialize splitter once
# ---------------------------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ],
)


# ---------------------------------------------------------------------
# Public Function
# ---------------------------------------------------------------------

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split LangChain documents into overlapping chunks.

    Args:
        documents: List of LangChain Document objects.

    Returns:
        List of chunked Document objects.
    """

    if not documents:
        return []

    chunks = text_splitter.split_documents(documents)

    return chunks