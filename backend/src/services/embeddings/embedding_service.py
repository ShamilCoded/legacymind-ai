from typing import List, Dict, Any, Union
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """Service for generating embeddings using sentence-transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)

    def encode_text(self, text: Union[str, List[str]], normalize: bool = True, show_progress: bool = False) -> np.ndarray:
        """Encode text to embeddings."""
        if isinstance(text, str):
            text = [text]
        embeddings = self.model.encode(
            text,
            normalize_embeddings=normalize,
            show_progress_bar=show_progress
        )
        return np.array(embeddings, dtype=np.float32)

    def encode_chunks(self, chunks: List[Dict[str, Any]], text_key: str = 'text', normalize: bool = True, show_progress: bool = False) -> np.ndarray:
        """Encode multiple chunks."""
        texts = [chunk[text_key] for chunk in chunks]
        return self.encode_text(texts, normalize=normalize, show_progress=show_progress)

    def encode_query(self, query: str, normalize: bool = True) -> np.ndarray:
        """Encode search query."""
        # Typically query is returned as a 1D array from SentenceTransformer, but we need it formatted similarly
        return self.encode_text(query, normalize=normalize)[0]

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        # Since we use normalized embeddings, cosine similarity is just the dot product
        if len(embedding1.shape) > 1:
            embedding1 = embedding1.flatten()
        if len(embedding2.shape) > 1:
            embedding2 = embedding2.flatten()
        return float(np.dot(embedding1, embedding2))

    def get_embedding_dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_sentence_embedding_dimension()
