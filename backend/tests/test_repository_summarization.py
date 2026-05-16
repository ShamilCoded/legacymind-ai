"""
Tests for Repository Summarization Pipeline
"""

import pytest
import json
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.repository_summarization import (
    RepositorySummarizer,
    RepositoryData,
    SummaryResult,
    PromptTemplates,
    RepositorySummarizationPipeline,
    PipelineConfig,
    SummarizationConfig,
    AIProviderConfig
)


class TestRepositoryData:
    """Tests for RepositoryData class."""
    
    def test_repository_data_creation(self):
        """Test creating RepositoryData instance."""
        data = RepositoryData(
            name="test-repo",
            description="Test repository",
            primary_language="Python",
            total_files=100,
            total_loc=10000
        )
        
        assert data.name == "test-repo"
        assert data.description == "Test repository"
        assert data.primary_language == "Python"
        assert data.total_files == 100
        assert data.total_loc == 10000
    
    def test_repository_data_to_dict(self):
        """Test converting RepositoryData to dictionary."""
        data = RepositoryData(
            name="test-repo",
            frameworks=["FastAPI", "SQLAlchemy"]
        )
        
        data_dict = data.to_dict()
        
        assert isinstance(data_dict, dict)
        assert data_dict['name'] == "test-repo"
        assert data_dict['frameworks'] == ["FastAPI", "SQLAlchemy"]
    
    def test_repository_data_optional_fields(self):
        """Test RepositoryData with optional fields."""
        data = RepositoryData(
            name="test-repo",
            service_dirs=["auth", "api", "workers"],
            languages={"Python": 80.0, "JavaScript": 20.0}
        )
        
        assert data.service_dirs == ["auth", "api", "workers"]
        assert data.languages == {"Python": 80.0, "JavaScript": 20.0}


class TestSummaryResult:
    """Tests for SummaryResult class."""
    
    def test_summary_result_creation(self):
        """Test creating SummaryResult instance."""
        result = SummaryResult(
            overview="Repository overview",
            tech_stack="Technology stack analysis"
        )
        
        assert result.overview == "Repository overview"
        assert result.tech_stack == "Technology stack analysis"
        assert result.architecture is None
    
    def test_summary_result_to_dict(self):
        """Test converting SummaryResult to dictionary."""
        result = SummaryResult(
            overview="Overview text",
            architecture="Architecture text"
        )
        
        result_dict = result.to_dict()
        
        assert isinstance(result_dict, dict)
        assert result_dict['overview'] == "Overview text"
        assert result_dict['architecture'] == "Architecture text"
        assert 'services' not in result_dict  # None values excluded
    
    def test_summary_result_to_json(self):
        """Test converting SummaryResult to JSON."""
        result = SummaryResult(
            overview="Overview",
            tech_stack="Tech stack"
        )
        
        json_str = result.to_json()
        
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed['overview'] == "Overview"
        assert parsed['tech_stack'] == "Tech stack"


class TestPromptTemplates:
    """Tests for PromptTemplates class."""
    
    def test_repository_overview_prompt(self):
        """Test generating repository overview prompt."""
        repo_data = {
            'name': 'test-repo',
            'description': 'Test description',
            'primary_language': 'Python',
            'total_files': 100
        }
        
        prompt = PromptTemplates.repository_overview(repo_data)
        
        assert isinstance(prompt, str)
        assert 'test-repo' in prompt
        assert 'Python' in prompt
        assert 'overview' in prompt.lower()
    
    def test_architecture_analysis_prompt(self):
        """Test generating architecture analysis prompt."""
        repo_data = {
            'directory_tree': 'src/\n  api/\n  models/',
            'code_patterns': ['MVC', 'Repository Pattern']
        }
        
        prompt = PromptTemplates.architecture_analysis(repo_data)
        
        assert isinstance(prompt, str)
        assert 'architecture' in prompt.lower()
        assert 'pattern' in prompt.lower()
    
    def test_services_identification_prompt(self):
        """Test generating services identification prompt."""
        repo_data = {
            'service_dirs': ['auth', 'api', 'workers'],
            'api_endpoints': ['/api/users', '/api/products']
        }
        
        prompt = PromptTemplates.services_identification(repo_data)
        
        assert isinstance(prompt, str)
        assert 'service' in prompt.lower()
        assert 'component' in prompt.lower()
    
    def test_dependencies_analysis_prompt(self):
        """Test generating dependencies analysis prompt."""
        repo_data = {
            'package_dependencies': {'fastapi': '0.100.0', 'sqlalchemy': '2.0.0'},
            'external_apis': ['Stripe API', 'SendGrid']
        }
        
        prompt = PromptTemplates.dependencies_analysis(repo_data)
        
        assert isinstance(prompt, str)
        assert 'dependencies' in prompt.lower()
    
    def test_business_logic_summary_prompt(self):
        """Test generating business logic summary prompt."""
        repo_data = {
            'business_modules': ['User Management', 'Order Processing'],
            'domain_models': ['User', 'Order', 'Product']
        }
        
        prompt = PromptTemplates.business_logic_summary(repo_data)
        
        assert isinstance(prompt, str)
        assert 'business' in prompt.lower()
    
    def test_tech_stack_analysis_prompt(self):
        """Test generating tech stack analysis prompt."""
        repo_data = {
            'languages': {'Python': 80.0, 'JavaScript': 20.0},
            'frameworks': ['FastAPI', 'React'],
            'testing_frameworks': ['pytest', 'Jest']
        }
        
        prompt = PromptTemplates.tech_stack_analysis(repo_data)
        
        assert isinstance(prompt, str)
        assert 'technology' in prompt.lower() or 'tech stack' in prompt.lower()
    
    def test_comprehensive_summary_prompt(self):
        """Test generating comprehensive summary prompt."""
        repo_data = {
            'metadata': {'name': 'test-repo'},
            'structure': 'src/',
            'statistics': {'files': 100}
        }
        
        prompt = PromptTemplates.comprehensive_summary(repo_data)
        
        assert isinstance(prompt, str)
        assert 'comprehensive' in prompt.lower() or 'executive' in prompt.lower()
    
    def test_get_all_prompts(self):
        """Test generating all prompts at once."""
        repo_data = {
            'name': 'test-repo',
            'primary_language': 'Python'
        }
        
        prompts = PromptTemplates.get_all_prompts(repo_data)
        
        assert isinstance(prompts, dict)
        assert 'overview' in prompts
        assert 'architecture' in prompts
        assert 'services' in prompts
        assert 'dependencies' in prompts
        assert 'business_logic' in prompts
        assert 'tech_stack' in prompts
        assert 'comprehensive' in prompts
        assert len(prompts) == 7


class TestRepositorySummarizer:
    """Tests for RepositorySummarizer class."""
    
    def test_summarizer_initialization(self):
        """Test initializing summarizer without AI client."""
        summarizer = RepositorySummarizer(ai_client=None)
        
        assert summarizer.ai_client is None
        assert summarizer.prompt_templates is not None
    
    def test_generate_prompts_all_aspects(self):
        """Test generating prompts for all aspects."""
        summarizer = RepositorySummarizer(ai_client=None)
        
        repo_data = RepositoryData(
            name="test-repo",
            primary_language="Python"
        )
        
        prompts = summarizer.generate_prompts(repo_data, aspects=None)
        
        assert isinstance(prompts, dict)
        assert len(prompts) == 7
        assert all(isinstance(p, str) for p in prompts.values())
    
    def test_generate_prompts_specific_aspects(self):
        """Test generating prompts for specific aspects."""
        summarizer = RepositorySummarizer(ai_client=None)
        
        repo_data = RepositoryData(
            name="test-repo",
            primary_language="Python"
        )
        
        prompts = summarizer.generate_prompts(
            repo_data,
            aspects=['overview', 'tech_stack']
        )
        
        assert isinstance(prompts, dict)
        assert len(prompts) == 2
        assert 'overview' in prompts
        assert 'tech_stack' in prompts
    
    def test_generate_prompts_invalid_aspect(self):
        """Test generating prompts with invalid aspect."""
        summarizer = RepositorySummarizer(ai_client=None)
        
        repo_data = RepositoryData(name="test-repo")
        
        prompts = summarizer.generate_prompts(
            repo_data,
            aspects=['overview', 'invalid_aspect']
        )
        
        # Should only include valid aspects
        assert 'overview' in prompts
        assert 'invalid_aspect' not in prompts
    
    def test_export_prompts(self, tmp_path):
        """Test exporting prompts to file."""
        summarizer = RepositorySummarizer(ai_client=None)
        
        repo_data = RepositoryData(
            name="test-repo",
            primary_language="Python"
        )
        
        output_path = tmp_path / "prompts.txt"
        
        summarizer.export_prompts(
            repo_data,
            str(output_path),
            aspects=['overview']
        )
        
        assert output_path.exists()
        content = output_path.read_text()
        assert 'test-repo' in content
        assert 'OVERVIEW' in content


class TestPipelineConfig:
    """Tests for PipelineConfig class."""
    
    def test_pipeline_config_defaults(self):
        """Test PipelineConfig default values."""
        config = PipelineConfig()
        
        assert config.model == "gpt-4"
        assert config.temperature == 0.3
        assert config.max_tokens == 4000
        assert config.aspects is None
        assert config.output_format == "json"
        assert config.enable_cache is True
    
    def test_pipeline_config_custom_values(self):
        """Test PipelineConfig with custom values."""
        config = PipelineConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            aspects=['overview', 'tech_stack'],
            output_format='markdown'
        )
        
        assert config.model == "gpt-3.5-turbo"
        assert config.temperature == 0.5
        assert config.aspects == ['overview', 'tech_stack']
        assert config.output_format == 'markdown'


class TestSummarizationConfig:
    """Tests for SummarizationConfig class."""
    
    def test_config_defaults(self):
        """Test SummarizationConfig default values."""
        config = SummarizationConfig()
        
        assert config.output_format == "json"
        assert config.enable_cache is True
        assert config.save_prompts is False
    
    def test_config_to_dict(self):
        """Test converting config to dictionary."""
        config = SummarizationConfig(
            output_format='markdown',
            aspects=['overview']
        )
        
        config_dict = config.to_dict()
        
        assert isinstance(config_dict, dict)
        assert config_dict['output_format'] == 'markdown'
        assert config_dict['aspects'] == ['overview']


class TestRepositorySummarizationPipeline:
    """Tests for RepositorySummarizationPipeline class."""
    
    def test_pipeline_initialization(self):
        """Test initializing pipeline."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        assert pipeline.ai_client is None
        assert pipeline.summarizer is not None
        assert pipeline.config is not None
    
    def test_structure_repository_data(self):
        """Test structuring raw repository data."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        raw_data = {
            'name': 'test-repo',
            'description': 'Test description',
            'primary_language': 'Python',
            'total_files': 100,
            'frameworks': ['FastAPI']
        }
        
        structured = pipeline._structure_repository_data(raw_data)
        
        assert isinstance(structured, RepositoryData)
        assert structured.name == 'test-repo'
        assert structured.primary_language == 'Python'
        assert structured.frameworks == ['FastAPI']
    
    def test_generate_cache_key(self):
        """Test generating cache key."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        repo_data = RepositoryData(
            name="test-repo",
            total_files=100,
            total_loc=10000
        )
        
        cache_key = pipeline._generate_cache_key(repo_data)
        
        assert isinstance(cache_key, str)
        assert len(cache_key) == 32  # MD5 hash length
    
    def test_format_output_json(self):
        """Test formatting output as JSON."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        result = SummaryResult(
            overview="Overview text",
            tech_stack="Tech stack text"
        )
        
        output = pipeline.format_output(result, format_type='json')
        
        assert isinstance(output, str)
        parsed = json.loads(output)
        assert parsed['overview'] == "Overview text"
    
    def test_format_output_markdown(self):
        """Test formatting output as Markdown."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        result = SummaryResult(
            overview="Overview text",
            architecture="Architecture text"
        )
        
        output = pipeline.format_output(result, format_type='markdown')
        
        assert isinstance(output, str)
        assert '# Repository Analysis Summary' in output
        assert '## Overview' in output
        assert '## Architecture' in output
        assert 'Overview text' in output
    
    def test_format_output_html(self):
        """Test formatting output as HTML."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        result = SummaryResult(
            overview="Overview text"
        )
        
        output = pipeline.format_output(result, format_type='html')
        
        assert isinstance(output, str)
        assert '<!DOCTYPE html>' in output
        assert '<h1>Repository Analysis Summary</h1>' in output
        assert 'Overview text' in output
    
    def test_save_output(self, tmp_path):
        """Test saving output to file."""
        pipeline = RepositorySummarizationPipeline(ai_client=None)
        
        result = SummaryResult(overview="Test overview")
        output_path = tmp_path / "output.json"
        
        pipeline.save_output(result, str(output_path), format_type='json')
        
        assert output_path.exists()
        content = output_path.read_text()
        assert 'Test overview' in content


class TestAIProviderConfig:
    """Tests for AIProviderConfig class."""
    
    def test_ai_provider_config_defaults(self):
        """Test AIProviderConfig default values."""
        config = AIProviderConfig()
        
        assert config.provider == "openai"
        assert config.model == "gpt-4"
        assert config.temperature == 0.3
        assert config.max_tokens == 4000
    
    def test_ai_provider_config_custom(self):
        """Test AIProviderConfig with custom values."""
        config = AIProviderConfig(
            provider="anthropic",
            model="claude-3-opus-20240229",
            temperature=0.5,
            api_key="test-key"
        )
        
        assert config.provider == "anthropic"
        assert config.model == "claude-3-opus-20240229"
        assert config.temperature == 0.5
        assert config.api_key == "test-key"


# Integration tests would go here
class TestIntegration:
    """Integration tests (require AI client setup)."""
    
    @pytest.mark.skip(reason="Requires AI API key")
    def test_full_pipeline_with_openai(self):
        """Test full pipeline with OpenAI (requires API key)."""
        # This test would require actual API credentials
        pass
    
    @pytest.mark.skip(reason="Requires AI API key")
    def test_async_processing(self):
        """Test async processing (requires API key)."""
        # This test would require actual API credentials
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
