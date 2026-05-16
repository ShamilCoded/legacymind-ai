"""
Repository Summarization Pipeline

End-to-end pipeline for processing repository data and generating summaries.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path
from dataclasses import dataclass

from .summarizer import RepositorySummarizer, RepositoryData, SummaryResult


logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration for the summarization pipeline."""
    
    # AI Model settings
    model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 4000
    
    # Processing settings
    aspects: Optional[List[str]] = None  # None = all aspects
    parallel_processing: bool = False
    
    # Output settings
    output_format: str = "json"  # json, markdown, html
    save_prompts: bool = False
    prompts_output_path: Optional[str] = None
    
    # Caching
    enable_cache: bool = True
    cache_dir: Optional[str] = None


class RepositorySummarizationPipeline:
    """
    End-to-end pipeline for repository analysis and summarization.
    
    This pipeline:
    1. Accepts parsed repository data
    2. Structures it for analysis
    3. Generates optimized prompts
    4. Calls AI models for summarization
    5. Formats and returns results
    """
    
    def __init__(
        self,
        ai_client: Optional[Any] = None,
        config: Optional[PipelineConfig] = None
    ):
        """
        Initialize the pipeline.
        
        Args:
            ai_client: AI model client for generating summaries
            config: Pipeline configuration
        """
        self.ai_client = ai_client
        self.config = config or PipelineConfig()
        self.summarizer = RepositorySummarizer(ai_client)
        
        if self.config.enable_cache and self.config.cache_dir:
            os.makedirs(self.config.cache_dir, exist_ok=True)
    
    def process_repository(
        self,
        repo_data: Dict[str, Any],
        custom_config: Optional[PipelineConfig] = None
    ) -> SummaryResult:
        """
        Process repository data and generate summaries.
        
        Args:
            repo_data: Raw repository data dictionary
            custom_config: Override default configuration
        
        Returns:
            SummaryResult with generated summaries
        """
        config = custom_config or self.config
        
        # Step 1: Structure the data
        logger.info("Structuring repository data...")
        structured_data = self._structure_repository_data(repo_data)
        
        # Step 2: Check cache
        if config.enable_cache:
            cached_result = self._check_cache(structured_data)
            if cached_result:
                logger.info("Using cached results")
                return cached_result
        
        # Step 3: Export prompts if requested
        if config.save_prompts and config.prompts_output_path:
            logger.info("Exporting prompts...")
            self.summarizer.export_prompts(
                structured_data,
                config.prompts_output_path,
                config.aspects
            )
        
        # Step 4: Generate summaries
        logger.info("Generating summaries...")
        result = self.summarizer.summarize_sync(
            repo_data=structured_data,
            aspects=config.aspects,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        # Step 5: Cache results
        if config.enable_cache:
            self._cache_result(structured_data, result)
        
        return result
    
    async def process_repository_async(
        self,
        repo_data: Dict[str, Any],
        custom_config: Optional[PipelineConfig] = None
    ) -> SummaryResult:
        """
        Asynchronously process repository data and generate summaries.
        
        Args:
            repo_data: Raw repository data dictionary
            custom_config: Override default configuration
        
        Returns:
            SummaryResult with generated summaries
        """
        config = custom_config or self.config
        
        # Step 1: Structure the data
        logger.info("Structuring repository data...")
        structured_data = self._structure_repository_data(repo_data)
        
        # Step 2: Check cache
        if config.enable_cache:
            cached_result = self._check_cache(structured_data)
            if cached_result:
                logger.info("Using cached results")
                return cached_result
        
        # Step 3: Export prompts if requested
        if config.save_prompts and config.prompts_output_path:
            logger.info("Exporting prompts...")
            self.summarizer.export_prompts(
                structured_data,
                config.prompts_output_path,
                config.aspects
            )
        
        # Step 4: Generate summaries
        logger.info("Generating summaries...")
        result = await self.summarizer.summarize(
            repo_data=structured_data,
            aspects=config.aspects,
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        
        # Step 5: Cache results
        if config.enable_cache:
            self._cache_result(structured_data, result)
        
        return result
    
    def _structure_repository_data(self, raw_data: Dict[str, Any]) -> RepositoryData:
        """
        Convert raw repository data to structured RepositoryData object.
        
        Args:
            raw_data: Raw data dictionary
        
        Returns:
            Structured RepositoryData object
        """
        return RepositoryData(
            # Metadata
            name=raw_data.get('name', 'Unknown'),
            description=raw_data.get('description'),
            primary_language=raw_data.get('primary_language'),
            total_files=raw_data.get('total_files', 0),
            total_loc=raw_data.get('total_loc', 0),
            
            # Structure
            file_structure=raw_data.get('file_structure'),
            directory_tree=raw_data.get('directory_tree'),
            top_level_dirs=raw_data.get('top_level_dirs'),
            
            # Code analysis
            key_files=raw_data.get('key_files'),
            config_files=raw_data.get('config_files'),
            code_patterns=raw_data.get('code_patterns'),
            
            # Services
            service_dirs=raw_data.get('service_dirs'),
            api_endpoints=raw_data.get('api_endpoints'),
            class_definitions=raw_data.get('class_definitions'),
            module_exports=raw_data.get('module_exports'),
            
            # Dependencies
            package_dependencies=raw_data.get('package_dependencies'),
            internal_dependencies=raw_data.get('internal_dependencies'),
            external_apis=raw_data.get('external_apis'),
            database_connections=raw_data.get('database_connections'),
            
            # Business logic
            business_modules=raw_data.get('business_modules'),
            domain_models=raw_data.get('domain_models'),
            business_rules=raw_data.get('business_rules'),
            workflows=raw_data.get('workflows'),
            validation_logic=raw_data.get('validation_logic'),
            
            # Tech stack
            languages=raw_data.get('languages'),
            frameworks=raw_data.get('frameworks'),
            build_tools=raw_data.get('build_tools'),
            testing_frameworks=raw_data.get('testing_frameworks'),
            infrastructure_code=raw_data.get('infrastructure_code'),
            cicd_config=raw_data.get('cicd_config'),
            
            # Statistics
            statistics=raw_data.get('statistics')
        )
    
    def _check_cache(self, repo_data: RepositoryData) -> Optional[SummaryResult]:
        """
        Check if cached results exist for this repository.
        
        Args:
            repo_data: Repository data
        
        Returns:
            Cached SummaryResult if exists, None otherwise
        """
        if not self.config.cache_dir:
            return None
        
        cache_key = self._generate_cache_key(repo_data)
        cache_path = Path(self.config.cache_dir) / f"{cache_key}.json"
        
        if cache_path.exists():
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                return SummaryResult(**cached_data)
            except Exception as e:
                logger.warning(f"Failed to load cache: {str(e)}")
        
        return None
    
    def _cache_result(self, repo_data: RepositoryData, result: SummaryResult) -> None:
        """
        Cache the summarization result.
        
        Args:
            repo_data: Repository data
            result: Summary result to cache
        """
        if not self.config.cache_dir:
            return
        
        cache_key = self._generate_cache_key(repo_data)
        cache_path = Path(self.config.cache_dir) / f"{cache_key}.json"
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(result.to_dict(), f, indent=2)
            logger.info(f"Results cached to {cache_path}")
        except Exception as e:
            logger.warning(f"Failed to cache results: {str(e)}")
    
    def _generate_cache_key(self, repo_data: RepositoryData) -> str:
        """
        Generate a cache key for repository data.
        
        Args:
            repo_data: Repository data
        
        Returns:
            Cache key string
        """
        import hashlib
        
        # Create a hash based on key repository attributes
        key_data = f"{repo_data.name}_{repo_data.total_files}_{repo_data.total_loc}"
        return hashlib.md5(key_data.encode(), usedforsecurity=False).hexdigest()
    
    def format_output(
        self,
        result: SummaryResult,
        format_type: Optional[str] = None
    ) -> str:
        """
        Format the summary result in the specified format.
        
        Args:
            result: Summary result
            format_type: Output format (json, markdown, html)
        
        Returns:
            Formatted string
        """
        format_type = format_type or self.config.output_format
        
        if format_type == "json":
            return result.to_json()
        elif format_type == "markdown":
            return self._format_as_markdown(result)
        elif format_type == "html":
            return self._format_as_html(result)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _format_as_markdown(self, result: SummaryResult) -> str:
        """Format result as Markdown."""
        md = "# Repository Analysis Summary\n\n"
        
        if result.overview:
            md += "## Overview\n\n"
            md += result.overview + "\n\n"
        
        if result.architecture:
            md += "## Architecture\n\n"
            md += result.architecture + "\n\n"
        
        if result.services:
            md += "## Major Services\n\n"
            md += result.services + "\n\n"
        
        if result.dependencies:
            md += "## Dependencies\n\n"
            md += result.dependencies + "\n\n"
        
        if result.business_logic:
            md += "## Business Logic\n\n"
            md += result.business_logic + "\n\n"
        
        if result.tech_stack:
            md += "## Technology Stack\n\n"
            md += result.tech_stack + "\n\n"
        
        if result.comprehensive:
            md += "## Comprehensive Summary\n\n"
            md += result.comprehensive + "\n\n"
        
        return md
    
    def _format_as_html(self, result: SummaryResult) -> str:
        """Format result as HTML."""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Repository Analysis Summary</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        h2 { color: #007bff; margin-top: 30px; }
        pre { background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>Repository Analysis Summary</h1>
"""
        
        if result.overview:
            html += f"<h2>Overview</h2><pre>{result.overview}</pre>"
        
        if result.architecture:
            html += f"<h2>Architecture</h2><pre>{result.architecture}</pre>"
        
        if result.services:
            html += f"<h2>Major Services</h2><pre>{result.services}</pre>"
        
        if result.dependencies:
            html += f"<h2>Dependencies</h2><pre>{result.dependencies}</pre>"
        
        if result.business_logic:
            html += f"<h2>Business Logic</h2><pre>{result.business_logic}</pre>"
        
        if result.tech_stack:
            html += f"<h2>Technology Stack</h2><pre>{result.tech_stack}</pre>"
        
        if result.comprehensive:
            html += f"<h2>Comprehensive Summary</h2><pre>{result.comprehensive}</pre>"
        
        html += "</body></html>"
        return html
    
    def save_output(
        self,
        result: SummaryResult,
        output_path: str,
        format_type: Optional[str] = None
    ) -> None:
        """
        Save the formatted output to a file.
        
        Args:
            result: Summary result
            output_path: Path to save the output
            format_type: Output format
        """
        formatted_output = self.format_output(result, format_type)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        
        logger.info(f"Output saved to {output_path}")

# Made with Bob
