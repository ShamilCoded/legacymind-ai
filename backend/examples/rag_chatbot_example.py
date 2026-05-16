"""
Example usage of the RAG chatbot system.

This example demonstrates:
- Setting up the chatbot
- Indexing a repository
- Conversational Q&A
- Architecture explanations
- Dependency tracing
- Session management
"""
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.embeddings.embedding_service import EmbeddingService
from src.services.vector_store.vector_store import VectorStore
from src.services.embeddings.pipeline import EmbeddingsPipeline
from src.services.chat.rag_chatbot import RAGChatbot
from src.services.chat.memory import ConversationMemory, SessionManager


def setup_environment():
    """Setup environment variables."""
    # Set your API keys here or in .env file
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Please set it in your environment.")
        print("export OPENAI_API_KEY='your-key-here'")
        return False
    return True


def example_1_index_repository():
    """Example 1: Index a repository."""
    print("\n" + "="*60)
    print("Example 1: Indexing a Repository")
    print("="*60)
    
    # Initialize services
    print("\n1. Initializing embedding service...")
    embedding_service = EmbeddingService(model_name="all-MiniLM-L6-v2")
    
    print("2. Creating vector store...")
    dimension = embedding_service.get_embedding_dimension()
    vector_store = VectorStore(dimension=dimension, index_type="flat")
    
    print("3. Creating pipeline...")
    pipeline = EmbeddingsPipeline(
        embedding_service=embedding_service,
        vector_store=vector_store
    )
    
    # Process a directory (use your own repository path)
    repo_path = "./src"  # Example: index the src directory
    
    print(f"\n4. Processing repository: {repo_path}")
    result = pipeline.process_directory(
        directory=repo_path,
        file_patterns=["*.py", "*.md"],
        exclude_patterns=["*/__pycache__/*", "*/tests/*"]
    )
    
    print(f"\n✓ Indexing complete!")
    print(f"  - Files processed: {result['files_processed']}")
    print(f"  - Chunks created: {result['chunks_created']}")
    print(f"  - Vectors added: {result['vectors_added']}")
    
    # Save vector store
    print("\n5. Saving vector store...")
    vector_store.save("./vector_store_data")
    print("✓ Vector store saved to ./vector_store_data")
    
    return embedding_service, vector_store


def example_2_basic_chat(embedding_service, vector_store):
    """Example 2: Basic conversational Q&A."""
    print("\n" + "="*60)
    print("Example 2: Basic Conversational Q&A")
    print("="*60)
    
    # Create chatbot
    print("\n1. Initializing chatbot...")
    chatbot = RAGChatbot(
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm_provider="openai",
        model_name="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create conversation memory
    memory = ConversationMemory(max_messages=20)
    
    # Ask questions
    questions = [
        "What is the main purpose of this codebase?",
        "How does the embedding service work?",
        "Can you show me an example of how to use it?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 60)
        
        response = chatbot.chat(
            query=question,
            memory=memory
        )
        
        print(f"\nAnswer:\n{response['response']}")
        
        if response['sources']:
            print(f"\nSources ({len(response['sources'])}):")
            for source in response['sources'][:2]:
                print(f"  - {source['file_path']} (score: {source['score']:.2f})")
        
        if response['suggestions']:
            print(f"\nSuggested follow-ups:")
            for suggestion in response['suggestions'][:3]:
                print(f"  - {suggestion}")
    
    return chatbot, memory


def example_3_architecture_explanation(chatbot, memory):
    """Example 3: Explain architecture."""
    print("\n" + "="*60)
    print("Example 3: Architecture Explanation")
    print("="*60)
    
    # Overall architecture
    print("\n1. Explaining overall architecture...")
    print("-" * 60)
    
    response = chatbot.explain_architecture(memory=memory)
    print(f"\n{response['response']}")
    
    # Specific component
    print("\n2. Explaining specific component (embedding service)...")
    print("-" * 60)
    
    response = chatbot.explain_architecture(
        component="embedding service",
        memory=memory
    )
    print(f"\n{response['response']}")


def example_4_dependency_tracing(chatbot, memory):
    """Example 4: Trace dependencies."""
    print("\n" + "="*60)
    print("Example 4: Dependency Tracing")
    print("="*60)
    
    # Trace dependencies for a file
    target = "embedding_service.py"
    
    print(f"\n1. Tracing dependencies for: {target}")
    print("-" * 60)
    
    response = chatbot.trace_dependencies(
        file_or_function=target,
        memory=memory
    )
    
    print(f"\nExplanation:\n{response['response']}")
    
    if response.get('dependencies'):
        print(f"\nDependency Map:")
        for file, deps in response['dependencies'].items():
            print(f"\n  {file}:")
            for dep in deps[:5]:
                print(f"    - {dep}")


def example_5_code_search(chatbot):
    """Example 5: Search for code."""
    print("\n" + "="*60)
    print("Example 5: Code Search")
    print("="*60)
    
    queries = [
        "function that generates embeddings",
        "class that manages vector storage",
        "code that handles file processing"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Searching for: {query}")
        print("-" * 60)
        
        results = chatbot.find_similar_code(
            code_description=query,
            k=3
        )
        
        print(f"\nFound {len(results)} results:")
        for j, result in enumerate(results, 1):
            print(f"\n  Result {j}:")
            print(f"    File: {result['file_path']}")
            print(f"    Score: {result['score']:.2f}")
            print(f"    Language: {result.get('language', 'unknown')}")
            
            if result.get('elements'):
                print(f"    Contains:")
                for elem_type, names in result['elements'].items():
                    if names and elem_type != 'comment':
                        print(f"      - {elem_type}s: {', '.join(names[:3])}")


def example_6_session_management():
    """Example 6: Session management."""
    print("\n" + "="*60)
    print("Example 6: Session Management")
    print("="*60)
    
    # Create session manager
    print("\n1. Creating session manager...")
    session_manager = SessionManager(storage_dir="./chat_sessions")
    
    # Create multiple sessions
    print("\n2. Creating sessions...")
    session1 = session_manager.create_session("user-alice")
    session2 = session_manager.create_session("user-bob")
    
    # Add messages to sessions
    session1.add_message("user", "How does the vector store work?")
    session1.add_message("assistant", "The vector store uses FAISS...")
    
    session2.add_message("user", "What is the embedding dimension?")
    session2.add_message("assistant", "The embedding dimension is 384...")
    
    # List sessions
    print("\n3. Active sessions:")
    for session_id in session_manager.list_sessions():
        memory = session_manager.get_session(session_id)
        stats = memory.get_stats()
        print(f"  - {session_id}: {stats['total_messages']} messages")
    
    # Save sessions
    print("\n4. Saving sessions...")
    session_manager.save_session("user-alice")
    session_manager.save_session("user-bob")
    print("✓ Sessions saved")
    
    # Load session
    print("\n5. Loading session...")
    loaded_session = session_manager.load_session("user-alice")
    messages = loaded_session.get_messages()
    print(f"✓ Loaded session with {len(messages)} messages")
    
    for msg in messages:
        print(f"  {msg.role}: {msg.content[:50]}...")


def example_7_advanced_features(chatbot, memory):
    """Example 7: Advanced features."""
    print("\n" + "="*60)
    print("Example 7: Advanced Features")
    print("="*60)
    
    # Get conversation context
    print("\n1. Getting conversation context...")
    context = memory.get_context(max_messages=5)
    print(f"✓ Retrieved {len(context)} context messages")
    
    # Get relevant context
    print("\n2. Getting relevant context for query...")
    relevant = memory.get_relevant_context(
        query="embedding service",
        max_messages=3
    )
    print(f"✓ Found {len(relevant)} relevant messages")
    
    # Get conversation stats
    print("\n3. Conversation statistics:")
    stats = memory.get_stats()
    for key, value in stats.items():
        print(f"  - {key}: {value}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("RAG Chatbot System - Complete Examples")
    print("="*60)
    
    # Check environment
    if not setup_environment():
        return
    
    try:
        # Example 1: Index repository
        embedding_service, vector_store = example_1_index_repository()
        
        # Example 2: Basic chat
        chatbot, memory = example_2_basic_chat(embedding_service, vector_store)
        
        # Example 3: Architecture explanation
        example_3_architecture_explanation(chatbot, memory)
        
        # Example 4: Dependency tracing
        example_4_dependency_tracing(chatbot, memory)
        
        # Example 5: Code search
        example_5_code_search(chatbot)
        
        # Example 6: Session management
        example_6_session_management()
        
        # Example 7: Advanced features
        example_7_advanced_features(chatbot, memory)
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


# Made with Bob