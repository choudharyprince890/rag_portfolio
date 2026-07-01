# src/database/vector_store.py
import os
from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "data/processed/chroma_db"

# Initialize the embedding model ONCE at the module level
print("Loading Base Embedding Model into memory...")
embeddings_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={'device': 'cpu'}, 
    encode_kwargs={'normalize_embeddings': True} 
)

def get_embeddings_model():
    # Return the already-loaded model
    return embeddings_model

def save_chunks_to_db(chunks: List[Document]) -> None:
    os.makedirs(os.path.dirname(DB_DIR), exist_ok=True)
    Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings_model(),
        persist_directory=DB_DIR
    )
    print(f"Successfully saved {len(chunks)} chunks to {DB_DIR}")

def get_retriever(top_k: int = 3):
    if not os.path.exists(DB_DIR):
        raise FileNotFoundError(
            f"Database not found at {DB_DIR}. Please run the ingestion pipeline first."
        )

    db = Chroma(
        persist_directory=DB_DIR,
        embedding_function=get_embeddings_model()
    )

    dynamic_fetch_k = top_k * 3 

    retriever = db.as_retriever(
        search_type="mmr", 
        search_kwargs={
            "k": top_k,
            "fetch_k": dynamic_fetch_k
        }
    )
    
    return retriever