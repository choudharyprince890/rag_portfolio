
"""
pdf_loader.py

Loads PDF documents and returns a list of LangChain Document objects.
"""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(pdf_path: str | Path) -> list[Document]:
    """
    Load a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of LangChain Document objects.

    Raises:
        FileNotFoundError: If the PDF does not exist.
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()

    return documents