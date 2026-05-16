"""
Integration tests for the embeddings pipeline.
"""
import pytest
import numpy as np
import tempfile
import shutil
from pathlib import Path
from src.services.embeddings import create_pipeline, EmbeddingsPipeline


class TestEmbeddingsPipeline:
    """Tests for EmbeddingsPipeline class."""
    
    @pytest.fixture
    def pipeline(self):
        """Create a test pipeline."""
        return create_pipeline(
            model_key='mini',
            chunk_size=100,
            chunk_overlap=20,
            index_type='flat'
        )
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_pipeline_creation(self, pipeline):
        """Test pipeline initialization."""
        assert pipeline is not None
        assert pipeline.embedding_service is not None
        assert pipeline.vector_store is not None
        assert pipeline.retriever is not None
    
    def test_process_file(self, pipeline):
        """Test processing a single file."""
        content = """
# Test Document

This is a test document for the embeddings pipeline.

## Section 1
Content for section 1.

## Section 2
Content for section 2.
"""
        
        chunk_count = pipeline.process_file(
            file_path='test.md',
            content=content
        )
        
        assert chunk_count > 0
        stats = pipeline.get_stats()
        assert stats['vector_store']['total_vectors'] == chunk_count
    
    def test_search(self, pipeline):
        """Test search functionality."""
        # Add some content
        content = """
# Installation Guide

To install the package, run:
pip install embeddings-pipeline

## Requirements
- Python 3.8+
- CUDA (optional)
"""
        
        pipeline.process_file('install.md', content)
        
        # Search
        results = pipeline.search("how to install", k=2)
        
        assert len(results) > 0
        assert 'score' in results[0]
        assert 'metadata' in results[0]
    
    def test_search_with_context(self, pipeline):
        """Test search with context."""
        content = """
# Chapter 1
Introduction to the topic.

# Chapter 2
Main content here.

# Chapter 3
Conclusion and summary.
"""
        
        pipeline.process_file('doc.md', content)
        
        results = pipeline.search_with_context(
            "main content",
            k=1,
            context_window=1
        )
        
        assert len(results) > 0
        # Context may or may not be present depending on chunk structure
    
    def test_save_and_load(self, pipeline, temp_dir):
        """Test saving and loading pipeline."""
        # Add content
        content = "Test content for save and load."
        pipeline.process_file('test.txt', content)
        
        # Save
        save_path = Path(temp_dir) / "pipeline_data"
        pipeline.save(str(save_path))
        
        assert save_path.exists()
        assert (save_path / "index.faiss").exists()
        assert (save_path / "metadata.pkl").exists()
        assert (save_path / "config.json").exists()
        
        # Load
        loaded_pipeline = EmbeddingsPipeline.load(str(save_path))
        
        assert loaded_pipeline is not None
        loaded_stats = loaded_pipeline.get_stats()
        original_stats = pipeline.get_stats()
        
        assert loaded_stats['vector_store']['total_vectors'] == \
               original_stats['vector_store']['total_vectors']
    
    def test_get_stats(self, pipeline):
        """Test getting pipeline statistics."""
        stats = pipeline.get_stats()
        
        assert 'vector_store' in stats
        assert 'embedding_model' in stats
        assert 'embedding_dimension' in stats
        assert stats['embedding_dimension'] > 0
    
    def test_empty_search(self, pipeline):
        """Test search on empty index."""
        results = pipeline.search("test query", k=5)
        
        assert len(results) == 0
    
    def test_multiple_files(self, pipeline):
        """Test processing multiple files."""
        files = {
            'file1.txt': 'Content of file 1',
            'file2.txt': 'Content of file 2',
            'file3.txt': 'Content of file 3'
        }
        
        total_chunks = 0
        for file_path, content in files.items():
            chunks = pipeline.process_file(file_path, content)
            total_chunks += chunks
        
        stats = pipeline.get_stats()
        assert stats['vector_store']['total_vectors'] == total_chunks


class TestPipelineFactory:
    """Tests for pipeline factory function."""
    
    def test_create_mini_pipeline(self):
        """Test creating mini model pipeline."""
        pipeline = create_pipeline(model_key='mini')
        assert pipeline.embedding_service.model_name == 'all-MiniLM-L6-v2'
    
    def test_create_with_custom_params(self):
        """Test creating pipeline with custom parameters."""
        pipeline = create_pipeline(
            model_key='mini',
            chunk_size=500,
            chunk_overlap=100,
            index_type='flat'
        )
        
        assert pipeline.file_chunker.chunk_size == 500
        assert pipeline.file_chunker.chunk_overlap == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
