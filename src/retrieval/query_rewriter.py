"""
query_rewriter.py

Rewrites follow-up questions into standalone questions
to improve retrieval quality.

Responsibilities:
- Read conversation history
- Rewrite ambiguous user queries
- Return a standalone query

This module does NOT:
- Retrieve documents
- Call Chroma
- Generate the final answer
"""

from langchain_core.messages import AIMessage, HumanMessage

from src.llm.llm_client import llm


REWRITE_PROMPT = """
You are an expert query rewriting assistant for a Retrieval-Augmented Generation (RAG) system.

Your task is to rewrite the user's latest question into a complete, standalone question.

Rules:
- Preserve the original intent.
- Resolve references like:
  - it
  - that
  - this
  - they
  - those
- Use the conversation history when necessary.
- Do NOT answer the question.
- Return ONLY the rewritten question.
- If the question is already standalone, return it unchanged.

Conversation History:
{history}

Latest User Question:
{question}

Rewritten Question:
"""


def rewrite_query(
    question: str,
    history: list,
) -> str:
    """
    Rewrite the user's question into a standalone query.

    Args:
        question: Latest user question.
        history: List of LangChain messages.

    Returns:
        Standalone rewritten query.
    """

    if not history:
        return question

    history_text = []

    for message in history:
        if isinstance(message, HumanMessage):
            history_text.append(f"User: {message.content}")

        elif isinstance(message, AIMessage):
            history_text.append(f"Assistant: {message.content}")

    prompt = REWRITE_PROMPT.format(
        history="\n".join(history_text),
        question=question,
    )

    response = llm.invoke(prompt)

    return response.content.strip()