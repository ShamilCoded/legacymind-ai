"""
Configuration settings for the embeddings pipeline.
"""
from typing import Dict, Any, Optional
from pathlib import Path


class PipelineConfig:
    """Configuration for embeddings pipeline."""
    
    # Model configurations
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    MODELS = {
        'mini': {
            'name': 'all-MiniLM-L6-v2',
            'dimension': 384,
            'description': 'Fast and lightweight model'
        },
        'base': {
            'name': 'all-mpnet-base-v2',
            'dimension': 768,
            'description': 'Balanced performance and quality'
        },
        'large': {
            'name': 'all-distilroberta-v1',
            'dimension': 768,
            'description': 'Best quality, slower'
        },
        'code': {
            'name': 'flax-sentence-embeddings/st-codesearch-distilroberta-base',
            'dimension': 768,
            'description': 'Optimized for code search'
        },
        'multilingual': {
            'name': 'paraphrase-multilingual-MiniLM-L12-v2',
            'dimension': 384,
            'description': 'Supports multiple languages'
        }
    }
    
    # Chunking configurations
    DEFAULT_CHUNK_SIZE = 1000
    DEFAULT_CHUNK_OVERLAP = 200
    
    CHUNK_CONFIGS = {
        'small': {'size': 500, 'overlap': 100},
        'medium': {'size': 1000, 'overlap': 200},
        'large': {'size': 2000, 'overlap': 400}
    }
    
    # Index configurations
    DEFAULT_INDEX_TYPE = 'flat'
    
    INDEX_CONFIGS = {
        'flat': {
            'type': 'flat',
            'description': 'Exact search, best for < 100K vectors',
            'params': {}
        },
        'ivf': {
            'type': 'ivf',
            'description': 'Fast approximate search for large datasets',
            'params': {'nlist': 100}
        },
        'hnsw': {
            'type': 'hnsw',
            'description': 'Hierarchical navigable small world',
            'params': {'M': 32}
        }
    }
    
    # File processing configurations
    DEFAULT_FILE_PATTERNS = [
        '*.py', '*.js', '*.ts', '*.tsx', '*.jsx',
        '*.md', '*.txt', '*.json', '*.yaml', '*.yml',
        '*.java', '*.cpp', '*.c', '*.go', '*.rs'
    ]
    
    DEFAULT_EXCLUDE_PATTERNS = [
        '*/node_modules/*',
        '*/.git/*',
        '*/venv/*',
        '*/__pycache__/*',
        '*/dist/*',
        '*/build/*',
        '*/.next/*',
        '*/target/*'
    ]
    
    # Search configurations
    DEFAULT_SEARCH_K = 5
    DEFAULT_SCORE_THRESHOLD = 0.5
    DEFAULT_CONTEXT_WINDOW = 1
    
    # Storage configurations
    DEFAULT_STORAGE_DIR = './vector_store_data'
    
    @classmethod
    def get_model_config(cls, model_key: str) -> Dict[str, Any]:
        """
        Get model configuration.
        
        Args:
            model_key: Model key ('mini', 'base', etc.)
            
        Returns:
            Model configuration dictionary
        """
        return cls.MODELS.get(model_key, cls.MODELS['mini'])
    
    @classmethod
    def get_chunk_config(cls, size_key: str) -> Dict[str, int]:
        """
        Get chunk configuration.
        
        Args:
            size_key: Size key ('small', 'medium', 'large')
            
        Returns:
            Chunk configuration dictionary
        """
        return cls.CHUNK_CONFIGS.get(size_key, cls.CHUNK_CONFIGS['medium'])
    
    @classmethod
    def get_index_config(cls, index_key: str) -> Dict[str, Any]:
        """
        Get index configuration.
        
        Args:
            index_key: Index key ('flat', 'ivf', 'hnsw')
            
        Returns:
            Index configuration dictionary
        """
        return cls.INDEX_CONFIGS.get(index_key, cls.INDEX_CONFIGS['flat'])
    
    @classmethod
    def create_custom_config(
        cls,
        model_key: str = 'mini',
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        index_type: str = 'flat',
        storage_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a custom configuration.
        
        Args:
            model_key: Model to use
            chunk_size: Custom chunk size
            chunk_overlap: Custom chunk overlap
            index_type: Index type to use
            storage_dir: Storage directory
            
        Returns:
            Configuration dictionary
        """
        model_config = cls.get_model_config(model_key)
        index_config = cls.get_index_config(index_type)
        
        return {
            'model': {
                'key': model_key,
                'name': model_config['name'],
                'dimension': model_config['dimension']
            },
            'chunking': {
                'size': chunk_size or cls.DEFAULT_CHUNK_SIZE,
                'overlap': chunk_overlap or cls.DEFAULT_CHUNK_OVERLAP
            },
            'index': {
                'type': index_type,
                'params': index_config['params']
            },
            'storage': {
                'directory': storage_dir or cls.DEFAULT_STORAGE_DIR
            },
            'search': {
                'default_k': cls.DEFAULT_SEARCH_K,
                'score_threshold': cls.DEFAULT_SCORE_THRESHOLD,
                'context_window': cls.DEFAULT_CONTEXT_WINDOW
            },
            'processing': {
                'file_patterns': cls.DEFAULT_FILE_PATTERNS,
                'exclude_patterns': cls.DEFAULT_EXCLUDE_PATTERNS
            }
        }


class LoggingConfig:
    """Logging configuration."""
    
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'embeddings_pipeline.log'
    
    @classmethod
    def setup_logging(cls, log_level: str = None, log_file: str = None):
        """
        Setup logging configuration.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            log_file: Log file path
        """
        import logging
        
        level = getattr(logging, log_level or cls.LOG_LEVEL)
        file = log_file or cls.LOG_FILE
        
        logging.basicConfig(
            level=level,
            format=cls.LOG_FORMAT,
            handlers=[
                logging.FileHandler(file),
                logging.StreamHandler()
            ]
        )


# Preset configurations for common use cases
PRESET_CONFIGS = {
    'fast': {
        'description': 'Fast processing with mini model',
        'model_key': 'mini',
        'chunk_size': 800,
        'chunk_overlap': 150,
        'index_type': 'flat'
    },
    'balanced': {
        'description': 'Balanced performance and quality',
        'model_key': 'base',
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'index_type': 'flat'
    },
    'quality': {
        'description': 'Best quality, slower processing',
        'model_key': 'large',
        'chunk_size': 1200,
        'chunk_overlap': 250,
        'index_type': 'flat'
    },
    'code': {
        'description': 'Optimized for code repositories',
        'model_key': 'code',
        'chunk_size': 800,
        'chunk_overlap': 150,
        'index_type': 'flat'
    },
    'large_scale': {
        'description': 'For large repositories (> 100K chunks)',
        'model_key': 'mini',
        'chunk_size': 1000,
        'chunk_overlap': 200,
        'index_type': 'ivf'
    }
}


def get_preset_config(preset_name: str) -> Dict[str, Any]:
    """
    Get a preset configuration.
    
    Args:
        preset_name: Name of preset ('fast', 'balanced', 'quality', etc.)
        
    Returns:
        Configuration dictionary
    """
    if preset_name not in PRESET_CONFIGS:
        raise ValueError(f"Unknown preset: {preset_name}. "
                        f"Available: {list(PRESET_CONFIGS.keys())}")
    
    preset = PRESET_CONFIGS[preset_name]
    return PipelineConfig.create_custom_config(
        model_key=preset['model_key'],
        chunk_size=preset['chunk_size'],
        chunk_overlap=preset['chunk_overlap'],
        index_type=preset['index_type']
    )

# Made with Bob
