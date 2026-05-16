"""
Tests for RAG chatbot system.
"""
import pytest
import numpy as np
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.chat.memory import ConversationMemory, Message, SessionManager
from src.services.chat.code_analyzer import CodeAnalyzer
from src.services.embeddings.embedding_service import EmbeddingService
from src.services.vector_store.vector_store import VectorStore


class TestConversationMemory:
    """Tests for ConversationMemory."""
    
    def test_add_message(self):
        """Test adding messages to memory."""
        memory = ConversationMemory(max_messages=10)
        
        msg = memory.add_message("user", "Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert len(memory.messages) == 1
    
    def test_get_messages(self):
        """Test retrieving messages."""
        memory = ConversationMemory()
        
        memory.add_message("user", "Question 1")
        memory.add_message("assistant", "Answer 1")
        memory.add_message("user", "Question 2")
        
        messages = memory.get_messages()
        assert len(messages) == 3
        
        # Test limit
        messages = memory.get_messages(limit=2)
        assert len(messages) == 2
        
        # Test role filter
        user_messages = memory.get_messages(role_filter="user")
        assert len(user_messages) == 2
        assert all(m.role == "user" for m in user_messages)
    
    def test_get_context(self):
        """Test getting context for LLM."""
        memory = ConversationMemory()
        
        memory.add_message("user", "Question 1")
        memory.add_message("assistant", "Answer 1")
        
        context = memory.get_context(max_messages=5)
        assert len(context) == 2
        assert context[0]["role"] == "user"
        assert context[1]["role"] == "assistant"
    
    def test_max_messages_limit(self):
        """Test that max_messages limit is enforced."""
        memory = ConversationMemory(max_messages=3)
        
        for i in range(5):
            memory.add_message("user", f"Message {i}")
        
        assert len(memory.messages) == 3
        # Should keep the most recent messages
        messages = memory.get_messages()
        assert messages[-1].content == "Message 4"
    
    def test_clear(self):
        """Test clearing memory."""
        memory = ConversationMemory()
        
        memory.add_message("user", "Test")
        assert len(memory.messages) == 1
        
        memory.clear()
        assert len(memory.messages) == 0
    
    def test_get_stats(self):
        """Test getting conversation statistics."""
        memory = ConversationMemory()
        
        memory.add_message("user", "Q1")
        memory.add_message("assistant", "A1")
        memory.add_message("user", "Q2")
        
        stats = memory.get_stats()
        assert stats["total_messages"] == 3
        assert stats["user_messages"] == 2
        assert stats["assistant_messages"] == 1


class TestMessage:
    """Tests for Message class."""
    
    def test_message_creation(self):
        """Test creating a message."""
        msg = Message("user", "Hello", {"key": "value"})
        
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert msg.metadata == {"key": "value"}
        assert msg.timestamp is not None
    
    def test_to_dict(self):
        """Test converting message to dictionary."""
        msg = Message("user", "Hello")
        data = msg.to_dict()
        
        assert data["role"] == "user"
        assert data["content"] == "Hello"
        assert "timestamp" in data
    
    def test_from_dict(self):
        """Test creating message from dictionary."""
        data = {
            "role": "assistant",
            "content": "Response",
            "metadata": {"score": 0.9},
            "timestamp": "2024-01-01T00:00:00"
        }
        
        msg = Message.from_dict(data)
        assert msg.role == "assistant"
        assert msg.content == "Response"
        assert msg.metadata["score"] == 0.9


class TestSessionManager:
    """Tests for SessionManager."""
    
    def test_create_session(self, tmp_path):
        """Test creating a session."""
        manager = SessionManager(storage_dir=str(tmp_path))
        
        memory = manager.create_session("test-session")
        assert memory.conversation_id == "test-session"
        assert "test-session" in manager.sessions
    
    def test_get_session(self, tmp_path):
        """Test getting a session."""
        manager = SessionManager(storage_dir=str(tmp_path))
        
        manager.create_session("test-session")
        memory = manager.get_session("test-session")
        
        assert memory is not None
        assert memory.conversation_id == "test-session"
    
    def test_get_or_create_session(self, tmp_path):
        """Test get or create session."""
        manager = SessionManager(storage_dir=str(tmp_path))
        
        # Create new
        memory1 = manager.get_or_create_session("new-session")
        assert memory1.conversation_id == "new-session"
        
        # Get existing
        memory2 = manager.get_or_create_session("new-session")
        assert memory1 is memory2
    
    def test_delete_session(self, tmp_path):
        """Test deleting a session."""
        manager = SessionManager(storage_dir=str(tmp_path))
        
        manager.create_session("test-session")
        assert manager.delete_session("test-session")
        assert manager.get_session("test-session") is None
    
    def test_list_sessions(self, tmp_path):
        """Test listing sessions."""
        manager = SessionManager(storage_dir=str(tmp_path))
        
        manager.create_session("session-1")
        manager.create_session("session-2")
        
        sessions = manager.list_sessions()
        assert len(sessions) == 2
        assert "session-1" in sessions
        assert "session-2" in sessions


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer."""
    
    def test_detect_language(self):
        """Test language detection."""
        analyzer = CodeAnalyzer()
        
        assert analyzer.detect_language("test.py") == "python"
        assert analyzer.detect_language("test.js") == "javascript"
        assert analyzer.detect_language("test.ts") == "typescript"
        assert analyzer.detect_language("test.java") == "java"
        assert analyzer.detect_language("test.txt") is None
    
    def test_extract_code_elements_python(self):
        """Test extracting Python code elements."""
        analyzer = CodeAnalyzer()
        
        code = """
def hello_world():
    print("Hello")

class MyClass:
    pass

import numpy as np
from typing import List
"""
        
        elements = analyzer.extract_code_elements(code, "python")
        
        assert "hello_world" in elements.get("function", [])
        assert "MyClass" in elements.get("class", [])
        assert len(elements.get("import", [])) > 0
    
    def test_extract_code_elements_javascript(self):
        """Test extracting JavaScript code elements."""
        analyzer = CodeAnalyzer()
        
        code = """
function myFunction() {
    return true;
}

class MyClass {
    constructor() {}
}

import React from 'react';
"""
        
        elements = analyzer.extract_code_elements(code, "javascript")
        
        assert "myFunction" in elements.get("function", [])
        assert "MyClass" in elements.get("class", [])
    
    def test_analyze_code_chunk(self):
        """Test analyzing a code chunk."""
        analyzer = CodeAnalyzer()
        
        chunk = {
            "text": "def test():\n    pass",
            "metadata": {"file_path": "test.py"}
        }
        
        analysis = analyzer.analyze_code_chunk(chunk)
        
        assert analysis["language"] == "python"
        assert analysis["is_code"] is True
        assert analysis["file_path"] == "test.py"
        assert "elements" in analysis
    
    def test_is_test_file(self):
        """Test identifying test files."""
        analyzer = CodeAnalyzer()
        
        assert analyzer._is_test_file("test_module.py")
        assert analyzer._is_test_file("tests/test_file.py")
        assert analyzer._is_test_file("module.test.js")
        assert not analyzer._is_test_file("module.py")
    
    def test_is_config_file(self):
        """Test identifying config files."""
        analyzer = CodeAnalyzer()
        
        assert analyzer._is_config_file("config.json")
        assert analyzer._is_config_file("settings.yaml")
        assert analyzer._is_config_file("package.json")
        assert not analyzer._is_config_file("module.py")
    
    def test_generate_code_context(self):
        """Test generating code context."""
        analyzer = CodeAnalyzer()
        
        results = [
            {
                "metadata": {
                    "text": "def hello():\n    pass",
                    "file_path": "test.py"
                },
                "score": 0.9
            }
        ]
        
        context = analyzer.generate_code_context(results)
        
        assert "test.py" in context
        assert "def hello()" in context
        assert "0.90" in context
    
    def test_identify_code_patterns(self):
        """Test identifying code patterns."""
        analyzer = CodeAnalyzer()
        
        code = """
async def fetch_data():
    try:
        result = await api.get()
    except Exception as e:
        handle_error(e)
"""
        
        patterns = analyzer.identify_code_patterns(code, "python")
        
        assert "Async/Await" in patterns
        assert "Exception Handling" in patterns


class TestVectorStoreIntegration:
    """Integration tests for vector store with embeddings."""
    
    @pytest.fixture
    def embedding_service(self):
        """Create embedding service for testing."""
        return EmbeddingService(model_name="all-MiniLM-L6-v2")
    
    @pytest.fixture
    def vector_store(self, embedding_service):
        """Create vector store for testing."""
        dimension = embedding_service.get_embedding_dimension()
        return VectorStore(dimension=dimension)
    
    def test_add_and_search(self, embedding_service, vector_store):
        """Test adding vectors and searching."""
        # Create test data
        texts = [
            "Python is a programming language",
            "JavaScript is used for web development",
            "Machine learning uses neural networks"
        ]
        
        # Generate embeddings
        embeddings = embedding_service.encode_text(texts)
        
        # Create metadata
        metadata = [
            {"text": text, "index": i}
            for i, text in enumerate(texts)
        ]
        
        # Add to vector store
        ids = vector_store.add_vectors(embeddings, metadata)
        assert len(ids) == 3
        
        # Search
        query = "programming language"
        query_embedding = embedding_service.encode_query(query)
        results = vector_store.search(query_embedding, k=2)
        
        assert len(results) == 2
        assert results[0]["metadata"]["text"] == texts[0]
    
    def test_save_and_load(self, vector_store, tmp_path):
        """Test saving and loading vector store."""
        # Add some data
        embeddings = np.random.rand(5, vector_store.dimension).astype(np.float32)
        metadata = [{"id": i} for i in range(5)]
        vector_store.add_vectors(embeddings, metadata)
        
        # Save
        save_path = tmp_path / "test_store"
        vector_store.save(str(save_path))
        
        # Load
        loaded_store = VectorStore.load(str(save_path))
        
        assert loaded_store.index.ntotal == 5
        assert len(loaded_store.metadata) == 5


@pytest.mark.asyncio
class TestAPIEndpoints:
    """Tests for API endpoints (requires mocking)."""
    
    @pytest.fixture
    def mock_chatbot(self):
        """Create mock chatbot."""
        chatbot = Mock()
        chatbot.chat.return_value = {
            "response": "Test response",
            "sources": [],
            "suggestions": [],
            "metadata": {}
        }
        return chatbot
    
    def test_chat_response_format(self, mock_chatbot):
        """Test chat response format."""
        response = mock_chatbot.chat(
            query="Test query",
            memory=None
        )
        
        assert "response" in response
        assert "sources" in response
        assert "suggestions" in response
        assert isinstance(response["response"], str)


# Made with Bob