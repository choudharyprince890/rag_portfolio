import re

def clean_resume_text(text: str) -> str:
    """
    Cleans and normalizes extracted resume text for better chunking.
    
    Args:
        text (str): Raw text extracted from the PDF.
        
    Returns:
        str: Cleaned text with normalized bullets, spacing, and sections.
    """
    if not text:
        return ""

    # Standardize various PDF bullet points to a simple hyphen for consistency
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]', '-', text)
    
    # Compress multiple spaces or tabs into a single space to save tokens
    text = re.compile(r'[ \t]+').sub(' ', text)
    
    # Remove rogue spaces trapped around newline characters
    text = re.sub(r'\s*\n\s*', '\n', text)
    
    # Limit consecutive newlines to 2 (preserves major section breaks 
    # like 'Experience' vs 'Education' without wasting context window space)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Strip leading and trailing whitespace from the final document
    return text.strip()