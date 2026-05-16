"""
Pydantic models for API requests and responses.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., description="User query", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    max_results: int = Field(5, description="Maximum number of results to retrieve", ge=1, le=20)
    include_sources: bool = Field(True, description="Whether to include source documents")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How does the authentication system work?",
                "session_id": "user-123-session",
                "max_results": 5,
                "include_sources": True
            }
        }


class SourceDocument(BaseModel):
    """Source document in response."""
    file_path: str = Field(..., description="Path to source file")
    score: float = Field(..., description="Relevance score", ge=0, le=1)
    preview: str = Field(..., description="Preview of content")
    language: Optional[str] = Field(None, description="Programming language")
    is_code: bool = Field(False, description="Whether this is code")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Generated response")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents")
    suggestions: List[str] = Field(default_factory=list, description="Suggested follow-up questions")
    session_id: Optional[str] = Field(None, description="Session ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "The authentication system uses JWT tokens...",
                "sources": [
                    {
                        "file_path": "src/auth/jwt.py",
                        "score": 0.92,
                        "preview": "def generate_token(user_id)...",
                        "language": "python",
                        "is_code": True
                    }
                ],
                "suggestions": [
                    "How are JWT tokens validated?",
                    "Show me the user authentication flow"
                ],
                "session_id": "user-123-session",
                "metadata": {
                    "num_retrieved": 5,
                    "has_code_context": True
                }
            }
        }


class ArchitectureRequest(BaseModel):
    """Request model for architecture explanation."""
    component: Optional[str] = Field(None, description="Specific component to explain")
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "component": "authentication module",
                "session_id": "user-123-session"
            }
        }


class DependencyRequest(BaseModel):
    """Request model for dependency tracing."""
    target: str = Field(..., description="File path or function name to trace", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "target": "src/auth/jwt.py",
                "session_id": "user-123-session"
            }
        }


class DependencyResponse(BaseModel):
    """Response model for dependency tracing."""
    response: str = Field(..., description="Dependency explanation")
    dependencies: Dict[str, List[str]] = Field(default_factory=dict, description="Dependency map")
    sources: List[SourceDocument] = Field(default_factory=list, description="Source documents")
    session_id: Optional[str] = Field(None, description="Session ID")


class SearchRequest(BaseModel):
    """Request model for code search."""
    query: str = Field(..., description="Search query", min_length=1)
    k: int = Field(5, description="Number of results", ge=1, le=20)
    file_type: Optional[str] = Field(None, description="Filter by file type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "function that validates email addresses",
                "k": 5,
                "file_type": "python"
            }
        }


class CodeResult(BaseModel):
    """Code search result."""
    file_path: str = Field(..., description="Path to file")
    score: float = Field(..., description="Relevance score")
    code: str = Field(..., description="Code snippet")
    language: Optional[str] = Field(None, description="Programming language")
    elements: Dict[str, List[str]] = Field(default_factory=dict, description="Code elements")


class SearchResponse(BaseModel):
    """Response model for code search."""
    results: List[CodeResult] = Field(default_factory=list, description="Search results")
    total: int = Field(..., description="Total number of results")


class SessionInfo(BaseModel):
    """Session information."""
    session_id: str = Field(..., description="Session ID")
    total_messages: int = Field(..., description="Total messages in session")
    user_messages: int = Field(..., description="Number of user messages")
    assistant_messages: int = Field(..., description="Number of assistant messages")
    created_at: Optional[datetime] = Field(None, description="Session creation time")


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    sessions: List[SessionInfo] = Field(default_factory=list, description="List of sessions")
    total: int = Field(..., description="Total number of sessions")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    vector_store_stats: Dict[str, Any] = Field(default_factory=dict, description="Vector store statistics")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code")


class IndexRequest(BaseModel):
    """Request model for indexing repository."""
    repository_path: str = Field(..., description="Path to repository")
    file_patterns: Optional[List[str]] = Field(None, description="File patterns to include")
    exclude_patterns: Optional[List[str]] = Field(None, description="Patterns to exclude")
    chunk_size: int = Field(1000, description="Chunk size for splitting", ge=100, le=5000)
    chunk_overlap: int = Field(200, description="Chunk overlap", ge=0, le=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "repository_path": "/path/to/repo",
                "file_patterns": ["*.py", "*.js", "*.md"],
                "exclude_patterns": ["*/node_modules/*", "*/.git/*"],
                "chunk_size": 1000,
                "chunk_overlap": 200
            }
        }


class IndexResponse(BaseModel):
    """Response model for indexing."""
    status: str = Field(..., description="Indexing status")
    files_processed: int = Field(..., description="Number of files processed")
    chunks_created: int = Field(..., description="Number of chunks created")
    vectors_added: int = Field(..., description="Number of vectors added")
    duration_seconds: float = Field(..., description="Processing duration")


class MessageHistory(BaseModel):
    """Message in conversation history."""
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(..., description="Message timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Message metadata")


class ConversationHistoryResponse(BaseModel):
    """Response model for conversation history."""
    session_id: str = Field(..., description="Session ID")
    messages: List[MessageHistory] = Field(default_factory=list, description="Conversation messages")
    total_messages: int = Field(..., description="Total number of messages")


# Made with Bob

# Architecture Visualization Models

class ArchitectureGraphRequest(BaseModel):
    """Request model for architecture graph generation."""
    directory: str = Field(..., description="Directory path to analyze")
    file_patterns: Optional[List[str]] = Field(None, description="File patterns to include")
    max_depth: Optional[int] = Field(None, description="Maximum directory depth")
    
    class Config:
        json_schema_extra = {
            "example": {
                "directory": "./backend/src",
                "file_patterns": ["*.py", "*.js"],
                "max_depth": 5
            }
        }


class GraphNode(BaseModel):
    """Node in architecture graph."""
    id: str = Field(..., description="Unique node identifier")
    label: str = Field(..., description="Node label")
    type: str = Field(..., description="Node type (python, javascript, etc.)")
    path: str = Field(..., description="File path")
    functions: int = Field(0, description="Number of functions")
    classes: int = Field(0, description="Number of classes")
    imports: int = Field(0, description="Number of imports")


class GraphEdge(BaseModel):
    """Edge in architecture graph."""
    id: str = Field(..., description="Unique edge identifier")
    source: str = Field(..., description="Source node ID")
    target: str = Field(..., description="Target node ID")
    type: str = Field(..., description="Edge type (import, from_import, etc.)")
    label: Optional[str] = Field(None, description="Edge label")


class ModuleGroup(BaseModel):
    """Module grouping information."""
    name: str = Field(..., description="Module name")
    files: List[str] = Field(default_factory=list, description="File IDs in module")
    file_count: int = Field(0, description="Number of files")


class ArchitectureLayer(BaseModel):
    """Architecture layer information."""
    name: str = Field(..., description="Layer name")
    files: List[str] = Field(default_factory=list, description="File IDs in layer")
    file_count: int = Field(0, description="Number of files")


class GraphMetrics(BaseModel):
    """Graph metrics."""
    total_nodes: int = Field(0, description="Total number of nodes")
    total_edges: int = Field(0, description="Total number of edges")
    avg_dependencies: float = Field(0.0, description="Average dependencies per node")
    most_imported: List[Dict[str, Any]] = Field(default_factory=list, description="Most imported files")
    most_importing: List[Dict[str, Any]] = Field(default_factory=list, description="Most importing files")
    isolated_nodes: int = Field(0, description="Number of isolated nodes")


class ArchitectureGraphResponse(BaseModel):
    """Response model for architecture graph."""
    nodes: List[GraphNode] = Field(default_factory=list, description="Graph nodes")
    edges: List[GraphEdge] = Field(default_factory=list, description="Graph edges")
    modules: List[ModuleGroup] = Field(default_factory=list, description="Module groupings")
    layers: List[ArchitectureLayer] = Field(default_factory=list, description="Architecture layers")
    metrics: GraphMetrics = Field(..., description="Graph metrics")
    stats: Dict[str, Any] = Field(default_factory=dict, description="Additional statistics")


class DependencyTreeRequest(BaseModel):
    """Request model for dependency tree."""
    directory: str = Field(..., description="Directory path to analyze")
    target_file: str = Field(..., description="Target file to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "directory": "./backend/src",
                "target_file": "api/app.py"
            }
        }


class DependencyTreeResponse(BaseModel):
    """Response model for dependency tree."""
    root: Optional[GraphNode] = Field(None, description="Root node")
    nodes: List[GraphNode] = Field(default_factory=list, description="Tree nodes")
    edges: List[GraphEdge] = Field(default_factory=list, description="Tree edges")
    stats: Dict[str, Any] = Field(default_factory=dict, description="Tree statistics")



# Risk Analysis Models

from ..services.risk_analysis.models import (
    RiskAnalysisRequest,
    RiskAnalysisResult,
    RiskVisualization,
    CircularDependency,
    DeadCodeItem,
    CouplingMetrics,
    TestCoverageReport,
    RiskyFile,
    ComplexityMetrics,
    RiskScore,
    RiskLevel
)

# Export risk analysis models
__all__ = [
    'RiskAnalysisRequest',
    'RiskAnalysisResult',
    'RiskVisualization',
    'CircularDependency',
    'DeadCodeItem',
    'CouplingMetrics',
    'TestCoverageReport',
    'RiskyFile',
    'ComplexityMetrics',
    'RiskScore',
    'RiskLevel'
]
# Made with Bob


# Modernization Models

from ..services.modernization.models import (
    ModernizationRequest,
    ModernizationResult,
    DependencyAnalysis,
    MicroserviceRecommendation,
    RefactoringRecommendation,
    CloudMigrationPlan,
    ScalabilityAnalysis,
    ModernizationRoadmap,
    MigrationPhase,
    CloudProvider,
    ArchitecturePattern
)

# Export modernization models
__all__ = [
    'ModernizationRequest',
    'ModernizationResult',
    'DependencyAnalysis',
    'MicroserviceRecommendation',
    'RefactoringRecommendation',
    'CloudMigrationPlan',
    'ScalabilityAnalysis',
    'ModernizationRoadmap',
    'MigrationPhase',
    'CloudProvider',
    'ArchitecturePattern',
    'RiskAnalysisRequest',
    'RiskAnalysisResult',
    'RiskVisualization',
    'CircularDependency',
    'DeadCodeItem',
    'CouplingMetrics',
    'TestCoverageReport',
    'RiskyFile',
    'ComplexityMetrics',
    'RiskScore',
    'RiskLevel'
]
# Made with Bob