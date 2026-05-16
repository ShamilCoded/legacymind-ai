"""
Chunking utilities for processing large files into manageable segments.
"""
from typing import List, Dict, Any
import re


class TextChunker:
    """Handles chunking of text content with overlap for context preservation."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separator: str = "\n\n"
    ):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
            separator: Primary separator for splitting text
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Text content to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        if not text:
            return []
            
        chunks = []
        metadata = metadata or {}
        
        # Split by separator first
        splits = text.split(self.separator)
        
        current_chunk = ""
        chunk_index = 0
        
        for split in splits:
            # If adding this split would exceed chunk_size, save current chunk
            if len(current_chunk) + len(split) > self.chunk_size and current_chunk:
                chunks.append(self._create_chunk_dict(
                    current_chunk.strip(),
                    chunk_index,
                    metadata
                ))
                chunk_index += 1
                
                # Start new chunk with overlap from previous
                if self.chunk_overlap > 0:
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    current_chunk = overlap_text + self.separator + split
                else:
                    current_chunk = split
            else:
                # Add to current chunk
                if current_chunk:
                    current_chunk += self.separator + split
                else:
                    current_chunk = split
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(self._create_chunk_dict(
                current_chunk.strip(),
                chunk_index,
                metadata
            ))
        
        return chunks
    
    def chunk_code(self, code: str, language: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Chunk code while trying to preserve logical boundaries (functions, classes).
        
        Args:
            code: Code content to chunk
            language: Programming language (python, javascript, etc.)
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        metadata = metadata or {}
        metadata['content_type'] = 'code'
        metadata['language'] = language
        
        # For code, use double newline as separator to preserve logical blocks
        return self.chunk_text(code, metadata)
    
    def chunk_markdown(self, markdown: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Chunk markdown while preserving section boundaries.
        
        Args:
            markdown: Markdown content to chunk
            metadata: Optional metadata to attach to each chunk
            
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        metadata = metadata or {}
        metadata['content_type'] = 'markdown'
        
        # Split by headers first
        sections = re.split(r'\n(?=#{1,6}\s)', markdown)
        
        chunks = []
        chunk_index = 0
        
        for section in sections:
            if not section.strip():
                continue
                
            # If section is larger than chunk_size, split it further
            if len(section) > self.chunk_size:
                section_chunks = self.chunk_text(section, metadata)
                for chunk in section_chunks:
                    chunk['chunk_index'] = chunk_index
                    chunks.append(chunk)
                    chunk_index += 1
            else:
                chunks.append(self._create_chunk_dict(
                    section.strip(),
                    chunk_index,
                    metadata
                ))
                chunk_index += 1
        
        return chunks
    
    def _create_chunk_dict(
        self,
        text: str,
        chunk_index: int,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a standardized chunk dictionary.
        
        Args:
            text: Chunk text content
            chunk_index: Index of this chunk
            metadata: Metadata to include
            
        Returns:
            Dictionary with chunk data
        """
        return {
            'text': text,
            'chunk_index': chunk_index,
            'char_count': len(text),
            'metadata': metadata.copy()
        }


class FileChunker:
    """Handles chunking of various file types."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the file chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.text_chunker = TextChunker(chunk_size, chunk_overlap)
        
    def chunk_file(
        self,
        content: str,
        file_path: str,
        file_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Chunk file content based on file type.
        
        Args:
            content: File content as string
            file_path: Path to the file
            file_type: Type of file (auto-detected from extension if not provided)
            
        Returns:
            List of chunk dictionaries
        """
        if file_type is None:
            file_type = self._detect_file_type(file_path)
        
        base_metadata = {
            'file_path': file_path,
            'file_type': file_type
        }
        
        # Route to appropriate chunking method
        if file_type == 'markdown':
            return self.text_chunker.chunk_markdown(content, base_metadata)
        elif file_type in ['python', 'javascript', 'typescript', 'java', 'cpp', 'go']:
            return self.text_chunker.chunk_code(content, file_type, base_metadata)
        else:
            return self.text_chunker.chunk_text(content, base_metadata)
    
    def _detect_file_type(self, file_path: str) -> str:
        """
        Detect file type from extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string
        """
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.md': 'markdown',
            '.txt': 'text',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
        }
        
        for ext, file_type in extension_map.items():
            if file_path.endswith(ext):
                return file_type
        
        return 'text'

# Made with Bob
