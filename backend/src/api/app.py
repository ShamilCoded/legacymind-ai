"""
FastAPI application for RAG chatbot system.
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from typing import Optional
import logging
from pathlib import Path

from .models import (
    ChatRequest, ChatResponse, ArchitectureRequest, DependencyRequest,
    DependencyResponse, SearchRequest, SearchResponse, SessionListResponse,
    HealthResponse, ErrorResponse, IndexRequest, IndexResponse,
    ConversationHistoryResponse, MessageHistory, SourceDocument, CodeResult,
    ArchitectureGraphRequest, ArchitectureGraphResponse, GraphNode, GraphEdge,
    ModuleGroup, ArchitectureLayer, GraphMetrics, DependencyTreeRequest,
    DependencyTreeResponse, RiskAnalysisRequest, RiskAnalysisResult,
    RiskVisualization
)
from ..services.embeddings.embedding_service import EmbeddingService
from ..services.vector_store.vector_store import VectorStore
from ..services.chat.rag_chatbot import RAGChatbot
from ..services.chat.memory import SessionManager
from ..services.architecture.graph_generator import GraphGenerator
from ..services.embeddings.pipeline import EmbeddingsPipeline
from ..services.risk_analysis.risk_analyzer import RiskAnalyzer
from ..services.modernization.modernization_engine import ModernizationEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
app_state = {
    "embedding_service": None,
    "vector_store": None,
    "chatbot": None,
    "session_manager": None,
    "pipeline": None,
    "graph_generator": None,
    "risk_analyzer": None,
    "modernization_engine": None
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Initializing RAG chatbot system...")
    
    # Load environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    google_api_key = os.getenv("GOOGLE_API_KEY")
    llm_provider = os.getenv("LLM_PROVIDER", "gemini")
    model_name = os.getenv("MODEL_NAME", "gemini-1.5-flash")
    embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    vector_store_path = os.getenv("VECTOR_STORE_PATH", "./vector_store_data")
    
    # Initialize embedding service
    logger.info(f"Loading embedding model: {embedding_model}")
    app_state["embedding_service"] = EmbeddingService(model_name=embedding_model)
    
    # Initialize or load vector store
    vector_store_dir = Path(vector_store_path)
    if vector_store_dir.exists() and (vector_store_dir / "index.faiss").exists():
        logger.info(f"Loading existing vector store from {vector_store_path}")
        app_state["vector_store"] = VectorStore.load(vector_store_path)
    else:
        logger.info("Creating new vector store")
        dimension = app_state["embedding_service"].get_embedding_dimension()
        app_state["vector_store"] = VectorStore(dimension=dimension)
    
    # Initialize chatbot
    if llm_provider == "openai":
        api_key = openai_api_key
    elif llm_provider == "anthropic":
        api_key = anthropic_api_key
    elif llm_provider == "gemini":
        api_key = google_api_key
    else:
        api_key = None
    logger.info(f"Initializing chatbot with {llm_provider}/{model_name}")
    app_state["chatbot"] = RAGChatbot(
        embedding_service=app_state["embedding_service"],
        vector_store=app_state["vector_store"],
        llm_provider=llm_provider,
        model_name=model_name,
        api_key=api_key
    )
    
    # Initialize session manager
    app_state["session_manager"] = SessionManager()
    
    # Initialize pipeline
    app_state["pipeline"] = EmbeddingsPipeline(
        embedding_service=app_state["embedding_service"],
        vector_store=app_state["vector_store"]
    )
    
    # Initialize graph generator
    app_state["graph_generator"] = GraphGenerator()
    
    # Initialize risk analyzer
    app_state["risk_analyzer"] = RiskAnalyzer()
    
    # Initialize modernization engine
    app_state["modernization_engine"] = ModernizationEngine()
    
    logger.info("RAG chatbot system initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down RAG chatbot system...")
    
    # Save vector store
    if app_state["vector_store"]:
        logger.info(f"Saving vector store to {vector_store_path}")
        app_state["vector_store"].save(vector_store_path)
    
    logger.info("Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Repository RAG Chatbot API",
    description="Semantic search and conversational Q&A for code repositories",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get chatbot
def get_chatbot() -> RAGChatbot:
    """Get chatbot instance."""
    if app_state["chatbot"] is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    return app_state["chatbot"]


# Dependency to get session manager
def get_session_manager() -> SessionManager:
    """Get session manager instance."""
    if app_state["session_manager"] is None:
        raise HTTPException(status_code=503, detail="Session manager not initialized")
    return app_state["session_manager"]


# Dependency to get pipeline


# Dependency to get graph generator
def get_graph_generator() -> GraphGenerator:
    """Get graph generator instance."""
    if app_state["graph_generator"] is None:
        raise HTTPException(status_code=503, detail="Graph generator not initialized")
    return app_state["graph_generator"]


def get_risk_analyzer() -> RiskAnalyzer:
    """Get risk analyzer instance."""
    if app_state["risk_analyzer"] is None:
        raise HTTPException(status_code=503, detail="Risk analyzer not initialized")
    return app_state["risk_analyzer"]


def get_modernization_engine() -> ModernizationEngine:
    """Get modernization engine instance."""
    if app_state["modernization_engine"] is None:
        raise HTTPException(status_code=503, detail="Modernization engine not initialized")
    return app_state["modernization_engine"]


def get_pipeline() -> EmbeddingsPipeline:
    """Get pipeline instance."""
    if app_state["pipeline"] is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    return app_state["pipeline"]


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Repository RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    vector_store = app_state.get("vector_store")
    stats = vector_store.get_stats() if vector_store else {}
    
    return HealthResponse(
        status="healthy" if app_state["chatbot"] else "initializing",
        version="1.0.0",
        vector_store_stats=stats
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chatbot: RAGChatbot = Depends(get_chatbot),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Chat with the repository assistant.
    
    Performs semantic search over the repository and generates
    contextual responses using RAG.
    """
    try:
        # Get or create session
        memory = None
        if request.session_id:
            memory = session_manager.get_or_create_session(request.session_id)
        
        # Process query
        result = chatbot.chat(
            query=request.query,
            memory=memory,
            session_id=request.session_id
        )
        
        # Format response
        sources = [
            SourceDocument(**source) for source in result.get("sources", [])
        ] if request.include_sources else []
        
        return ChatResponse(
            response=result["response"],
            sources=sources,
            suggestions=result.get("suggestions", []),
            session_id=result.get("session_id"),
            metadata=result.get("metadata", {})
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/architecture", response_model=ChatResponse)
async def explain_architecture(
    request: ArchitectureRequest,
    chatbot: RAGChatbot = Depends(get_chatbot),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Explain repository architecture.
    
    Provides high-level architectural overview or explains
    specific components.
    """
    try:
        memory = None
        if request.session_id:
            memory = session_manager.get_or_create_session(request.session_id)
        
        result = chatbot.explain_architecture(
            component=request.component,
            memory=memory
        )
        
        return ChatResponse(
            response=result["response"],
            sources=[SourceDocument(**s) for s in result.get("sources", [])],
            suggestions=result.get("suggestions", []),
            session_id=result.get("session_id"),
            metadata=result.get("metadata", {})
        )
    
    except Exception as e:
        logger.error(f"Error in architecture endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/dependencies", response_model=DependencyResponse)
async def trace_dependencies(
    request: DependencyRequest,
    chatbot: RAGChatbot = Depends(get_chatbot),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Trace dependencies for a file or function.
    
    Shows what the target depends on and what depends on it.
    """
    try:
        memory = None
        if request.session_id:
            memory = session_manager.get_or_create_session(request.session_id)
        
        result = chatbot.trace_dependencies(
            file_or_function=request.target,
            memory=memory
        )
        
        return DependencyResponse(
            response=result["response"],
            dependencies=result.get("dependencies", {}),
            sources=[SourceDocument(**s) for s in result.get("sources", [])],
            session_id=result.get("session_id")
        )
    
    except Exception as e:
        logger.error(f"Error in dependencies endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchResponse)
async def search_code(
    request: SearchRequest,
    chatbot: RAGChatbot = Depends(get_chatbot)
):
    """
    Search for code snippets.
    
    Performs semantic search to find relevant code based on
    natural language description.
    """
    try:
        results = chatbot.find_similar_code(
            code_description=request.query,
            k=request.k
        )
        
        # Filter by file type if specified
        if request.file_type:
            results = [
                r for r in results
                if r.get("language") == request.file_type
            ]
        
        return SearchResponse(
            results=[CodeResult(**r) for r in results],
            total=len(results)
        )
    
    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index", response_model=IndexResponse)
async def index_repository(
    request: IndexRequest,
    pipeline: EmbeddingsPipeline = Depends(get_pipeline)
):
    """
    Index a repository.
    
    Processes files, generates embeddings, and stores in vector database.
    """
    try:
        import time
        start_time = time.time()
        
        # Process repository
        result = pipeline.process_directory(
            directory=request.repository_path,
            file_patterns=request.file_patterns,
            exclude_patterns=request.exclude_patterns,
            chunk_size=request.chunk_size,
            chunk_overlap=request.chunk_overlap
        )
        
        duration = time.time() - start_time
        
        return IndexResponse(
            status="completed",
            files_processed=result.get("files_processed", 0),
            chunks_created=result.get("chunks_created", 0),
            vectors_added=result.get("vectors_added", 0),
            duration_seconds=duration
        )
    
    except Exception as e:
        logger.error(f"Error in index endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    session_manager: SessionManager = Depends(get_session_manager)
):
    """List all active sessions."""
    try:
        session_ids = session_manager.list_sessions()
        sessions = []
        
        for session_id in session_ids:
            memory = session_manager.get_session(session_id)
            if memory:
                stats = memory.get_stats()
                sessions.append({
                    "session_id": session_id,
                    "total_messages": stats["total_messages"],
                    "user_messages": stats["user_messages"],
                    "assistant_messages": stats["assistant_messages"],
                    "created_at": None
                })
        
        return SessionListResponse(
            sessions=sessions,
            total=len(sessions)
        )
    
    except Exception as e:
        logger.error(f"Error in list sessions endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions/{session_id}", response_model=ConversationHistoryResponse)
async def get_session_history(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """Get conversation history for a session."""
    try:
        memory = session_manager.get_session(session_id)
        if not memory:
            raise HTTPException(status_code=404, detail="Session not found")
        
        messages = memory.get_messages()
        
        return ConversationHistoryResponse(
            session_id=session_id,
            messages=[
                MessageHistory(
                    role=msg.role,
                    content=msg.content,
                    timestamp=msg.timestamp,
                    metadata=msg.metadata
                )
                for msg in messages
            ],
            total_messages=len(messages)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get session history endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """Delete a session."""
    try:
        success = session_manager.delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete session endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Made with Bob


@app.post("/architecture/graph", response_model=ArchitectureGraphResponse)
async def generate_architecture_graph(
    request: ArchitectureGraphRequest,
    graph_generator: GraphGenerator = Depends(get_graph_generator)
):
    """
    Generate architecture visualization graph.
    
    Analyzes code dependencies and creates a node-edge graph
    for visualization with React Flow.
    """
    try:
        graph = graph_generator.generate_architecture_graph(
            directory=request.directory,
            file_patterns=request.file_patterns,
            max_depth=request.max_depth
        )
        
        return ArchitectureGraphResponse(
            nodes=[GraphNode(**node) for node in graph['nodes']],
            edges=[GraphEdge(**edge) for edge in graph['edges']],
            modules=[ModuleGroup(**module) for module in graph.get('modules', [])],
            layers=[ArchitectureLayer(**layer) for layer in graph.get('layers', [])],
            metrics=GraphMetrics(**graph.get('metrics', {})),
            stats=graph.get('stats', {})
        )
    
    except Exception as e:
        logger.error(f"Error generating architecture graph: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/architecture/module-graph")
async def generate_module_graph(
    directory: str,
    module_path: str,
    graph_generator: GraphGenerator = Depends(get_graph_generator)
):
    """
    Generate graph for a specific module.
    
    Shows dependencies within and connections to a specific module.
    """
    try:
        graph = graph_generator.generate_module_graph(directory, module_path)
        
        return {
            'nodes': graph['nodes'],
            'edges': graph['edges'],
            'stats': graph.get('stats', {})
        }
    
    except Exception as e:
        logger.error(f"Error generating module graph: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/architecture/api-relationships")
async def generate_api_relationships(
    directory: str,
    graph_generator: GraphGenerator = Depends(get_graph_generator)
):
    """
    Generate API relationship graph.
    
    Shows how API endpoints connect to services and data layers.
    """
    try:
        graph = graph_generator.generate_api_relationship_graph(directory)
        
        return {
            'nodes': graph['nodes'],
            'edges': graph['edges'],
            'stats': graph.get('stats', {})
        }
    
    except Exception as e:
        logger.error(f"Error generating API relationships: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/architecture/dependency-tree", response_model=DependencyTreeResponse)
async def generate_dependency_tree(
    request: DependencyTreeRequest,
    graph_generator: GraphGenerator = Depends(get_graph_generator)
):
    """
    Generate dependency tree for a specific file.
    
    Shows what a file depends on and what depends on it.
    """
    try:
        tree = graph_generator.generate_dependency_tree(
            directory=request.directory,
            target_file=request.target_file
        )
        
        return DependencyTreeResponse(
            root=GraphNode(**tree['root']) if tree.get('root') else None,
            nodes=[GraphNode(**node) for node in tree.get('nodes', [])],
            edges=[GraphEdge(**edge) for edge in tree.get('edges', [])],
            stats=tree.get('stats', {})
        )
    
    except Exception as e:
        logger.error(f"Error generating dependency tree: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/risk-analysis", response_model=RiskAnalysisResult)
async def analyze_repository_risk(
    request: RiskAnalysisRequest,
    risk_analyzer: RiskAnalyzer = Depends(get_risk_analyzer)
):
    """
    Perform comprehensive risk analysis on a repository.
    
    Analyzes:
    - Circular dependencies
    - Dead code
    - Module coupling
    - Test coverage
    - Risky files
    - Code complexity
    
    Returns detailed risk assessment with scores and recommendations.
    """
    try:
        logger.info(f"Starting risk analysis for: {request.directory}")
        
        result = risk_analyzer.analyze(
            directory=request.directory,
            file_patterns=request.file_patterns,
            exclude_patterns=request.exclude_patterns,
            include_tests=request.include_tests,
            include_complexity=request.include_complexity,
            include_dependencies=request.include_dependencies
        )
        
        logger.info(f"Risk analysis complete. Overall score: {result.overall_risk_score.overall_score}")
        
        return result
    
    except Exception as e:
        logger.error(f"Error in risk analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/risk-analysis/visualization", response_model=RiskVisualization)
async def get_risk_visualization(
    request: RiskAnalysisRequest,
    risk_analyzer: RiskAnalyzer = Depends(get_risk_analyzer)
):
    """
    Get risk analysis with visualization data.
    
    Returns risk analysis results formatted for frontend visualization
    including heatmaps, charts, and graphs.
    """
    try:
        # Perform analysis
        result = risk_analyzer.analyze(
            directory=request.directory,
            file_patterns=request.file_patterns,
            exclude_patterns=request.exclude_patterns,
            include_tests=request.include_tests,
            include_complexity=request.include_complexity,
            include_dependencies=request.include_dependencies
        )
        
        # Generate visualization data
        viz_data = risk_analyzer.generate_visualization_data(result)
        
        return RiskVisualization(
            risk_heatmap=viz_data['risk_heatmap'],
            dependency_graph=viz_data.get('dependency_graph', {}),
            complexity_distribution=viz_data['complexity_distribution'],
            risk_trends=viz_data['risk_trends'],
            top_risks=viz_data['top_risks']
        )
    
    except Exception as e:
        logger.error(f"Error generating risk visualization: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/risk-analysis/file/{file_path:path}")
async def analyze_file_risk(
    file_path: str,
    risk_analyzer: RiskAnalyzer = Depends(get_risk_analyzer)
):
    """
    Analyze risk for a single file.
    
    Returns complexity metrics and risk assessment for the specified file.
    """
    try:
        result = risk_analyzer.analyze_file(file_path)
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing file risk: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/risk-analysis/summary/{directory:path}")
async def get_risk_summary(
    directory: str,
    risk_analyzer: RiskAnalyzer = Depends(get_risk_analyzer)
):
    """
    Get quick risk summary for a directory.
    
    Returns high-level risk metrics without detailed analysis.
    """
    try:
        result = risk_analyzer.analyze(
            directory=directory,
            include_tests=False,
            include_complexity=True,
            include_dependencies=True
        )
        
        return {
            'overall_score': result.overall_risk_score.overall_score,
            'risk_level': result.overall_risk_score.risk_level.value,
            'critical_issues': result.overall_risk_score.critical_issues,
            'high_issues': result.overall_risk_score.high_issues,
            'recommendations': result.overall_risk_score.recommendations[:3],
            'summary': result.summary
        }
    
    except Exception as e:
        logger.error(f"Error getting risk summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Made with Bob

# Made with Bob

# Modernization Endpoints

@app.post("/modernization/analyze")
async def analyze_modernization(
    request: dict,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Perform comprehensive modernization analysis.
    
    Analyzes repository for:
    - Outdated dependencies
    - Microservice opportunities
    - Refactoring needs
    - Cloud migration readiness
    - Scalability issues
    
    Returns complete modernization roadmap with recommendations.
    """
    try:
        from ..services.modernization.models import ModernizationRequest
        
        # Create request object
        mod_request = ModernizationRequest(**request)
        
        logger.info(f"Starting modernization analysis for {mod_request.directory}")
        
        # Perform analysis
        result = modernization_engine.analyze(mod_request)
        
        logger.info(f"Modernization analysis complete. Score: {result.overall_modernization_score}")
        
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error in modernization analysis: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/modernization/summary/{directory:path}")
async def get_modernization_summary(
    directory: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Get quick modernization summary for a directory.
    
    Returns high-level assessment without detailed analysis.
    """
    try:
        from ..services.modernization.models import ModernizationRequest
        
        # Quick analysis with minimal options
        request = ModernizationRequest(
            directory=directory,
            analyze_dependencies=True,
            analyze_architecture=False,
            analyze_scalability=False
        )
        
        result = modernization_engine.analyze(request)
        
        return {
            'overall_score': result.overall_modernization_score,
            'summary': result.summary,
            'immediate_actions': result.immediate_actions[:3],
            'critical_dependencies': result.dependency_analysis.critical_updates if result.dependency_analysis else 0,
            'security_issues': result.dependency_analysis.security_issues if result.dependency_analysis else 0
        }
    
    except Exception as e:
        logger.error(f"Error getting modernization summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modernization/dependencies")
async def analyze_dependencies(
    directory: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Analyze dependencies for outdated packages and security issues.
    """
    try:
        result = modernization_engine.dependency_analyzer.analyze(directory)
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error analyzing dependencies: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modernization/microservices")
async def analyze_microservices(
    directory: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Analyze codebase for microservice decomposition opportunities.
    """
    try:
        result = modernization_engine.microservice_analyzer.analyze(directory)
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error analyzing microservices: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modernization/refactoring")
async def analyze_refactoring(
    directory: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Analyze code quality and refactoring opportunities.
    """
    try:
        result = modernization_engine.refactoring_analyzer.analyze(directory)
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error analyzing refactoring: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modernization/cloud-migration")
async def plan_cloud_migration(
    directory: str,
    target_provider: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Create cloud migration plan for specified provider.
    """
    try:
        from ..services.modernization.models import CloudProvider
        
        provider = CloudProvider(target_provider)
        result = modernization_engine.cloud_migration_planner.create_plan(
            directory=directory,
            target_provider=provider,
            include_cost_estimates=True
        )
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error planning cloud migration: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/modernization/scalability")
async def analyze_scalability(
    directory: str,
    modernization_engine: ModernizationEngine = Depends(get_modernization_engine)
):
    """
    Analyze scalability and performance bottlenecks.
    """
    try:
        result = modernization_engine.scalability_analyzer.analyze(directory)
        return result.dict()
    
    except Exception as e:
        logger.error(f"Error analyzing scalability: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# Made with Bob