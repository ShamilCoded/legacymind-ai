"""
Vector store service using FAISS for efficient similarity search.
"""
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import faiss
import pickle
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class VectorStore:
    """FAISS-based vector store for efficient similarity search."""
    
    def __init__(
        self,
        dimension: int,
        index_type: str = "flat",
        metric: str = "cosine"
    ):
        """
        Initialize the vector store.
        
        Args:
            dimension: Dimension of the embedding vectors
            index_type: Type of FAISS index ('flat', 'ivf', 'hnsw')
            metric: Distance metric ('cosine', 'l2', 'ip')
        """
        self.dimension = dimension
        self.index_type = index_type
        self.metric = metric
        
        # Initialize FAISS index
        self.index = self._create_index()
        
        # Store metadata separately (FAISS only stores vectors)
        self.metadata: List[Dict[str, Any]] = []
        self.id_to_index: Dict[str, int] = {}
        self.next_id = 0
        
        logger.info(f"Initialized {index_type} vector store with dimension {dimension}")
    
    def _create_index(self) -> faiss.Index:
        """
        Create FAISS index based on configuration.
        
        Returns:
            FAISS index
        """
        if self.index_type == "flat":
            # Flat index - exact search, no training needed
            if self.metric == "cosine":
                # For cosine similarity, use inner product with normalized vectors
                index = faiss.IndexFlatIP(self.dimension)
            elif self.metric == "l2":
                index = faiss.IndexFlatL2(self.dimension)
            else:  # inner product
                index = faiss.IndexFlatIP(self.dimension)
                
        elif self.index_type == "ivf":
            # IVF index - faster search with some accuracy tradeoff
            nlist = 100  # number of clusters
            quantizer = faiss.IndexFlatL2(self.dimension)
            
            if self.metric == "cosine":
                index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist, faiss.METRIC_INNER_PRODUCT)
            else:
                index = faiss.IndexIVFFlat(quantizer, self.dimension, nlist, faiss.METRIC_L2)
                
        elif self.index_type == "hnsw":
            # HNSW index - hierarchical navigable small world
            M = 32  # number of connections per layer
            index = faiss.IndexHNSWFlat(self.dimension, M)
            
            if self.metric == "cosine":
                index.metric_type = faiss.METRIC_INNER_PRODUCT
            else:
                index.metric_type = faiss.METRIC_L2
        else:
            raise ValueError(f"Unknown index type: {self.index_type}")
        
        return index
    
    def add_vectors(
        self,
        embeddings: np.ndarray,
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add vectors to the store.
        
        Args:
            embeddings: Array of embeddings (shape: [n_vectors, dimension])
            metadata: List of metadata dicts for each vector
            ids: Optional list of IDs for vectors
            
        Returns:
            List of assigned IDs
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Number of embeddings must match number of metadata entries")
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype(np.float32)
        
        # Normalize for cosine similarity
        if self.metric == "cosine":
            faiss.normalize_L2(embeddings)
        
        # Train index if needed (for IVF)
        if self.index_type == "ivf" and not self.index.is_trained:
            logger.info("Training IVF index...")
            self.index.train(embeddings)
            logger.info("Index trained")
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"vec_{self.next_id + i}" for i in range(len(embeddings))]
        
        # Add to FAISS index
        start_idx = len(self.metadata)
        self.index.add(embeddings)
        
        # Store metadata and ID mappings
        for i, (meta, vec_id) in enumerate(zip(metadata, ids)):
            idx = start_idx + i
            self.metadata.append(meta)
            self.id_to_index[vec_id] = idx
        
        self.next_id += len(embeddings)
        
        logger.info(f"Added {len(embeddings)} vectors. Total: {self.index.ntotal}")
        return ids
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = 5,
        return_scores: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            return_scores: Whether to include similarity scores
            
        Returns:
            List of results with metadata and optional scores
        """
        if self.index.ntotal == 0:
            return []
        
        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype(np.float32)
        
        # Normalize for cosine similarity
        if self.metric == "cosine":
            faiss.normalize_L2(query_embedding)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
            
            result = {
                'metadata': self.metadata[idx].copy(),
                'index': int(idx)
            }
            
            if return_scores:
                # Convert distance to similarity score
                if self.metric == "cosine":
                    score = float(dist)  # Already similarity for IP
                else:  # L2 distance
                    score = 1.0 / (1.0 + float(dist))
                result['score'] = score
            
            results.append(result)
        
        return results
    
    def search_batch(
        self,
        query_embeddings: np.ndarray,
        k: int = 5,
        return_scores: bool = True
    ) -> List[List[Dict[str, Any]]]:
        """
        Search for similar vectors for multiple queries.
        
        Args:
            query_embeddings: Array of query embeddings (shape: [n_queries, dimension])
            k: Number of results per query
            return_scores: Whether to include similarity scores
            
        Returns:
            List of result lists, one per query
        """
        if self.index.ntotal == 0:
            return [[] for _ in range(len(query_embeddings))]
        
        # Ensure float32
        query_embeddings = query_embeddings.astype(np.float32)
        
        # Normalize for cosine similarity
        if self.metric == "cosine":
            faiss.normalize_L2(query_embeddings)
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_embeddings, k)
        
        # Prepare results for each query
        all_results = []
        for query_distances, query_indices in zip(distances, indices):
            results = []
            for dist, idx in zip(query_distances, query_indices):
                if idx == -1:
                    continue
                
                result = {
                    'metadata': self.metadata[idx].copy(),
                    'index': int(idx)
                }
                
                if return_scores:
                    if self.metric == "cosine":
                        score = float(dist)
                    else:
                        score = 1.0 / (1.0 + float(dist))
                    result['score'] = score
                
                results.append(result)
            
            all_results.append(results)
        
        return all_results
    
    def get_by_id(self, vec_id: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata by vector ID.
        
        Args:
            vec_id: Vector ID
            
        Returns:
            Metadata dict or None if not found
        """
        idx = self.id_to_index.get(vec_id)
        if idx is None:
            return None
        return self.metadata[idx].copy()
    
    def delete_by_id(self, vec_id: str) -> bool:
        """
        Delete vector by ID (marks as deleted in metadata).
        Note: FAISS doesn't support true deletion, so we mark in metadata.
        
        Args:
            vec_id: Vector ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        idx = self.id_to_index.get(vec_id)
        if idx is None:
            return False
        
        self.metadata[idx]['_deleted'] = True
        return True
    
    def save(self, directory: str) -> None:
        """
        Save vector store to disk.
        
        Args:
            directory: Directory to save to
        """
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = dir_path / "index.faiss"
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata
        metadata_path = dir_path / "metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'id_to_index': self.id_to_index,
                'next_id': self.next_id
            }, f)
        
        # Save config
        config_path = dir_path / "config.json"
        with open(config_path, 'w') as f:
            json.dump({
                'dimension': self.dimension,
                'index_type': self.index_type,
                'metric': self.metric
            }, f, indent=2)
        
        logger.info(f"Saved vector store to {directory}")
    
    @classmethod
    def load(cls, directory: str) -> 'VectorStore':
        """
        Load vector store from disk.
        
        Args:
            directory: Directory to load from
            
        Returns:
            Loaded VectorStore instance
        """
        dir_path = Path(directory)
        
        # Load config
        config_path = dir_path / "config.json"
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Create instance
        store = cls(
            dimension=config['dimension'],
            index_type=config['index_type'],
            metric=config['metric']
        )
        
        # Load FAISS index
        index_path = dir_path / "index.faiss"
        store.index = faiss.read_index(str(index_path))
        
        # Load metadata
        metadata_path = dir_path / "metadata.pkl"
        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)
            store.metadata = data['metadata']
            store.id_to_index = data['id_to_index']
            store.next_id = data['next_id']
        
        logger.info(f"Loaded vector store from {directory}")
        return store
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_vectors': self.index.ntotal,
            'dimension': self.dimension,
            'index_type': self.index_type,
            'metric': self.metric,
            'metadata_count': len(self.metadata),
            'is_trained': self.index.is_trained if hasattr(self.index, 'is_trained') else True
        }

# Made with Bob
