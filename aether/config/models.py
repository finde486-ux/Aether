import os
from typing import Optional, Any
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_ollama import ChatOllama
try:
    from langchain_community.chat_models import MiniMaxChat
except ImportError:
    # Handle older community package versions
    from langchain_community.chat_models.minimax import MiniMaxChat

class ModelFactory:
    @staticmethod
    def get_model(provider: Optional[str] = None, model_name: Optional[str] = None) -> Any:
        """Factory to initialize a chat model from various providers."""
        provider = provider or os.getenv("AETHER_PROVIDER", "google")

        if provider == "openai":
            return ChatOpenAI(
                model=model_name or os.getenv("OPENAI_MODEL", "gpt-4o"),
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model_name or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"),
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        elif provider == "google":
            return ChatGoogleGenerativeAI(
                model=model_name or os.getenv("GOOGLE_MODEL", "gemini-2.0-flash"),
                google_api_key=os.getenv("GOOGLE_API_KEY")
            )
        elif provider == "mistral":
            return ChatMistralAI(
                model=model_name or os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
                api_key=os.getenv("MISTRAL_API_KEY")
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model_name or os.getenv("OLLAMA_MODEL", "llama3.1"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        elif provider == "minimax":
            return MiniMaxChat(
                model=model_name or os.getenv("MINIMAX_MODEL", "minimax-abab6.5-chat"),
                minimax_api_key=os.getenv("MINIMAX_API_KEY"),
                minimax_group_id=os.getenv("MINIMAX_GROUP_ID")
            )
        elif provider == "nvidia" or provider == "glm":
            # These usually follow OpenAI compatible API format
            base_url = os.getenv(f"{provider.upper()}_BASE_URL")
            return ChatOpenAI(
                model=model_name or os.getenv(f"{provider.upper()}_MODEL"),
                openai_api_key=os.getenv(f"{provider.upper()}_API_KEY"),
                openai_api_base=base_url
            )

        raise ValueError(f"Unsupported provider: {provider}")
