"""
conversation_memory.py

Stores recent conversation history for the chatbot.

Responsibilities:
- Store user and assistant messages
- Return recent conversation history
- Clear conversation history

This module does NOT know about:
- Retrieval
- LLM
- Prompt templates
"""

from collections import deque


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

MAX_HISTORY = 4


# ---------------------------------------------------------------------
# Conversation Memory
# ---------------------------------------------------------------------

class ConversationMemory:
    """
    Stores the most recent conversation messages.
    """

    def __init__(self, max_history: int = MAX_HISTORY):
        self._messages = deque(maxlen=max_history)

    def add_user_message(self, message: str) -> None:
        """
        Add a user message.
        """
        self._messages.append(
            {
                "role": "user",
                "content": message,
            }
        )

    def add_assistant_message(self, message: str) -> None:
        """
        Add an assistant message.
        """
        self._messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

   #  def get_history(self) -> str:
   #      """
   #      Returns the conversation formatted for the prompt.
   #      """

   #      if not self._messages:
   #          return ""

   #      history = []

   #      for msg in self._messages:
   #          role = "User" if msg["role"] == "user" else "Assistant"
   #          history.append(f"{role}: {msg['content']}")

   #      return "\n".join(history)

    def get_messages(self):
        return list(self._messages)

    def clear(self) -> None:
        """
        Clear all conversation history.
        """
        self._messages.clear()


# ---------------------------------------------------------------------
# Shared Memory Instance
# ---------------------------------------------------------------------

conversation_memory = ConversationMemory()