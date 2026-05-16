"""
Configuration for Repository Summarization Service
"""

import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class AIProviderConfig:
    """Configuration for AI provider."""
    
    provider: str = "openai"  # openai, anthropic, watsonx
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 4000
    
    # Provider-specific settings
    project_id: Optional[str] = None  # For WatsonX
    url: Optional[str] = None  # For WatsonX
    
    @classmethod
    def from_env(cls, provider: Optional[str] = None) -> "AIProviderConfig":
        """
        Create configuration from environment variables.
        
        Environment variables:
        - AI_PROVIDER: Provider name (openai, anthropic, watsonx)
        - OPENAI_API_KEY: OpenAI API key
        - ANTHROPIC_API_KEY: Anthropic API key
        - IBM_CLOUD_API_KEY: IBM Cloud API key
        - WATSONX_PROJECT_ID: WatsonX project ID
        - WATSONX_URL: WatsonX service URL
        - AI_MODEL: Model identifier
        - AI_TEMPERATURE: Temperature setting
        - AI_MAX_TOKENS: Max tokens setting
        """
        provider = provider or os.getenv("AI_PROVIDER", "openai")
        
        config = cls(provider=provider)
        
        # Set API key based on provider
        if provider == "openai":
            config.api_key = os.getenv("OPENAI_API_KEY")
            config.model = os.getenv("AI_MODEL", "gpt-4")
        elif provider == "anthropic":
            config.api_key = os.getenv("ANTHROPIC_API_KEY")
            config.model = os.getenv("AI_MODEL", "claude-3-opus-20240229")
        elif provider == "watsonx":
            config.api_key = os.getenv("IBM_CLOUD_API_KEY")
            config.project_id = os.getenv("WATSONX_PROJECT_ID")
            config.url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
            config.model = os.getenv("AI_MODEL", "ibm/granite-13b-chat-v2")
        
        # Common settings
        config.temperature = float(os.getenv("AI_TEMPERATURE", "0.3"))
        config.max_tokens = int(os.getenv("AI_MAX_TOKENS", "4000"))
        
        return config


@dataclass
class SummarizationConfig:
    """Configuration for summarization pipeline."""
    
    # AI settings
    ai_provider: AIProviderConfig = field(default_factory=AIProviderConfig)
    
    # Processing settings
    aspects: Optional[list] = None  # None = all aspects
    parallel_processing: bool = False
    
    # Output settings
    output_format: str = "json"  # json, markdown, html
    save_prompts: bool = False
    prompts_output_path: Optional[str] = None
    
    # Caching
    enable_cache: bool = True
    cache_dir: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "SummarizationConfig":
        """
        Create configuration from environment variables.
        
        Environment variables:
        - SUMMARIZATION_ASPECTS: Comma-separated list of aspects
        - SUMMARIZATION_OUTPUT_FORMAT: Output format
        - SUMMARIZATION_SAVE_PROMPTS: Whether to save prompts
        - SUMMARIZATION_PROMPTS_PATH: Path to save prompts
        - SUMMARIZATION_ENABLE_CACHE: Enable caching
        - SUMMARIZATION_CACHE_DIR: Cache directory
        - LOG_LEVEL: Logging level
        """
        config = cls()
        
        # AI provider config
        config.ai_provider = AIProviderConfig.from_env()
        
        # Processing settings
        aspects_str = os.getenv("SUMMARIZATION_ASPECTS")
        if aspects_str:
            config.aspects = [a.strip() for a in aspects_str.split(",")]
        
        # Output settings
        config.output_format = os.getenv("SUMMARIZATION_OUTPUT_FORMAT", "json")
        config.save_prompts = os.getenv("SUMMARIZATION_SAVE_PROMPTS", "false").lower() == "true"
        config.prompts_output_path = os.getenv("SUMMARIZATION_PROMPTS_PATH")
        
        # Caching
        config.enable_cache = os.getenv("SUMMARIZATION_ENABLE_CACHE", "true").lower() == "true"
        config.cache_dir = os.getenv("SUMMARIZATION_CACHE_DIR", ".cache/summaries")
        
        # Logging
        config.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        return config
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "ai_provider": {
                "provider": self.ai_provider.provider,
                "model": self.ai_provider.model,
                "temperature": self.ai_provider.temperature,
                "max_tokens": self.ai_provider.max_tokens
            },
            "aspects": self.aspects,
            "parallel_processing": self.parallel_processing,
            "output_format": self.output_format,
            "save_prompts": self.save_prompts,
            "prompts_output_path": self.prompts_output_path,
            "enable_cache": self.enable_cache,
            "cache_dir": self.cache_dir,
            "log_level": self.log_level
        }


# Default configuration
DEFAULT_CONFIG = SummarizationConfig(
    ai_provider=AIProviderConfig(
        provider="openai",
        model="gpt-4",
        temperature=0.3,
        max_tokens=4000
    ),
    output_format="json",
    enable_cache=True,
    cache_dir=".cache/summaries"
)

# Made with Bob
