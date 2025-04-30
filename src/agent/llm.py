"""
A model integrator for any LLM model.
"""

from langchain_groq import ChatGroq
from setting import env
from langchain_core.language_models import BaseChatModel

class LLM:
    """
    A model integrator for any LLM model.
    """

    @classmethod
    def groq(cls, model_name: str = None, api_key: str = None) -> BaseChatModel:
        """
        Initialize the Groq model.
        """
        if model_name is None:
            model_name = env.GROQ_QWEN_2_5_32_B_MODEL_NAME
        if api_key is None:
            api_key = env.GROQ_API_KEY
        return ChatGroq(
            model_name=model_name,
            temperature=env.GROQ_TEMPERATURE,
            api_key=api_key,
        )