# src/retrieval/reranker.py
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from src.database.vector_store import get_retriever

# 1. Initialize the model ONCE at the module level
print("Loading Cross-Encoder Model into memory...")
cross_encoder_model = HuggingFaceCrossEncoder(
    model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", 
    model_kwargs={'device': 'cpu'} 
)

def get_reranked_retriever(base_k: int = 15, final_k: int = 3):
    """
    Creates a two-stage retrieval pipeline.
    """
    base_retriever = get_retriever(top_k=base_k)
    
    # Use the globally loaded model instead of initializing a new one
    reranker = CrossEncoderReranker(model=cross_encoder_model, top_n=final_k)
    
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker,
        base_retriever=base_retriever
    )
    
    return compression_retriever