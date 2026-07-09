

"""
pipeline.py

Simple Retrieval-Augmented Generation (RAG) pipeline.

Flow:
    User Question
            ↓
      Retrieve Documents
            ↓
      Build Prompt
            ↓
        Groq LLM
            ↓
          Answer
"""

from src.llm.llm_client import generate_response
from src.retrieval.retriever import retrieve_documents
from src.memory import conversation_memory
from src.guardrails import (is_safe,is_grounded,)

# ---------------------------------------------------------------------
# Prompt Template
# ---------------------------------------------------------------------

# SYSTEM_PROMPT = """
# You are Prince Choudhary's AI Portfolio Assistant.

# Answer ONLY using the provided context.

# Guidelines:
# - If the answer is present in the context, answer naturally.
# - Do not make up information.
# - If the information is unavailable, politely say you don't know.
# - Keep responses concise and professional.

# Context:
# {context}

# Question:
# {question}

# Answer:
# """



SYSTEM_PROMPT = """
You are Prince Choudhary's AI Portfolio Assistant.

Use the previous conversation whenever it helps answer follow-up questions.

Rules:
- Answer ONLY using the provided context.
- Use the conversation history for references like:
    "that project"
    "it"
    "those skills"
- Never invent information.
- If the answer is not in the context, say you don't know.

Conversation History:
{history}

Context:
{context}

Question:
{question}

Answer:
"""



# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------

def _build_context(documents) -> str:
    """
    Combine retrieved documents into a single context string.
    """

    return "\n\n".join(doc.page_content for doc in documents)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------

# def ask(question: str, k: int = 5) -> str:
#     """
#     Execute the complete RAG pipeline.

#     Args:
#         question: User's question.
#         k: Number of chunks to retrieve.

#     Returns:
#         LLM-generated answer.
#     """

#     if not question.strip():
#         return "Please enter a question."

#     # Step 1: Retrieve relevant documents
#     documents = retrieve_documents(question, k=k)

#     # Step 2: Build context
#     context = _build_context(documents)

#     # Step 3: Build prompt
#     prompt = SYSTEM_PROMPT.format(
#         context=context,
#         question=question,
#     )

#     # Step 4: Generate answer
#     answer = generate_response(prompt)

#     return answer


def ask(question: str, k: int = 5) -> str:
    """
    Execute the complete RAG pipeline.
    """

    if not question.strip():
        return "Please enter a question."
    

    # -------------------------------
    # Prompt Injection Guard
    # -------------------------------
    if not is_safe(question):
        return (
            "I'm sorry, but I can't process requests that attempt "
            "to manipulate my instructions."
        )

    # --------------------------------------------------
    # Save user message
    # --------------------------------------------------

    conversation_memory.add_user_message(question)


    # --------------------------------------------------
    # Get recent chat history
    # --------------------------------------------------

    history = conversation_memory.get_messages()


    # --------------------------------------------------
    # rerwrite the query
    # --------------------------------------------------

    # rewritten_query = rewrite_query(question, history)

    # --------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------

    # documents = retrieve_documents(rewritten_query, k=k)

    documents = retrieve_documents(question, k=k)

    context = _build_context(documents)



    # --------------------------------------------------
    # Build prompt
    # --------------------------------------------------

    prompt = SYSTEM_PROMPT.format(
        history=history,
        context=context,
        question=question,
    )

    # --------------------------------------------------
    # Generate answer
    # --------------------------------------------------

    # answer = generate_response(prompt)

    # # --------------------------------------------------
    # # Save assistant reply
    # # --------------------------------------------------

    # conversation_memory.add_assistant_message(answer)

    # return answer

    answer = generate_response(prompt)

    # -------------------------------
    # Hallucination Guard
    # -------------------------------
    if not is_grounded(context, answer):
        answer = (
            "I couldn't verify this information from my knowledge base."
        )

    conversation_memory.add_assistant_message(answer)

    return answer