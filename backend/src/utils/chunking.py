import re
from typing import List, Dict, Any, Optional

class TextChunker:
    """Utility class for chunking text, code, and markdown."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, separator: str = "\n\n"):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator
        
    def chunk_text(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            # Find the end of the chunk
            end = start + self.chunk_size

            # If we're not at the end of the text, try to find a natural break
            if end < text_len:
                # Try to find a newline or space within the overlap region
                overlap_region = text[max(start, end - self.chunk_overlap):end]
                last_newline = overlap_region.rfind('\n')
                if last_newline != -1:
                    end = max(start, end - self.chunk_overlap) + last_newline + 1
                else:
                    last_space = overlap_region.rfind(' ')
                    if last_space != -1:
                        end = max(start, end - self.chunk_overlap) + last_space + 1
            
            chunk_text = text[start:end]
            
            chunk_data = {
                'text': chunk_text,
                'chunk_index': len(chunks),
                'char_count': len(chunk_text),
                'metadata': metadata.copy() if metadata else {}
            }
            chunks.append(chunk_data)
            
            # Move start forward, accounting for overlap
            start = end - self.chunk_overlap if end < text_len else end

            # Ensure we always make progress to avoid infinite loops
            if start <= chunks[-1]['chunk_index'] * (self.chunk_size - self.chunk_overlap):
                start = end

        return chunks

    def chunk_code(self, code: str, language: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        meta = metadata.copy() if metadata else {}
        meta['content_type'] = 'code'
        meta['language'] = language
        return self.chunk_text(code, meta)

    def chunk_markdown(self, markdown: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        meta = metadata.copy() if metadata else {}
        meta['content_type'] = 'markdown'
        return self.chunk_text(markdown, meta)


class FileChunker:
    """Utility class for chunking files based on type."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_chunker = TextChunker(chunk_size, chunk_overlap)
        
    def _detect_file_type(self, file_path: str) -> str:
        ext = file_path.split('.')[-1].lower() if '.' in file_path else ''
        
        language_map = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'go': 'go',
            'rs': 'rust',
            'md': 'markdown'
        }
        
        if ext in language_map:
            return language_map[ext]
        return 'text'

    def chunk_file(self, content: str, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        file_type = self._detect_file_type(file_path)

        meta = metadata.copy() if metadata else {}
        meta['file_path'] = file_path
        meta['file_type'] = file_type

        if file_type == 'markdown':
            return self.text_chunker.chunk_markdown(content, meta)
        elif file_type == 'text':
            return self.text_chunker.chunk_text(content, meta)
        else:
            return self.text_chunker.chunk_code(content, file_type, meta)
