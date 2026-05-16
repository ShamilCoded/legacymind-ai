"""
Repository Summarizer

Core service for generating AI-powered repository summaries.
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
import logging

from .prompt_templates import PromptTemplates


logger = logging.getLogger(__name__)


@dataclass
class RepositoryData:
    """
    Structured repository data for analysis.
    """
    # Metadata
    name: str
    description: Optional[str] = None
    primary_language: Optional[str] = None
    total_files: int = 0
    total_loc: int = 0
    
    # Structure
    file_structure: Optional[str] = None
    directory_tree: Optional[str] = None
    top_level_dirs: Optional[List[str]] = None
    
    # Code analysis
    key_files: Optional[List[str]] = None
    config_files: Optional[List[str]] = None
    code_patterns: Optional[List[str]] = None
    
    # Services
    service_dirs: Optional[List[str]] = None
    api_endpoints: Optional[List[str]] = None
    class_definitions: Optional[List[str]] = None
    module_exports: Optional[List[str]] = None
    
    # Dependencies
    package_dependencies: Optional[Dict[str, str]] = None
    internal_dependencies: Optional[Dict[str, List[str]]] = None
    external_apis: Optional[List[str]] = None
    database_connections: Optional[List[str]] = None
    
    # Business logic
    business_modules: Optional[List[str]] = None
    domain_models: Optional[List[str]] = None
    business_rules: Optional[List[str]] = None
    workflows: Optional[List[str]] = None
    validation_logic: Optional[List[str]] = None
    
    # Tech stack
    languages: Optional[Dict[str, float]] = None
    frameworks: Optional[List[str]] = None
    build_tools: Optional[List[str]] = None
    testing_frameworks: Optional[List[str]] = None
    infrastructure_code: Optional[List[str]] = None
    cicd_config: Optional[List[str]] = None
    
    # Statistics
    statistics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for prompt generation."""
        return asdict(self)


@dataclass
class SummaryResult:
    """
    Result of repository summarization.
    """
    overview: Optional[str] = None
    architecture: Optional[str] = None
    services: Optional[str] = None
    dependencies: Optional[str] = None
    business_logic: Optional[str] = None
    tech_stack: Optional[str] = None
    comprehensive: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


class RepositorySummarizer:
    """
    Service for generating AI-powered repository summaries.
    
    This class handles the generation of prompts and coordination of AI model calls
    to produce comprehensive repository analysis.
    """
    
    def __init__(self, ai_client: Optional[Any] = None):
        """
        Initialize the summarizer.
        
        Args:
            ai_client: AI model client (e.g., OpenAI, Anthropic, etc.)
                      If None, only prompts will be generated without AI calls.
        """
        self.ai_client = ai_client
        self.prompt_templates = PromptTemplates()
        
    def generate_prompts(
        self,
        repo_data: RepositoryData,
        aspects: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Generate prompts for specified aspects of repository analysis.
        
        Args:
            repo_data: Structured repository data
            aspects: List of aspects to analyze. If None, generates all.
                    Valid values: 'overview', 'architecture', 'services',
                    'dependencies', 'business_logic', 'tech_stack', 'comprehensive'
        
        Returns:
            Dictionary mapping aspect to prompt
        """
        repo_dict = repo_data.to_dict()
        
        if aspects is None:
            return self.prompt_templates.get_all_prompts(repo_dict)
        
        prompts = {}
        for aspect in aspects:
            if aspect == 'overview':
                prompts[aspect] = self.prompt_templates.repository_overview(repo_dict)
            elif aspect == 'architecture':
                prompts[aspect] = self.prompt_templates.architecture_analysis(repo_dict)
            elif aspect == 'services':
                prompts[aspect] = self.prompt_templates.services_identification(repo_dict)
            elif aspect == 'dependencies':
                prompts[aspect] = self.prompt_templates.dependencies_analysis(repo_dict)
            elif aspect == 'business_logic':
                prompts[aspect] = self.prompt_templates.business_logic_summary(repo_dict)
            elif aspect == 'tech_stack':
                prompts[aspect] = self.prompt_templates.tech_stack_analysis(repo_dict)
            elif aspect == 'comprehensive':
                prompts[aspect] = self.prompt_templates.comprehensive_summary(repo_dict)
            else:
                logger.warning(f"Unknown aspect: {aspect}")
        
        return prompts
    
    async def summarize(
        self,
        repo_data: RepositoryData,
        aspects: Optional[List[str]] = None,
        model: str = "gpt-4",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> SummaryResult:
        """
        Generate AI-powered summaries for specified aspects.
        
        Args:
            repo_data: Structured repository data
            aspects: List of aspects to analyze. If None, analyzes all.
            model: AI model to use
            temperature: Temperature for AI generation (0.0-1.0)
            max_tokens: Maximum tokens for each response
        
        Returns:
            SummaryResult containing generated summaries
        """
        if self.ai_client is None:
            raise ValueError("AI client not configured. Initialize with an AI client to generate summaries.")
        
        prompts = self.generate_prompts(repo_data, aspects)
        result = SummaryResult()
        
        for aspect, prompt in prompts.items():
            try:
                logger.info(f"Generating {aspect} summary...")
                summary = await self._call_ai_model(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                setattr(result, aspect, summary)
                logger.info(f"Successfully generated {aspect} summary")
            except Exception as e:
                logger.error(f"Error generating {aspect} summary: {str(e)}")
                setattr(result, aspect, f"Error: {str(e)}")
        
        return result
    
    def summarize_sync(
        self,
        repo_data: RepositoryData,
        aspects: Optional[List[str]] = None,
        model: str = "gpt-4",
        temperature: float = 0.3,
        max_tokens: int = 4000
    ) -> SummaryResult:
        """
        Synchronous version of summarize.
        
        Args:
            repo_data: Structured repository data
            aspects: List of aspects to analyze. If None, analyzes all.
            model: AI model to use
            temperature: Temperature for AI generation (0.0-1.0)
            max_tokens: Maximum tokens for each response
        
        Returns:
            SummaryResult containing generated summaries
        """
        if self.ai_client is None:
            raise ValueError("AI client not configured. Initialize with an AI client to generate summaries.")
        
        prompts = self.generate_prompts(repo_data, aspects)
        result = SummaryResult()
        
        for aspect, prompt in prompts.items():
            try:
                logger.info(f"Generating {aspect} summary...")
                summary = self._call_ai_model_sync(
                    prompt=prompt,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                setattr(result, aspect, summary)
                logger.info(f"Successfully generated {aspect} summary")
            except Exception as e:
                logger.error(f"Error generating {aspect} summary: {str(e)}")
                setattr(result, aspect, f"Error: {str(e)}")
        
        return result
    
    async def _call_ai_model(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Call AI model asynchronously (to be implemented based on specific AI client).
        
        Args:
            prompt: The prompt to send
            model: Model identifier
            temperature: Temperature setting
            max_tokens: Max tokens for response
        
        Returns:
            Generated text
        """
        # This is a placeholder. Implement based on your AI client.
        # Example for OpenAI:
        # response = await self.ai_client.chat.completions.create(
        #     model=model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=temperature,
        #     max_tokens=max_tokens
        # )
        # return response.choices[0].message.content
        
        raise NotImplementedError("AI model integration not implemented. Override this method with your AI client logic.")
    
    def _call_ai_model_sync(
        self,
        prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """
        Call AI model synchronously (to be implemented based on specific AI client).
        
        Args:
            prompt: The prompt to send
            model: Model identifier
            temperature: Temperature setting
            max_tokens: Max tokens for response
        
        Returns:
            Generated text
        """
        # This is a placeholder. Implement based on your AI client.
        # Example for OpenAI:
        # response = self.ai_client.chat.completions.create(
        #     model=model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=temperature,
        #     max_tokens=max_tokens
        # )
        # return response.choices[0].message.content
        
        raise NotImplementedError("AI model integration not implemented. Override this method with your AI client logic.")
    
    def export_prompts(
        self,
        repo_data: RepositoryData,
        output_path: str,
        aspects: Optional[List[str]] = None
    ) -> None:
        """
        Export generated prompts to a file for review or manual use.
        
        Args:
            repo_data: Structured repository data
            output_path: Path to output file
            aspects: List of aspects to include
        """
        prompts = self.generate_prompts(repo_data, aspects)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Repository Analysis Prompts\n\n")
            f.write(f"Repository: {repo_data.name}\n\n")
            f.write("---\n\n")
            
            for aspect, prompt in prompts.items():
                f.write(f"## {aspect.upper()}\n\n")
                f.write(prompt)
                f.write("\n\n---\n\n")
        
        logger.info(f"Prompts exported to {output_path}")

# Made with Bob
