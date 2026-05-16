# Repository Summarization Pipeline

AI-powered repository analysis and summarization service optimized for enterprise repositories.

## Overview

The Repository Summarization Pipeline provides comprehensive analysis of code repositories using AI models. It generates detailed summaries covering:

- **Repository Overview**: Purpose, scope, and key characteristics
- **Architecture Analysis**: Design patterns, layer structure, and architectural decisions
- **Major Services**: Identification and analysis of core services/components
- **Dependencies**: External and internal dependencies, integrations
- **Business Logic**: Domain models, business rules, and workflows
- **Tech Stack**: Complete technology stack analysis
- **Comprehensive Summary**: Executive-level overview combining all aspects

## Features

✨ **Enterprise-Optimized Prompts**: Carefully crafted prompts designed for large-scale repositories

🔌 **Multiple AI Providers**: Support for OpenAI, Anthropic Claude, and IBM WatsonX

📊 **Structured Output**: JSON, Markdown, or HTML output formats

💾 **Caching**: Built-in caching to avoid redundant API calls

🎯 **Flexible Analysis**: Analyze specific aspects or get comprehensive summaries

⚡ **Async Support**: Both synchronous and asynchronous processing

## Installation

### Prerequisites

```bash
# Core dependencies
pip install -r requirements.txt
```

### Optional AI Provider Dependencies

```bash
# For OpenAI
pip install openai

# For Anthropic Claude
pip install anthropic

# For IBM WatsonX
pip install ibm-watson-machine-learning
```

## Quick Start

### 1. Basic Usage (Prompt Generation Only)

Generate optimized prompts without making AI API calls:

```python
from src.services.repository_summarization import (
    RepositorySummarizer,
    RepositoryData
)

# Create repository data
repo_data = RepositoryData(
    name="my-enterprise-app",
    description="Enterprise application",
    primary_language="Python",
    total_files=500,
    frameworks=["FastAPI", "SQLAlchemy", "Redis"]
)

# Initialize summarizer (no AI client)
summarizer = RepositorySummarizer(ai_client=None)

# Generate prompts
prompts = summarizer.generate_prompts(
    repo_data,
    aspects=['overview', 'architecture']
)

# Export prompts to file
summarizer.export_prompts(repo_data, 'prompts.txt')
```

### 2. Full Pipeline with OpenAI

```python
from src.services.repository_summarization import (
    RepositorySummarizationPipeline,
    SummarizationConfig,
    AIProviderConfig
)
from src.services.repository_summarization.ai_clients import AIClientFactory

# Create AI client
ai_client = AIClientFactory.create_client(
    "openai",
    api_key="your-api-key"
)

# Configure pipeline
config = SummarizationConfig(
    ai_provider=AIProviderConfig(
        provider="openai",
        model="gpt-4",
        temperature=0.3,
        max_tokens=4000
    ),
    aspects=['overview', 'tech_stack'],
    output_format='markdown',
    enable_cache=True
)

# Initialize pipeline
pipeline = RepositorySummarizationPipeline(
    ai_client=ai_client,
    config=config
)

# Process repository
repo_data = {
    'name': 'enterprise-platform',
    'description': 'Microservices platform',
    'primary_language': 'Java',
    'frameworks': ['Spring Boot', 'Kafka'],
    'total_files': 800
}

result = pipeline.process_repository(repo_data)

# Save output
pipeline.save_output(result, 'summary.md', format_type='markdown')
```

### 3. Using Environment Variables

```bash
# Set environment variables
export AI_PROVIDER=openai
export OPENAI_API_KEY=your-key-here
export AI_MODEL=gpt-4
export AI_TEMPERATURE=0.3
export SUMMARIZATION_OUTPUT_FORMAT=markdown
export SUMMARIZATION_ENABLE_CACHE=true
```

```python
from src.services.repository_summarization import (
    RepositorySummarizationPipeline,
    SummarizationConfig
)
from src.services.repository_summarization.ai_clients import AIClientFactory

# Load configuration from environment
config = SummarizationConfig.from_env()
ai_client = AIClientFactory.create_from_env()

# Initialize pipeline
pipeline = RepositorySummarizationPipeline(ai_client, config)

# Process repository
result = pipeline.process_repository(repo_data)
```

## Configuration

### AI Provider Configuration

```python
from src.services.repository_summarization import AIProviderConfig

# OpenAI
openai_config = AIProviderConfig(
    provider="openai",
    api_key="sk-...",
    model="gpt-4",
    temperature=0.3,
    max_tokens=4000
)

# Anthropic Claude
anthropic_config = AIProviderConfig(
    provider="anthropic",
    api_key="sk-ant-...",
    model="claude-3-opus-20240229",
    temperature=0.3,
    max_tokens=4000
)

# IBM WatsonX
watsonx_config = AIProviderConfig(
    provider="watsonx",
    api_key="your-ibm-cloud-key",
    project_id="your-project-id",
    url="https://us-south.ml.cloud.ibm.com",
    model="ibm/granite-13b-chat-v2",
    temperature=0.3,
    max_tokens=4000
)
```

### Pipeline Configuration

```python
from src.services.repository_summarization import SummarizationConfig

config = SummarizationConfig(
    ai_provider=ai_provider_config,
    aspects=['overview', 'architecture', 'services'],  # or None for all
    output_format='json',  # json, markdown, html
    save_prompts=True,
    prompts_output_path='prompts.txt',
    enable_cache=True,
    cache_dir='.cache/summaries',
    log_level='INFO'
)
```

## Repository Data Structure

The pipeline expects repository data in the following structure:

```python
repo_data = {
    # Metadata
    'name': str,
    'description': str,
    'primary_language': str,
    'total_files': int,
    'total_loc': int,
    
    # Structure
    'file_structure': str,
    'directory_tree': str,
    'top_level_dirs': List[str],
    
    # Code analysis
    'key_files': List[str],
    'config_files': List[str],
    'code_patterns': List[str],
    
    # Services
    'service_dirs': List[str],
    'api_endpoints': List[str],
    'class_definitions': List[str],
    'module_exports': List[str],
    
    # Dependencies
    'package_dependencies': Dict[str, str],
    'internal_dependencies': Dict[str, List[str]],
    'external_apis': List[str],
    'database_connections': List[str],
    
    # Business logic
    'business_modules': List[str],
    'domain_models': List[str],
    'business_rules': List[str],
    'workflows': List[str],
    'validation_logic': List[str],
    
    # Tech stack
    'languages': Dict[str, float],
    'frameworks': List[str],
    'build_tools': List[str],
    'testing_frameworks': List[str],
    'infrastructure_code': List[str],
    'cicd_config': List[str],
    
    # Statistics
    'statistics': Dict[str, Any]
}
```

## Analysis Aspects

The pipeline can analyze the following aspects:

1. **overview**: High-level repository overview
2. **architecture**: Software architecture analysis
3. **services**: Major services and components
4. **dependencies**: Dependency analysis
5. **business_logic**: Business logic summary
6. **tech_stack**: Technology stack analysis
7. **comprehensive**: Complete executive summary

Specify aspects in configuration or use `None` for all aspects.

## Output Formats

### JSON

```python
result = pipeline.process_repository(repo_data)
json_output = result.to_json()
```

### Markdown

```python
pipeline.save_output(result, 'summary.md', format_type='markdown')
```

### HTML

```python
pipeline.save_output(result, 'summary.html', format_type='html')
```

## Advanced Usage

### Async Processing

```python
import asyncio

async def analyze_repository():
    result = await pipeline.process_repository_async(repo_data)
    return result

result = asyncio.run(analyze_repository())
```

### Batch Processing

```python
repositories = [repo1_data, repo2_data, repo3_data]

for repo in repositories:
    result = pipeline.process_repository(repo)
    pipeline.save_output(
        result,
        f'{repo["name"]}_summary.md',
        format_type='markdown'
    )
```

### Custom AI Client

```python
from src.services.repository_summarization.ai_clients import AIClientBase

class CustomAIClient(AIClientBase):
    async def generate_async(self, prompt, model, temperature, max_tokens):
        # Your custom implementation
        pass
    
    def generate_sync(self, prompt, model, temperature, max_tokens):
        # Your custom implementation
        pass

# Use custom client
custom_client = CustomAIClient()
pipeline = RepositorySummarizationPipeline(ai_client=custom_client)
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AI_PROVIDER` | AI provider (openai, anthropic, watsonx) | openai |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `IBM_CLOUD_API_KEY` | IBM Cloud API key | - |
| `WATSONX_PROJECT_ID` | WatsonX project ID | - |
| `WATSONX_URL` | WatsonX service URL | https://us-south.ml.cloud.ibm.com |
| `AI_MODEL` | Model identifier | gpt-4 |
| `AI_TEMPERATURE` | Temperature (0.0-1.0) | 0.3 |
| `AI_MAX_TOKENS` | Max tokens per response | 4000 |
| `SUMMARIZATION_ASPECTS` | Comma-separated aspects | all |
| `SUMMARIZATION_OUTPUT_FORMAT` | Output format | json |
| `SUMMARIZATION_SAVE_PROMPTS` | Save prompts to file | false |
| `SUMMARIZATION_PROMPTS_PATH` | Prompts output path | - |
| `SUMMARIZATION_ENABLE_CACHE` | Enable caching | true |
| `SUMMARIZATION_CACHE_DIR` | Cache directory | .cache/summaries |
| `LOG_LEVEL` | Logging level | INFO |

## Examples

See `backend/examples/repository_summarization_example.py` for comprehensive examples:

```bash
cd backend
python examples/repository_summarization_example.py
```

## Best Practices

### 1. Provide Rich Context

The more detailed your repository data, the better the analysis:

```python
repo_data = RepositoryData(
    name="my-app",
    description="Detailed description of what the app does",
    frameworks=["FastAPI", "SQLAlchemy", "Redis", "Celery"],
    business_modules=["User Management", "Order Processing", "Inventory"],
    # ... include as much relevant data as possible
)
```

### 2. Use Caching

Enable caching to avoid redundant API calls:

```python
config = SummarizationConfig(
    enable_cache=True,
    cache_dir='.cache/summaries'
)
```

### 3. Start with Specific Aspects

For faster iteration, analyze specific aspects first:

```python
config = SummarizationConfig(
    aspects=['overview', 'tech_stack']  # Start small
)
```

### 4. Export Prompts for Review

Review generated prompts before making API calls:

```python
summarizer.export_prompts(repo_data, 'prompts.txt')
# Review prompts.txt, then proceed with AI generation
```

### 5. Choose the Right Model

- **GPT-4**: Best quality, slower, more expensive
- **GPT-3.5-turbo**: Good balance of speed and quality
- **Claude 3 Opus**: Excellent for complex analysis
- **Claude 3 Sonnet**: Good balance
- **Granite**: IBM's enterprise-focused model

## Troubleshooting

### API Key Issues

```python
# Verify API key is set
import os
print(os.getenv("OPENAI_API_KEY"))

# Or pass directly
ai_client = AIClientFactory.create_client("openai", api_key="your-key")
```

### Import Errors

```bash
# Install missing dependencies
pip install openai anthropic ibm-watson-machine-learning
```

### Cache Issues

```python
# Clear cache
import shutil
shutil.rmtree('.cache/summaries', ignore_errors=True)
```

## Architecture

```
repository_summarization/
├── __init__.py              # Package exports
├── prompt_templates.py      # Optimized prompt templates
├── summarizer.py           # Core summarization logic
├── pipeline.py             # End-to-end pipeline
├── ai_clients.py           # AI provider integrations
└── config.py               # Configuration management
```

## Contributing

When adding new features:

1. Add prompt templates to `prompt_templates.py`
2. Update `RepositoryData` structure if needed
3. Add configuration options to `config.py`
4. Update documentation and examples

## License

Part of the IBM BOB Project.

## Support

For issues or questions, please refer to the main project documentation.