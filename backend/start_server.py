"""
Startup script for RAG Chatbot API server.
"""
import os
import sys
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


def check_environment():
    """Check if required environment variables are set."""
    required_vars = []
    
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    
    if llm_provider == "openai":
        if not os.getenv("OPENAI_API_KEY"):
            required_vars.append("OPENAI_API_KEY")
    elif llm_provider == "anthropic":
        if not os.getenv("ANTHROPIC_API_KEY"):
            required_vars.append("ANTHROPIC_API_KEY")
    
    if required_vars:
        print("❌ Missing required environment variables:")
        for var in required_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        print("See .env.example for reference.")
        return False
    
    return True


def print_startup_info():
    """Print startup information."""
    llm_provider = os.getenv("LLM_PROVIDER", "openai")
    model_name = os.getenv("MODEL_NAME", "gpt-4-turbo-preview")
    embedding_model = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    print("\n" + "="*60)
    print("🤖 RAG Chatbot API Server")
    print("="*60)
    print(f"\n📊 Configuration:")
    print(f"   LLM Provider: {llm_provider}")
    print(f"   Model: {model_name}")
    print(f"   Embedding Model: {embedding_model}")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"\n🌐 Server will be available at:")
    print(f"   - Local: http://localhost:{port}")
    print(f"   - Network: http://{host}:{port}")
    print(f"   - API Docs: http://localhost:{port}/docs")
    print(f"   - OpenAPI: http://localhost:{port}/openapi.json")
    print("\n" + "="*60 + "\n")


def main():
    """Main entry point."""
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Print startup info
    print_startup_info()
    
    # Get configuration
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    # Start server
    try:
        uvicorn.run(
            "src.api.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()


# Made with Bob