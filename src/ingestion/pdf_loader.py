from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts raw text from a PDF binary stream.
    
    Args:
        file_bytes (bytes): The raw bytes of the uploaded PDF file.
        
    Returns:
        str: The concatenated text from all pages of the PDF.
    """
    # Load the binary stream into a file-like object for pypdf
    pdf_file = BytesIO(file_bytes)
    reader = PdfReader(pdf_file)
    
    # Iterate through all pages, extract text, and join with no delimiter
    # (Fallback to empty string if extract_text() returns None)
    return "".join(
        page.extract_text() or "" for page in reader.pages
    )