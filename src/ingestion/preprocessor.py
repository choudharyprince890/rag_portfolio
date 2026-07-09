

"""
preprocessor.py

Basic text preprocessing utilities.

Responsibilities:
- Remove unnecessary whitespace
- Remove extra blank lines
- Normalize line endings

This module intentionally performs only lightweight cleaning to
preserve the semantic meaning of the original text.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean and normalize text.

    Operations:
    - Normalize line endings
    - Remove trailing spaces
    - Collapse multiple blank lines
    - Collapse repeated spaces/tabs
    - Strip leading/trailing whitespace

    Args:
        text: Raw input text.

    Returns:
        Cleaned text.
    """

    if not text:
        return ""

    # Normalize Windows/Mac line endings to Unix
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove trailing spaces at the end of each line
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse 3+ blank lines into a maximum of 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    return text.strip()