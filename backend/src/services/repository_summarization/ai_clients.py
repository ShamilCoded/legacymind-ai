"""
AI Client Integrations

Provides adapters for different AI model providers (OpenAI, Anthropic, etc.)
"""

import os
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class AIClientBase(ABC):
    """Base class for AI client implementations."""
    
    @abstractmethod
    async def generate_async(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate text asynchronously."""
        pass
    
    @abstractmethod
    def generate_sync(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate text synchronously."""
        pass


class OpenAIClient(AIClientBase):
    """
    OpenAI API client adapter.
    
    Supports GPT-4, GPT-3.5-turbo, and other OpenAI models.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.
        """
        try:
            import openai
            self.openai = openai
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.async_client = openai.AsyncOpenAI(api_key=self.api_key)
    
    async def generate_async(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using OpenAI API asynchronously."""
        try:
            response = await self.async_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software architect and code analyst specializing in enterprise repository analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def generate_sync(
        self,
        prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using OpenAI API synchronously."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software architect and code analyst specializing in enterprise repository analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise


class AnthropicClient(AIClientBase):
    """
    Anthropic Claude API client adapter.
    
    Supports Claude 3 models (Opus, Sonnet, Haiku).
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Anthropic client.
        
        Args:
            api_key: Anthropic API key. If None, reads from ANTHROPIC_API_KEY env var.
        """
        try:
            import anthropic
            self.anthropic = anthropic
        except ImportError:
            raise ImportError(
                "Anthropic package not installed. Install with: pip install anthropic"
            )
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key not provided")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.async_client = anthropic.AsyncAnthropic(api_key=self.api_key)
    
    async def generate_async(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using Anthropic API asynchronously."""
        try:
            message = await self.async_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system="You are an expert software architect and code analyst specializing in enterprise repository analysis.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise
    
    def generate_sync(
        self,
        prompt: str,
        model: str = "claude-3-opus-20240229",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using Anthropic API synchronously."""
        try:
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system="You are an expert software architect and code analyst specializing in enterprise repository analysis.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise


class WatsonXClient(AIClientBase):
    """
    IBM WatsonX AI client adapter.
    
    Supports IBM's foundation models.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        url: Optional[str] = None
    ):
        """
        Initialize WatsonX client.
        
        Args:
            api_key: IBM Cloud API key
            project_id: WatsonX project ID
            url: WatsonX service URL
        """
        try:
            from ibm_watson_machine_learning.foundation_models import Model
            from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
            self.Model = Model
            self.GenParams = GenParams
        except ImportError:
            raise ImportError(
                "IBM Watson ML package not installed. Install with: pip install ibm-watson-machine-learning"
            )
        
        self.api_key = api_key or os.getenv("IBM_CLOUD_API_KEY")
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID")
        self.url = url or os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        
        if not self.api_key or not self.project_id:
            raise ValueError("IBM Cloud API key and WatsonX project ID required")
        
        self.credentials = {
            "url": self.url,
            "apikey": self.api_key
        }
    
    async def generate_async(
        self,
        prompt: str,
        model: str = "ibm/granite-13b-chat-v2",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using WatsonX API asynchronously."""
        # WatsonX SDK doesn't have native async support, use sync version
        return self.generate_sync(prompt, model, temperature, max_tokens)
    
    def generate_sync(
        self,
        prompt: str,
        model: str = "ibm/granite-13b-chat-v2",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> str:
        """Generate text using WatsonX API synchronously."""
        try:
            parameters = {
                self.GenParams.DECODING_METHOD: "greedy",
                self.GenParams.MAX_NEW_TOKENS: max_tokens,
                self.GenParams.TEMPERATURE: temperature,
                self.GenParams.STOP_SEQUENCES: ["Human:", "Assistant:"]
            }
            
            model_instance = self.Model(
                model_id=model,
                params=parameters,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            system_prompt = "You are an expert software architect and code analyst specializing in enterprise repository analysis."
            full_prompt = f"{system_prompt}\n\nHuman: {prompt}\n\nAssistant:"
            
            response = model_instance.generate_text(prompt=full_prompt)
            return response
        except Exception as e:
            logger.error(f"WatsonX API error: {str(e)}")
            raise


class AIClientFactory:
    """Factory for creating AI client instances."""
    
    @staticmethod
    def create_client(
        provider: str,
        **kwargs
    ) -> AIClientBase:
        """
        Create an AI client instance.
        
        Args:
            provider: Provider name ('openai', 'anthropic', 'watsonx')
            **kwargs: Provider-specific configuration
        
        Returns:
            AI client instance
        """
        provider = provider.lower()
        
        if provider == "openai":
            return OpenAIClient(api_key=kwargs.get("api_key"))
        elif provider == "anthropic":
            return AnthropicClient(api_key=kwargs.get("api_key"))
        elif provider == "watsonx":
            return WatsonXClient(
                api_key=kwargs.get("api_key"),
                project_id=kwargs.get("project_id"),
                url=kwargs.get("url")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    @staticmethod
    def create_from_env(provider: Optional[str] = None) -> AIClientBase:
        """
        Create AI client from environment variables.
        
        Args:
            provider: Provider name. If None, auto-detects from env vars.
        
        Returns:
            AI client instance
        """
        if provider is None:
            # Auto-detect provider from environment
            if os.getenv("OPENAI_API_KEY"):
                provider = "openai"
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
            elif os.getenv("IBM_CLOUD_API_KEY"):
                provider = "watsonx"
            else:
                raise ValueError("No AI provider credentials found in environment")
        
        return AIClientFactory.create_client(provider)

# Made with Bob
