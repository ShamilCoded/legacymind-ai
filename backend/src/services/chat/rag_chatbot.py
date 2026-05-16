"""
RAG Chatbot service using LangGraph for conversational repository Q&A.
"""
from typing import List, Dict, Any, Optional, TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

from .memory import ConversationMemory
from .code_analyzer import CodeAnalyzer
from ..vector_store.retrieval import SemanticRetriever
from ..embeddings.embedding_service import EmbeddingService
from ..vector_store.vector_store import VectorStore

import logging

logger = logging.getLogger(__name__)


class ChatState(TypedDict):
    """State for the chat graph."""
    query: str
    chat_history: List[Dict[str, str]]
    retrieved_docs: List[Dict[str, Any]]
    code_analysis: Dict[str, Any]
    response: str
    metadata: Dict[str, Any]


class RAGChatbot:
    """Repository RAG chatbot with LangGraph orchestration."""
    
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_provider: str = "gemini",
        model_name: str = "gemini-1.5-flash",
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize RAG chatbot.
        
        Args:
            embedding_service: Service for generating embeddings
            vector_store: Vector store for retrieval
            llm_provider: LLM provider ('openai', 'anthropic', or 'gemini')
            model_name: Model name
            api_key: API key for LLM provider
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        """
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.retriever = SemanticRetriever(embedding_service=embedding_service, vector_store=vector_store)
        self.code_analyzer = CodeAnalyzer()
        
        # Initialize LLM
        if llm_provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif llm_provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model_name,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens
            )
        elif llm_provider == "gemini":
            import os
            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
            self.llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=temperature,
                max_output_tokens=max_tokens
            )
        else:
            raise ValueError(f"Unknown LLM provider: {llm_provider}")
        
        # Build LangGraph workflow
        self.graph = self._build_graph()
        
        logger.info(f"Initialized RAG chatbot with {llm_provider}/{model_name}")
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow for RAG.
        
        Returns:
            Compiled StateGraph
        """
        workflow = StateGraph(ChatState)
        
        # Add nodes
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("analyze_code", self._analyze_code_node)
        workflow.add_node("generate_response", self._generate_response_node)
        
        # Add edges
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "analyze_code")
        workflow.add_edge("analyze_code", "generate_response")
        workflow.add_edge("generate_response", END)
        
        return workflow.compile()
    
    def _retrieve_node(self, state: ChatState) -> ChatState:
        """
        Retrieve relevant documents from vector store.
        
        Args:
            state: Current chat state
            
        Returns:
            Updated state with retrieved documents
        """
        query = state["query"]
        
        # Perform semantic search
        results = self.retriever.search(
            query=query,
            k=5,
            score_threshold=0.3
        )
        
        state["retrieved_docs"] = results
        state["metadata"] = {
            "num_retrieved": len(results),
            "retrieval_scores": [r.get("score", 0) for r in results]
        }
        
        logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
        return state
    
    def _analyze_code_node(self, state: ChatState) -> ChatState:
        """
        Analyze retrieved code chunks.
        
        Args:
            state: Current chat state
            
        Returns:
            Updated state with code analysis
        """
        results = state["retrieved_docs"]
        
        # Analyze code in results
        analyzed_results = []
        for result in results:
            analysis = self.code_analyzer.analyze_code_chunk(result)
            result["code_analysis"] = analysis
            analyzed_results.append(result)
        
        # Extract dependencies
        dependencies = self.code_analyzer.extract_dependencies(analyzed_results)
        
        # Generate code context
        code_context = self.code_analyzer.generate_code_context(
            analyzed_results,
            max_context_length=3000
        )
        
        state["retrieved_docs"] = analyzed_results
        state["code_analysis"] = {
            "dependencies": {k: list(v) for k, v in dependencies.items()},
            "code_context": code_context,
            "has_code": any(r["code_analysis"]["is_code"] for r in analyzed_results)
        }
        
        logger.info("Completed code analysis")
        return state
    
    def _generate_response_node(self, state: ChatState) -> ChatState:
        """
        Generate response using LLM.
        
        Args:
            state: Current chat state
            
        Returns:
            Updated state with generated response
        """
        query = state["query"]
        chat_history = state.get("chat_history", [])
        code_context = state["code_analysis"]["code_context"]
        has_code = state["code_analysis"]["has_code"]
        
        # Build system prompt
        system_prompt = self._build_system_prompt(has_code)
        
        # Build messages
        messages = [SystemMessage(content=system_prompt)]
        
        # Add chat history
        for msg in chat_history[-6:]:  # Last 6 messages
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # Add context and query
        context_message = f"""
Relevant code and documentation from the repository:

{code_context}

User question: {query}
"""
        messages.append(HumanMessage(content=context_message))
        
        # Generate response
        response = self.llm.invoke(messages)
        
        state["response"] = response.content
        state["metadata"]["has_code_context"] = has_code
        
        logger.info("Generated response")
        return state
    
    def _build_system_prompt(self, has_code: bool) -> str:
        """
        Build system prompt based on context.
        
        Args:
            has_code: Whether code context is available
            
        Returns:
            System prompt string
        """
        base_prompt = """You are an expert AI assistant specialized in helping developers understand code repositories.

Your capabilities:
- Explain code functionality and architecture
- Identify design patterns and best practices
- Trace dependencies and relationships
- Provide implementation guidance
- Answer questions about specific functions, classes, and modules

Guidelines:
- Be precise and technical when discussing code
- Reference specific files, functions, and line numbers when relevant
- Explain complex concepts clearly
- Suggest related code or documentation when helpful
- If information is not in the provided context, say so clearly
"""
        
        if has_code:
            base_prompt += """
The context includes actual code from the repository. When answering:
- Quote relevant code snippets
- Explain what the code does
- Point out important patterns or techniques
- Mention related files or functions
"""
        else:
            base_prompt += """
The context includes documentation or text files. When answering:
- Reference specific sections
- Provide clear explanations
- Connect concepts to implementation when possible
"""
        
        return base_prompt
    
    def chat(
        self,
        query: str,
        memory: Optional[ConversationMemory] = None,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a chat query.
        
        Args:
            query: User query
            memory: Optional conversation memory
            session_id: Optional session identifier
            
        Returns:
            Response dictionary with answer and metadata
        """
        # Get chat history
        chat_history = []
        if memory:
            messages = memory.get_messages(limit=10)
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
        
        # Initialize state
        initial_state: ChatState = {
            "query": query,
            "chat_history": chat_history,
            "retrieved_docs": [],
            "code_analysis": {},
            "response": "",
            "metadata": {}
        }
        
        # Run graph
        final_state = self.graph.invoke(initial_state)
        
        # Extract response
        response = final_state["response"]
        metadata = final_state["metadata"]
        
        # Add to memory
        if memory:
            memory.add_message("user", query)
            memory.add_message("assistant", response, metadata)
        
        # Generate suggestions
        suggestions = self.code_analyzer.suggest_related_queries(
            query,
            final_state["retrieved_docs"]
        )
        
        return {
            "response": response,
            "sources": self._format_sources(final_state["retrieved_docs"]),
            "suggestions": suggestions,
            "metadata": metadata,
            "session_id": session_id
        }
    
    def _format_sources(
        self,
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Format source documents for response.
        
        Args:
            results: Retrieved documents
            
        Returns:
            Formatted sources
        """
        sources = []
        for result in results[:3]:  # Top 3 sources
            metadata = result.get("metadata", {})
            sources.append({
                "file_path": metadata.get("file_path", "unknown"),
                "score": result.get("score", 0),
                "preview": metadata.get("text", "")[:200] + "...",
                "language": result.get("code_analysis", {}).get("language"),
                "is_code": result.get("code_analysis", {}).get("is_code", False)
            })
        return sources
    
    def explain_architecture(
        self,
        component: Optional[str] = None,
        memory: Optional[ConversationMemory] = None
    ) -> Dict[str, Any]:
        """
        Explain repository architecture.
        
        Args:
            component: Optional specific component to explain
            memory: Optional conversation memory
            
        Returns:
            Architecture explanation
        """
        if component:
            query = f"Explain the architecture and design of {component}"
        else:
            query = "Explain the overall architecture and structure of this repository"
        
        # Search for architecture-related files
        results = self.retriever.search(
            query=query,
            k=10
        )
        
        # Prioritize config and main files
        results = self.code_analyzer.find_related_code(results, query_type='architecture')
        
        # Generate explanation
        return self.chat(query, memory)
    
    def trace_dependencies(
        self,
        file_or_function: str,
        memory: Optional[ConversationMemory] = None
    ) -> Dict[str, Any]:
        """
        Trace dependencies for a file or function.
        
        Args:
            file_or_function: File path or function name
            memory: Optional conversation memory
            
        Returns:
            Dependency information
        """
        query = f"What are the dependencies and imports for {file_or_function}? Show me what it depends on and what depends on it."
        
        # Search for the target
        results = self.retriever.search(query=file_or_function, k=10)
        
        # Extract dependencies
        dependencies = self.code_analyzer.extract_dependencies(results)
        
        # Generate explanation
        response = self.chat(query, memory)
        response["dependencies"] = dependencies
        
        return response
    
    def find_similar_code(
        self,
        code_description: str,
        k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar code based on description.
        
        Args:
            code_description: Description of code to find
            k: Number of results
            
        Returns:
            List of similar code chunks
        """
        results = self.retriever.search(
            query=code_description,
            k=k
        )
        
        # Analyze and format results
        formatted_results = []
        for result in results:
            analysis = self.code_analyzer.analyze_code_chunk(result)
            formatted_results.append({
                "file_path": result["metadata"].get("file_path"),
                "score": result.get("score"),
                "code": result["metadata"].get("text"),
                "language": analysis.get("language"),
                "elements": analysis.get("elements")
            })
        
        return formatted_results


# Made with Bob