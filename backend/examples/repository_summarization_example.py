"""
Repository Summarization Examples

Demonstrates how to use the repository summarization pipeline.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.repository_summarization import (
    RepositorySummarizationPipeline,
    RepositorySummarizer,
    RepositoryData
)
from src.services.repository_summarization.config import SummarizationConfig, AIProviderConfig
from src.services.repository_summarization.ai_clients import AIClientFactory


def example_1_basic_usage():
    """
    Example 1: Basic usage with mock data (no AI client).
    
    This example shows how to generate prompts without making AI API calls.
    """
    print("=" * 80)
    print("Example 1: Basic Usage - Generate Prompts Only")
    print("=" * 80)
    
    # Create sample repository data
    repo_data = {
        'name': 'enterprise-api',
        'description': 'Enterprise REST API for customer management',
        'primary_language': 'Python',
        'total_files': 150,
        'total_loc': 25000,
        'file_structure': '''
        src/
        ├── api/
        │   ├── routes/
        │   ├── controllers/
        │   └── middleware/
        ├── models/
        ├── services/
        ├── utils/
        └── config/
        ''',
        'top_level_dirs': ['src', 'tests', 'docs', 'config'],
        'frameworks': ['FastAPI', 'SQLAlchemy', 'Pydantic'],
        'languages': {'Python': 85.0, 'JavaScript': 10.0, 'Shell': 5.0}
    }
    
    # Initialize summarizer without AI client (prompts only)
    summarizer = RepositorySummarizer(ai_client=None)
    
    # Create structured data
    structured_data = RepositoryData(
        name=repo_data['name'],
        description=repo_data['description'],
        primary_language=repo_data['primary_language'],
        total_files=repo_data['total_files'],
        total_loc=repo_data['total_loc'],
        file_structure=repo_data['file_structure'],
        top_level_dirs=repo_data['top_level_dirs'],
        frameworks=repo_data['frameworks'],
        languages=repo_data['languages']
    )
    
    # Generate prompts for specific aspects
    prompts = summarizer.generate_prompts(
        structured_data,
        aspects=['overview', 'tech_stack']
    )
    
    # Export prompts to file
    output_path = 'repository_analysis_prompts.txt'
    summarizer.export_prompts(structured_data, output_path, aspects=['overview', 'tech_stack'])
    
    print(f"\n✓ Generated {len(prompts)} prompts")
    print(f"✓ Prompts exported to: {output_path}")
    print("\nPrompt preview (Overview):")
    print("-" * 80)
    print(prompts['overview'][:500] + "...")
    print()


def example_2_with_openai():
    """
    Example 2: Full pipeline with OpenAI integration.
    
    Requires OPENAI_API_KEY environment variable.
    """
    print("=" * 80)
    print("Example 2: Full Pipeline with OpenAI")
    print("=" * 80)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠ OPENAI_API_KEY not set. Skipping this example.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        return
    
    # Create AI client
    ai_client = AIClientFactory.create_client("openai")
    
    # Create configuration
    config = SummarizationConfig(
        ai_provider=AIProviderConfig(
            provider="openai",
            model="gpt-4",
            temperature=0.3,
            max_tokens=2000
        ),
        aspects=['overview', 'tech_stack'],
        output_format='markdown',
        enable_cache=True,
        cache_dir='.cache/summaries'
    )
    
    # Initialize pipeline
    pipeline = RepositorySummarizationPipeline(ai_client=ai_client)
    
    # Sample repository data
    repo_data = {
        'name': 'microservices-platform',
        'description': 'Enterprise microservices platform with event-driven architecture',
        'primary_language': 'Java',
        'total_files': 500,
        'total_loc': 150000,
        'frameworks': ['Spring Boot', 'Spring Cloud', 'Kafka', 'Redis'],
        'languages': {'Java': 70.0, 'Kotlin': 20.0, 'YAML': 5.0, 'Shell': 5.0},
        'top_level_dirs': ['services', 'common', 'infrastructure', 'docs']
    }
    
    print("\n📊 Processing repository...")
    
    # Process repository (synchronous)
    result = pipeline.process_repository(repo_data)
    
    # Save output
    output_path = 'repository_summary.md'
    pipeline.save_output(result, output_path, format_type='markdown')
    
    print(f"\n✓ Summary generated successfully")
    print(f"✓ Output saved to: {output_path}")
    
    if result.overview:
        print("\nOverview preview:")
        print("-" * 80)
        print(result.overview[:500] + "...")
    print()


def example_3_comprehensive_analysis():
    """
    Example 3: Comprehensive analysis with all aspects.
    
    This example shows how to analyze all aspects of a repository.
    """
    print("=" * 80)
    print("Example 3: Comprehensive Analysis")
    print("=" * 80)
    
    # Detailed repository data
    repo_data = {
        'name': 'e-commerce-platform',
        'description': 'Full-stack e-commerce platform with microservices architecture',
        'primary_language': 'TypeScript',
        'total_files': 800,
        'total_loc': 250000,
        
        # Structure
        'file_structure': '''
        apps/
        ├── web/          # Next.js frontend
        ├── mobile/       # React Native app
        └── admin/        # Admin dashboard
        services/
        ├── auth/         # Authentication service
        ├── products/     # Product catalog
        ├── orders/       # Order management
        ├── payments/     # Payment processing
        └── notifications/# Notification service
        packages/
        ├── ui/           # Shared UI components
        ├── utils/        # Shared utilities
        └── types/        # TypeScript types
        ''',
        'top_level_dirs': ['apps', 'services', 'packages', 'infrastructure', 'docs'],
        
        # Services
        'service_dirs': ['auth', 'products', 'orders', 'payments', 'notifications'],
        'api_endpoints': [
            'POST /api/auth/login',
            'GET /api/products',
            'POST /api/orders',
            'POST /api/payments/process'
        ],
        
        # Dependencies
        'frameworks': [
            'Next.js', 'React', 'React Native', 'Express.js',
            'NestJS', 'Prisma', 'GraphQL', 'Redis', 'PostgreSQL'
        ],
        'package_dependencies': {
            'next': '^14.0.0',
            'react': '^18.2.0',
            'express': '^4.18.0',
            '@nestjs/core': '^10.0.0',
            'prisma': '^5.0.0'
        },
        
        # Tech stack
        'languages': {
            'TypeScript': 75.0,
            'JavaScript': 15.0,
            'CSS': 5.0,
            'Shell': 3.0,
            'Dockerfile': 2.0
        },
        'build_tools': ['Turborepo', 'Webpack', 'Vite', 'esbuild'],
        'testing_frameworks': ['Jest', 'React Testing Library', 'Cypress', 'Playwright'],
        'cicd_config': ['.github/workflows/ci.yml', '.github/workflows/deploy.yml'],
        
        # Business logic
        'business_modules': [
            'User Authentication',
            'Product Catalog Management',
            'Shopping Cart',
            'Order Processing',
            'Payment Integration',
            'Inventory Management'
        ],
        'domain_models': [
            'User', 'Product', 'Order', 'Payment',
            'Cart', 'Inventory', 'Notification'
        ]
    }
    
    # Initialize summarizer (without AI for this example)
    summarizer = RepositorySummarizer(ai_client=None)
    
    # Create structured data
    structured_data = RepositoryData(**repo_data)
    
    # Generate all prompts
    prompts = summarizer.generate_prompts(structured_data, aspects=None)
    
    print(f"\n✓ Generated prompts for {len(prompts)} aspects:")
    for aspect in prompts.keys():
        print(f"  - {aspect}")
    
    # Export all prompts
    output_path = 'comprehensive_analysis_prompts.txt'
    summarizer.export_prompts(structured_data, output_path)
    print(f"\n✓ All prompts exported to: {output_path}")
    print()


def example_4_custom_configuration():
    """
    Example 4: Using custom configuration.
    
    Shows how to customize the pipeline behavior.
    """
    print("=" * 80)
    print("Example 4: Custom Configuration")
    print("=" * 80)
    
    # Create custom configuration
    config = SummarizationConfig(
        ai_provider=AIProviderConfig(
            provider="openai",
            model="gpt-3.5-turbo",  # Faster, cheaper model
            temperature=0.5,         # More creative
            max_tokens=1500          # Shorter responses
        ),
        aspects=['overview', 'architecture'],  # Only specific aspects
        output_format='json',
        save_prompts=True,
        prompts_output_path='custom_prompts.txt',
        enable_cache=True,
        cache_dir='.cache/custom'
    )
    
    print("\nCustom Configuration:")
    print(json.dumps(config.to_dict(), indent=2))
    
    # You can also load from environment
    env_config = SummarizationConfig.from_env()
    print("\nConfiguration from environment:")
    print(json.dumps(env_config.to_dict(), indent=2))
    print()


def example_5_batch_processing():
    """
    Example 5: Batch processing multiple repositories.
    
    Shows how to process multiple repositories efficiently.
    """
    print("=" * 80)
    print("Example 5: Batch Processing")
    print("=" * 80)
    
    # Multiple repositories to analyze
    repositories = [
        {
            'name': 'frontend-app',
            'primary_language': 'TypeScript',
            'frameworks': ['React', 'Next.js'],
            'total_files': 200
        },
        {
            'name': 'backend-api',
            'primary_language': 'Python',
            'frameworks': ['FastAPI', 'SQLAlchemy'],
            'total_files': 150
        },
        {
            'name': 'mobile-app',
            'primary_language': 'Kotlin',
            'frameworks': ['Android SDK', 'Jetpack Compose'],
            'total_files': 300
        }
    ]
    
    # Initialize summarizer
    summarizer = RepositorySummarizer(ai_client=None)
    
    print(f"\n📦 Processing {len(repositories)} repositories...\n")
    
    for repo in repositories:
        structured_data = RepositoryData(
            name=repo['name'],
            primary_language=repo['primary_language'],
            frameworks=repo['frameworks'],
            total_files=repo['total_files']
        )
        
        # Generate overview prompt
        prompts = summarizer.generate_prompts(
            structured_data,
            aspects=['overview']
        )
        
        print(f"✓ {repo['name']}: Generated overview prompt")
        print(f"  Language: {repo['primary_language']}")
        print(f"  Frameworks: {', '.join(repo['frameworks'])}")
        print()


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("REPOSITORY SUMMARIZATION PIPELINE - EXAMPLES")
    print("=" * 80 + "\n")
    
    # Run examples
    example_1_basic_usage()
    print("\n")
    
    example_2_with_openai()
    print("\n")
    
    example_3_comprehensive_analysis()
    print("\n")
    
    example_4_custom_configuration()
    print("\n")
    
    example_5_batch_processing()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

# Made with Bob
