"""
Offline ingestion script.

Run this script ONLY when your source documents change.

Flow:
    Resume PDF
        ↓
    About Me Markdown
        ↓
    Merge Documents
        ↓
    Preprocess
        ↓
    Split into Chunks
        ↓
    Generate Embeddings
        ↓
    Persist Chroma Database

Usage:
    python scripts/ingest.py
"""


from pathlib import Path
import shutil
import sys

# Allow imports from project root when running:
# python scripts/ingest.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from langchain_core.documents import Document

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.markdown_loader import load_markdown
from src.ingestion.preprocessor import clean_text
from src.ingestion.text_splitter import split_documents
from src.database.vector_store import create_vector_store


RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

PDF_PATH = RAW_DATA_DIR / "resume.pdf"
MARKDOWN_PATH = RAW_DATA_DIR / "about_me_2.md"

CHROMA_DB_PATH = PROJECT_ROOT / "data" / "processed" / "chroma_db"


def preprocess_documents(documents: list[Document]) -> list[Document]:
    """
    Apply lightweight preprocessing to each document.
    """

    cleaned_documents = []

    for doc in documents:
        cleaned_documents.append(
            Document(
                page_content=clean_text(doc.page_content),
                metadata=doc.metadata,
            )
        )

    return cleaned_documents


def main() -> None:

    print("=" * 60)
    print("Starting Offline Ingestion Pipeline")
    print("=" * 60)

    # ------------------------------------------------------------
    # Load documents
    # ------------------------------------------------------------

    print("\nLoading PDF...")
   #  pdf_docs = load_pdf(PDF_PATH)
    pdf_docs = ""

    print("Loading Markdown...")
    md_docs = load_markdown(MARKDOWN_PATH)

   #  documents = pdf_docs + md_docs
    documents = md_docs

    print(f"Loaded {len(documents)} document(s).")

    # ------------------------------------------------------------
    # Preprocess
    # ------------------------------------------------------------
   
    print("\nPreprocessing documents...")
    documents = preprocess_documents(documents)

    # ------------------------------------------------------------
    # Split
    # ------------------------------------------------------------

    print("Splitting into chunks...")
    chunks = split_documents(documents)

    print(f"Generated {len(chunks)} chunks.")

    # ------------------------------------------------------------
    # Remove old DB (optional but recommended)
    # ------------------------------------------------------------

    if CHROMA_DB_PATH.exists():
        print("\nRemoving existing Chroma database...")
        shutil.rmtree(CHROMA_DB_PATH)

    # ------------------------------------------------------------
    # Create vector database
    # ------------------------------------------------------------

    print("Creating Chroma database...")
    create_vector_store(chunks)

    print("\nIngestion completed successfully.")
    print(f"Vector database saved to:\n{CHROMA_DB_PATH}")


if __name__ == "__main__":
    main()




# python scripts/ingest.py