"""
Repository Summarization Service

This service provides AI-powered repository analysis and summarization capabilities.
It takes parsed repository code, metadata, and file structure as input and generates
comprehensive summaries including:
- Repository overview
- Architecture explanation
- Major services identification
- Dependencies analysis
- Business logic summary
- Tech stack analysis
"""

from .pipeline import RepositorySummarizationPipeline, PipelineConfig
from .prompt_templates import PromptTemplates
from .summarizer import RepositorySummarizer, RepositoryData, SummaryResult
from .ai_clients import AIClientFactory, AIClientBase, OpenAIClient, AnthropicClient, WatsonXClient
from .config import SummarizationConfig, AIProviderConfig

__all__ = [
    'RepositorySummarizationPipeline',
    'PipelineConfig',
    'PromptTemplates',
    'RepositorySummarizer',
    'RepositoryData',
    'SummaryResult',
    'AIClientFactory',
    'AIClientBase',
    'OpenAIClient',
    'AnthropicClient',
    'WatsonXClient',
    'SummarizationConfig',
    'AIProviderConfig'
]

# Made with Bob
