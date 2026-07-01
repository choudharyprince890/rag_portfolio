# src/ingestion/text_splitter.py
from typing import List
from langchain_core.documents import Document

def split_text_into_chunks(
    text: str, 
    chunk_size: int = 400, 
    chunk_overlap: int = 40
) -> List[Document]:
    """
    Splits text recursively based on natural document boundaries.
    
    Args:
        text (str): The cleaned document text.
        chunk_size (int): Maximum character length per chunk.
        chunk_overlap (int): Number of characters to overlap between chunks.
        
    Returns:
        List[Document]: A list of LangChain Documents ready for vectorization.
    """
    separators = ["\n\n", "\n", " "]
    chunks = []
    start_idx = 0
    
    while text:
        # Base case: remaining text fits in one chunk
        if len(text) <= chunk_size:
            chunks.append(
                Document(page_content=text, metadata={"start_index": start_idx})
            )
            break
            
        split_pos = -1
        
        # Find the best natural break point
        for sep in separators:
            pos = text[:chunk_size].rfind(sep)
            if pos > int(chunk_size * 0.3):
                split_pos = pos + len(sep)
                break
        
        # Fallback if no natural breaks are found
        if split_pos == -1:
            split_pos = chunk_size
            
        chunk_content = text[:split_pos].strip()
        if chunk_content:
            chunks.append(
                Document(page_content=chunk_content, metadata={"start_index": start_idx})
            )
        
        # Move forward, accounting for the overlap
        move_forward = max(1, split_pos - chunk_overlap)
        text = text[move_forward:]
        start_idx += move_forward

    return chunks