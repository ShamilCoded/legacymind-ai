import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

from .embedding_service import EmbeddingService
from ..vector_store.vector_store import VectorStore
from ..vector_store.retrieval import SemanticRetriever
from ...utils.chunking import FileChunker

class EmbeddingsPipeline:
    """Main pipeline orchestrator for document embeddings and search."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        # Fix argument order for SemanticRetriever based on error logs
        self.retriever = SemanticRetriever(embedding_service=embedding_service, vector_store=vector_store)
        self.file_chunker = FileChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def process_file(self, file_path: str, content: str, file_type: Optional[str] = None) -> int:
        """Process a file and add it to the vector store."""
        # 1. Chunk the file
        chunks = self.file_chunker.chunk_file(content, file_path)
        if not chunks:
            return 0

        # 2. Extract texts and metadata
        texts = [chunk['text'] for chunk in chunks]
        metadata = []
        for chunk in chunks:
            meta = chunk['metadata'].copy() if chunk.get('metadata') else {}
            meta['text'] = chunk['text']
            metadata.append(meta)

        # 3. Create embeddings
        embeddings = self.embedding_service.encode_text(texts)

        # 4. Store in vector store
        self.vector_store.add_vectors(embeddings, metadata)

        return len(chunks)

    def process_directory(self, directory: str, file_patterns: List[str] = None, exclude_patterns: List[str] = None, recursive: bool = True) -> List[Any]:
        """Process an entire directory."""
        import glob
        import fnmatch
        processed = []

        path_pattern = f"{directory}/**/*" if recursive else f"{directory}/*"
        for filepath in glob.glob(path_pattern, recursive=recursive):
            if os.path.isfile(filepath):
                if file_patterns and not any(fnmatch.fnmatch(filepath, p) for p in file_patterns):
                    continue
                if exclude_patterns and any(fnmatch.fnmatch(filepath, p) for p in exclude_patterns):
                    continue

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.process_file(filepath, content)
                    processed.append(filepath)
                except Exception:
                    pass
        return processed

    def search(self, query: str, k: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Semantic search."""
        return self.retriever.search(query, k=k, **kwargs)

    def search_with_context(self, query: str, k: int = 5, context_window: int = 1) -> List[Dict[str, Any]]:
        """Search with surrounding chunk context."""
        return self.retriever.search_with_context(query, k=k, context_window=context_window)

    def get_stats(self) -> Dict[str, Any]:
        """Get pipeline statistics."""
        return {
            'vector_store': self.vector_store.get_stats(),
            'embedding_model': self.embedding_service.model_name,
            'embedding_dimension': self.embedding_service.get_embedding_dimension()
        }

    def save(self, directory: str):
        """Save the pipeline state."""
        os.makedirs(directory, exist_ok=True)

        # Save vector store config explicitly because vector_store.save only saves its internal data
        self.vector_store.save(directory)
        # However vector_store.load actually reads config from directory, but wait vector store load expects config!
        # Checking how vector_store saves its config in its own class...
        # Wait, the error was "KeyError: 'dimension'". The vector store might not be saving config.json properly or expects pipeline to do it.
        # Let's save a config.json that contains the vector store kwargs as well
        config = {
            'model_name': self.embedding_service.model_name,
            'chunk_size': self.file_chunker.chunk_size,
            'chunk_overlap': self.file_chunker.chunk_overlap,
            'dimension': self.vector_store.dimension,
            'index_type': self.vector_store.index_type,
            'metric': self.vector_store.metric
        }
        with open(os.path.join(directory, 'config.json'), 'w') as f:
            json.dump(config, f)

    @classmethod
    def load(cls, directory: str) -> 'EmbeddingsPipeline':
        """Load the pipeline state."""
        # Load config
        with open(os.path.join(directory, 'config.json'), 'r') as f:
            config = json.load(f)

        # Initialize services
        embedding_service = EmbeddingService(model_name=config.get('model_name', 'all-MiniLM-L6-v2'))

        # Load vector store
        # we know vector_store.load will use the same config.json to read dimension, index_type, metric
        vector_store = VectorStore.load(directory)

        # Create and return pipeline
        return cls(
            embedding_service=embedding_service,
            vector_store=vector_store,
            chunk_size=config.get('chunk_size', 1000),
            chunk_overlap=config.get('chunk_overlap', 200)
        )

def create_pipeline(
    model_key: str = 'mini',
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    index_type: str = 'flat'
) -> EmbeddingsPipeline:
    """Factory to create an embeddings pipeline."""
    model_map = {
        'mini': 'all-MiniLM-L6-v2',
        'base': 'all-mpnet-base-v2',
        'large': 'all-distilroberta-v1',
        'code': 'st-codesearch-distilroberta-base',
        'multilingual': 'paraphrase-multilingual-MiniLM-L12-v2'
    }

    model_name = model_map.get(model_key, 'all-MiniLM-L6-v2')

    embedding_service = EmbeddingService(model_name=model_name)
    dimension = embedding_service.get_embedding_dimension()

    vector_store = VectorStore(dimension=dimension, index_type=index_type)

    return EmbeddingsPipeline(
        embedding_service=embedding_service,
        vector_store=vector_store,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
