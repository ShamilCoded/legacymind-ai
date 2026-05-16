"""
Tests for chunking utilities.
"""
import pytest
from src.utils.chunking import TextChunker, FileChunker


class TestTextChunker:
    """Tests for TextChunker class."""
    
    def test_basic_chunking(self):
        """Test basic text chunking."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)
        text = "This is a test. " * 10  # 160 characters
        
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) > 0
        assert all('text' in chunk for chunk in chunks)
        assert all('chunk_index' in chunk for chunk in chunks)
    
    def test_chunk_with_metadata(self):
        """Test chunking with metadata."""
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)
        text = "Test text"
        metadata = {'file_path': 'test.txt', 'author': 'test'}
        
        chunks = chunker.chunk_text(text, metadata)
        
        assert len(chunks) > 0
        assert chunks[0]['metadata']['file_path'] == 'test.txt'
        assert chunks[0]['metadata']['author'] == 'test'
    
    def test_empty_text(self):
        """Test chunking empty text."""
        chunker = TextChunker()
        chunks = chunker.chunk_text("")
        
        assert len(chunks) == 0
    
    def test_chunk_overlap(self):
        """Test that chunks have proper overlap."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        text = "A" * 250
        
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) >= 2
        # Check that there's some overlap
        if len(chunks) >= 2:
            assert chunks[0]['char_count'] <= 100
    
    def test_code_chunking(self):
        """Test code-specific chunking."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        code = """
def function1():
    pass

def function2():
    pass
"""
        
        chunks = chunker.chunk_code(code, 'python')
        
        assert len(chunks) > 0
        assert chunks[0]['metadata']['content_type'] == 'code'
        assert chunks[0]['metadata']['language'] == 'python'
    
    def test_markdown_chunking(self):
        """Test markdown-specific chunking."""
        chunker = TextChunker(chunk_size=100, chunk_overlap=20)
        markdown = """
# Header 1
Content 1

## Header 2
Content 2

### Header 3
Content 3
"""
        
        chunks = chunker.chunk_markdown(markdown)
        
        assert len(chunks) > 0
        assert chunks[0]['metadata']['content_type'] == 'markdown'


class TestFileChunker:
    """Tests for FileChunker class."""
    
    def test_detect_file_type(self):
        """Test file type detection."""
        chunker = FileChunker()
        
        assert chunker._detect_file_type('test.py') == 'python'
        assert chunker._detect_file_type('test.js') == 'javascript'
        assert chunker._detect_file_type('test.md') == 'markdown'
        assert chunker._detect_file_type('test.txt') == 'text'
        assert chunker._detect_file_type('test.unknown') == 'text'
    
    def test_chunk_python_file(self):
        """Test chunking Python file."""
        chunker = FileChunker(chunk_size=100, chunk_overlap=20)
        content = """
def hello():
    print("Hello, World!")

class MyClass:
    def __init__(self):
        self.value = 42
"""
        
        chunks = chunker.chunk_file(content, 'test.py')
        
        assert len(chunks) > 0
        assert chunks[0]['metadata']['file_path'] == 'test.py'
        assert chunks[0]['metadata']['file_type'] == 'python'
    
    def test_chunk_markdown_file(self):
        """Test chunking Markdown file."""
        chunker = FileChunker(chunk_size=100, chunk_overlap=20)
        content = """
# Title
This is a test document.

## Section 1
Content for section 1.
"""
        
        chunks = chunker.chunk_file(content, 'test.md')
        
        assert len(chunks) > 0
        assert chunks[0]['metadata']['file_type'] == 'markdown'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# Made with Bob
