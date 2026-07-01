# src/pipeline.py
import os
from typing import Generator
from langchain_groq import ChatGroq  # Native Groq import
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import the base retriever directly from your database module
from src.database.vector_store import get_retriever

# Initialize Groq at the module level
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Updated to the new supported model
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0,
    streaming=True
)

prompt = ChatPromptTemplate.from_template("""
You are the professional digital twin of Prince Choudhary, an AI and Robotics Engineer. 
Your goal is to enthusiastically and accurately represent Prince's skills, experience, and projects to hiring managers and technical recruiters.

Use the following retrieved context from his resume to answer the question. 
When discussing robotics, computer vision (like MOT or ReID algorithms), or Python development, speak with technical precision. 
If the context does not contain the answer, do not make up information—simply state that the provided resume doesn't cover that specific detail, but highlight a related skill if applicable.

Context: {context}

Question: {question}

Answer:
""")

def _format_docs(docs) -> str:
    """Helper to join retrieved documents into a single string."""
    return "\n\n".join(doc.page_content for doc in docs)

def answer_query_stream(question: str) -> Generator[str, None, None]:
    """
    Executes the LCEL chain and yields tokens as they arrive from Groq.
    """
    # Fetch 3 chunks directly from the vector store (No reranker model needed)
    retriever = get_retriever(top_k=3)
    
    rag_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    for chunk in rag_chain.stream(question):
        yield chunk