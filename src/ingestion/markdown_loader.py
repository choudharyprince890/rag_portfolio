"""
markdown_loader.py

Loads Markdown files and returns a list of LangChain Document objects.
"""

from pathlib import Path

from langchain_core.documents import Document


def load_markdown(md_path: str | Path) -> list[Document]:
    """
    Load a Markdown file.

    Args:
        md_path: Path to the markdown file.

    Returns:
        List containing one LangChain Document.

    Raises:
        FileNotFoundError: If the markdown file does not exist.
    """

    md_path = Path(md_path)

    if not md_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {md_path}")

    with open(md_path, "r", encoding="utf-8") as file:
        text = file.read()

    document = Document(
        page_content=text,
        metadata={
            "source": str(md_path),
            "file_type": "markdown",
        },
    )

    return [document]