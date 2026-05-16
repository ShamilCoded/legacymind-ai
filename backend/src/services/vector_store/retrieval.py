"""
Retrieval functions for semantic search over vector stores.
"""
from typing import List, Dict, Any, Optional, Callable
import numpy as np
from .vector_store import VectorStore
from ..embeddings.embedding_service import EmbeddingService
import logging

logger = logging.getLogger(__name__)


class SemanticRetriever:
    """Handles semantic search and retrieval operations."""
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):
        """
        Initialize the semantic retriever.
        
        Args:
            embedding_service: Service for generating embeddings
            vector_store: Vector store for similarity search
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
    
    def search(
        self,
        query: str,
        k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search.
        
        Args:
            query: Search query text
            k: Number of results to return
            filters: Optional metadata filters
            score_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of search results with metadata and scores
        """
        # Generate query embedding
        query_embedding = self.embedding_service.encode_query(query)
        
        # Search vector store (get more results if filtering)
        search_k = k * 3 if filters else k
        results = self.vector_store.search(
            query_embedding,
            k=search_k,
            return_scores=True
        )
        
        # Apply filters
        if filters:
            results = self._apply_filters(results, filters)
        
        # Apply score threshold
        if score_threshold is not None:
            results = [r for r in results if r.get('score', 0) >= score_threshold]
        
        # Limit to k results
        results = results[:k]
        
        return results
    
    def search_with_context(
        self,
        query: str,
        k: int = 5,
        context_window: int = 1,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search with surrounding context chunks.
        
        Args:
            query: Search query text
            k: Number of results to return
            context_window: Number of chunks before/after to include
            filters: Optional metadata filters
            
        Returns:
            List of results with context
        """
        # Perform basic search
        results = self.search(query, k=k, filters=filters)
        
        # Add context for each result
        results_with_context = []
        for result in results:
            result_with_context = result.copy()
            
            # Get chunk index from metadata
            chunk_idx = result['metadata'].get('chunk_index')
            file_path = result['metadata'].get('file_path')
            
            if chunk_idx is not None and file_path is not None:
                # Find surrounding chunks
                context_chunks = self._get_context_chunks(
                    file_path,
                    chunk_idx,
                    context_window
                )
                result_with_context['context'] = context_chunks
            
            results_with_context.append(result_with_context)
        
        return results_with_context
    
    def search_by_file(
        self,
        query: str,
        file_path: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search within a specific file.
        
        Args:
            query: Search query text
            file_path: Path to file to search within
            k: Number of results to return
            
        Returns:
            List of search results from the file
        """
        filters = {'file_path': file_path}
        return self.search(query, k=k, filters=filters)
    
    def search_by_type(
        self,
        query: str,
        content_type: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search within specific content type.
        
        Args:
            query: Search query text
            content_type: Type of content (code, markdown, text, etc.)
            k: Number of results to return
            
        Returns:
            List of search results of the specified type
        """
        filters = {'content_type': content_type}
        return self.search(query, k=k, filters=filters)
    
    def multi_query_search(
        self,
        queries: List[str],
        k: int = 5,
        aggregation: str = "max"
    ) -> List[Dict[str, Any]]:
        """
        Search using multiple queries and aggregate results.
        
        Args:
            queries: List of query strings
            k: Number of results to return
            aggregation: How to aggregate scores ('max', 'mean', 'sum')
            
        Returns:
            Aggregated search results
        """
        # Generate embeddings for all queries
        query_embeddings = self.embedding_service.encode_text(queries)
        
        # Search with all queries
        all_results = self.vector_store.search_batch(
            query_embeddings,
            k=k * 2,  # Get more results for aggregation
            return_scores=True
        )
        
        # Aggregate results by index
        index_to_results: Dict[int, List[float]] = {}
        index_to_metadata: Dict[int, Dict[str, Any]] = {}
        
        for results in all_results:
            for result in results:
                idx = result['index']
                score = result['score']
                
                if idx not in index_to_results:
                    index_to_results[idx] = []
                    index_to_metadata[idx] = result['metadata']
                
                index_to_results[idx].append(score)
        
        # Compute aggregated scores
        aggregated_results = []
        for idx, scores in index_to_results.items():
            if aggregation == "max":
                agg_score = max(scores)
            elif aggregation == "mean":
                agg_score = sum(scores) / len(scores)
            elif aggregation == "sum":
                agg_score = sum(scores)
            else:
                agg_score = max(scores)
            
            aggregated_results.append({
                'metadata': index_to_metadata[idx],
                'index': idx,
                'score': agg_score,
                'query_scores': scores
            })
        
        # Sort by aggregated score
        aggregated_results.sort(key=lambda x: x['score'], reverse=True)
        
        return aggregated_results[:k]
    
    def hybrid_search(
        self,
        query: str,
        keyword_filter: Optional[str] = None,
        k: int = 5,
        semantic_weight: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Combine semantic and keyword-based search.
        
        Args:
            query: Search query text
            keyword_filter: Optional keyword to filter by
            k: Number of results to return
            semantic_weight: Weight for semantic score (0-1)
            
        Returns:
            Hybrid search results
        """
        # Semantic search
        semantic_results = self.search(query, k=k * 2)
        
        # Apply keyword filtering if provided
        if keyword_filter:
            keyword_weight = 1.0 - semantic_weight
            
            for result in semantic_results:
                text = result['metadata'].get('text', '')
                
                # Simple keyword matching score
                keyword_score = self._keyword_match_score(text, keyword_filter)
                
                # Combine scores
                semantic_score = result.get('score', 0)
                result['score'] = (
                    semantic_weight * semantic_score +
                    keyword_weight * keyword_score
                )
                result['semantic_score'] = semantic_score
                result['keyword_score'] = keyword_score
            
            # Re-sort by combined score
            semantic_results.sort(key=lambda x: x['score'], reverse=True)
        
        return semantic_results[:k]
    
    def _apply_filters(
        self,
        results: List[Dict[str, Any]],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Apply metadata filters to results.
        
        Args:
            results: List of search results
            filters: Dictionary of metadata filters
            
        Returns:
            Filtered results
        """
        filtered_results = []
        
        for result in results:
            metadata = result.get('metadata', {})
            
            # Check if all filters match
            matches = True
            for key, value in filters.items():
                if metadata.get(key) != value:
                    matches = False
                    break
            
            if matches and not metadata.get('_deleted', False):
                filtered_results.append(result)
        
        return filtered_results
    
    def _get_context_chunks(
        self,
        file_path: str,
        chunk_index: int,
        window: int
    ) -> List[Dict[str, Any]]:
        """
        Get surrounding chunks for context.
        
        Args:
            file_path: Path to file
            chunk_index: Index of target chunk
            window: Number of chunks before/after
            
        Returns:
            List of context chunks
        """
        context_chunks = []
        
        # Search for chunks in the same file
        for i in range(chunk_index - window, chunk_index + window + 1):
            if i == chunk_index:
                continue
            
            # Find chunk with this index
            for idx, metadata in enumerate(self.vector_store.metadata):
                if (metadata.get('file_path') == file_path and
                    metadata.get('chunk_index') == i and
                    not metadata.get('_deleted', False)):
                    context_chunks.append({
                        'chunk_index': i,
                        'text': metadata.get('text', ''),
                        'position': 'before' if i < chunk_index else 'after'
                    })
                    break
        
        return sorted(context_chunks, key=lambda x: x['chunk_index'])
    
    def _keyword_match_score(self, text: str, keyword: str) -> float:
        """
        Calculate keyword match score.
        
        Args:
            text: Text to search in
            keyword: Keyword to search for
            
        Returns:
            Match score (0-1)
        """
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        # Count occurrences
        count = text_lower.count(keyword_lower)
        
        # Normalize by text length
        if len(text) == 0:
            return 0.0
        
        score = min(count / 10.0, 1.0)  # Cap at 1.0
        return score
    
    def get_similar_chunks(
        self,
        chunk_text: str,
        k: int = 5,
        exclude_same_file: bool = False,
        file_path: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find chunks similar to a given chunk.
        
        Args:
            chunk_text: Text of the chunk to find similar chunks for
            k: Number of similar chunks to return
            exclude_same_file: Whether to exclude chunks from same file
            file_path: File path of the source chunk (for exclusion)
            
        Returns:
            List of similar chunks
        """
        # Generate embedding for the chunk
        chunk_embedding = self.embedding_service.encode_query(chunk_text)
        
        # Search
        results = self.vector_store.search(
            chunk_embedding,
            k=k * 2 if exclude_same_file else k,
            return_scores=True
        )
        
        # Filter out same file if requested
        if exclude_same_file and file_path:
            results = [
                r for r in results
                if r['metadata'].get('file_path') != file_path
            ]
        
        return results[:k]

# Made with Bob
