"""
hallucination.py

Checks whether the generated answer is supported by
the retrieved context.
"""

from src.llm.llm_client import generate_response

PROMPT = """
You are a hallucination detection assistant.

Determine whether the generated answer is completely supported
by the retrieved context.

Rules:

- If every factual statement is supported,
  respond ONLY with:

SUPPORTED

- Otherwise respond ONLY with:

NOT_SUPPORTED

Retrieved Context:
{context}

Generated Answer:
{answer}

Result:
"""


def is_grounded(
    context: str,
    answer: str,
) -> bool:
    """
    Returns True if the answer is grounded in the context.
    """

    prompt = PROMPT.format(
        context=context,
        answer=answer,
    )

    result = generate_response(prompt)

    return result.strip().upper() == "SUPPORTED"