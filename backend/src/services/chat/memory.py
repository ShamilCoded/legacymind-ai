"""
Conversational memory service for maintaining chat history and context.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque
import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Message:
    """Represents a single message in the conversation."""
    
    def __init__(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize a message.
        
        Args:
            role: Role of the message sender ('user', 'assistant', 'system')
            content: Message content
            metadata: Optional metadata (sources, scores, etc.)
            timestamp: Message timestamp
        """
        self.role = role
        self.content = content
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'role': self.role,
            'content': self.content,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        return cls(
            role=data['role'],
            content=data['content'],
            metadata=data.get('metadata', {}),
            timestamp=datetime.fromisoformat(data['timestamp'])
        )


class ConversationMemory:
    """Manages conversation history with configurable retention."""
    
    def __init__(
        self,
        max_messages: int = 50,
        max_tokens: Optional[int] = None,
        summary_threshold: int = 20
    ):
        """
        Initialize conversation memory.
        
        Args:
            max_messages: Maximum number of messages to retain
            max_tokens: Maximum tokens to retain (approximate)
            summary_threshold: Number of messages before summarization
        """
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.summary_threshold = summary_threshold
        
        self.messages: deque = deque(maxlen=max_messages)
        self.summary: Optional[str] = None
        self.conversation_id: Optional[str] = None
    
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add a message to the conversation.
        
        Args:
            role: Message role
            content: Message content
            metadata: Optional metadata
            
        Returns:
            Created message
        """
        message = Message(role, content, metadata)
        self.messages.append(message)
        
        logger.debug(f"Added {role} message. Total messages: {len(self.messages)}")
        
        # Check if summarization is needed
        if len(self.messages) >= self.summary_threshold:
            self._maybe_summarize()
        
        return message
    
    def get_messages(
        self,
        limit: Optional[int] = None,
        role_filter: Optional[str] = None
    ) -> List[Message]:
        """
        Get messages from conversation history.
        
        Args:
            limit: Maximum number of messages to return
            role_filter: Filter by role
            
        Returns:
            List of messages
        """
        messages = list(self.messages)
        
        if role_filter:
            messages = [m for m in messages if m.role == role_filter]
        
        if limit:
            messages = messages[-limit:]
        
        return messages
    
    def get_context(
        self,
        max_messages: int = 10,
        include_summary: bool = True
    ) -> List[Dict[str, str]]:
        """
        Get conversation context for LLM.
        
        Args:
            max_messages: Maximum recent messages to include
            include_summary: Whether to include conversation summary
            
        Returns:
            List of message dicts for LLM context
        """
        context = []
        
        # Add summary if available
        if include_summary and self.summary:
            context.append({
                'role': 'system',
                'content': f"Previous conversation summary: {self.summary}"
            })
        
        # Add recent messages
        recent_messages = list(self.messages)[-max_messages:]
        for msg in recent_messages:
            context.append({
                'role': msg.role,
                'content': msg.content
            })
        
        return context
    
    def get_relevant_context(
        self,
        query: str,
        max_messages: int = 5
    ) -> List[Message]:
        """
        Get contextually relevant messages based on query.
        
        Args:
            query: Current query
            max_messages: Maximum messages to return
            
        Returns:
            List of relevant messages
        """
        # Simple keyword-based relevance (can be enhanced with embeddings)
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        scored_messages = []
        for msg in self.messages:
            if msg.role == 'system':
                continue
            
            content_lower = msg.content.lower()
            content_words = set(content_lower.split())
            
            # Calculate overlap score
            overlap = len(query_words & content_words)
            if overlap > 0:
                scored_messages.append((overlap, msg))
        
        # Sort by relevance and return top messages
        scored_messages.sort(reverse=True, key=lambda x: x[0])
        return [msg for _, msg in scored_messages[:max_messages]]
    
    def clear(self) -> None:
        """Clear conversation history."""
        self.messages.clear()
        self.summary = None
        logger.info("Conversation memory cleared")
    
    def _maybe_summarize(self) -> None:
        """
        Summarize old messages if threshold is reached.
        Note: This is a placeholder. Actual summarization would use an LLM.
        """
        if len(self.messages) < self.summary_threshold:
            return
        
        # Simple summarization: keep track of topics discussed
        topics = set()
        for msg in list(self.messages)[:self.summary_threshold // 2]:
            if msg.role == 'user':
                # Extract key terms (simplified)
                words = msg.content.lower().split()
                topics.update([w for w in words if len(w) > 5])
        
        if topics:
            self.summary = f"Discussed: {', '.join(list(topics)[:10])}"
            logger.info(f"Created conversation summary: {self.summary}")
    
    def save(self, filepath: str) -> None:
        """
        Save conversation to file.
        
        Args:
            filepath: Path to save file
        """
        data = {
            'conversation_id': self.conversation_id,
            'summary': self.summary,
            'messages': [msg.to_dict() for msg in self.messages],
            'config': {
                'max_messages': self.max_messages,
                'max_tokens': self.max_tokens,
                'summary_threshold': self.summary_threshold
            }
        }
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Saved conversation to {filepath}")
    
    @classmethod
    def load(cls, filepath: str) -> 'ConversationMemory':
        """
        Load conversation from file.
        
        Args:
            filepath: Path to load from
            
        Returns:
            Loaded ConversationMemory instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        config = data.get('config', {})
        memory = cls(
            max_messages=config.get('max_messages', 50),
            max_tokens=config.get('max_tokens'),
            summary_threshold=config.get('summary_threshold', 20)
        )
        
        memory.conversation_id = data.get('conversation_id')
        memory.summary = data.get('summary')
        
        for msg_data in data.get('messages', []):
            msg = Message.from_dict(msg_data)
            memory.messages.append(msg)
        
        logger.info(f"Loaded conversation from {filepath}")
        return memory
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get conversation statistics.
        
        Returns:
            Dictionary with statistics
        """
        user_messages = sum(1 for m in self.messages if m.role == 'user')
        assistant_messages = sum(1 for m in self.messages if m.role == 'assistant')
        
        return {
            'total_messages': len(self.messages),
            'user_messages': user_messages,
            'assistant_messages': assistant_messages,
            'has_summary': self.summary is not None,
            'conversation_id': self.conversation_id
        }


class SessionManager:
    """Manages multiple conversation sessions."""
    
    def __init__(self, storage_dir: str = "./chat_sessions"):
        """
        Initialize session manager.
        
        Args:
            storage_dir: Directory to store sessions
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, ConversationMemory] = {}
    
    def create_session(
        self,
        session_id: str,
        max_messages: int = 50
    ) -> ConversationMemory:
        """
        Create a new conversation session.
        
        Args:
            session_id: Unique session identifier
            max_messages: Maximum messages to retain
            
        Returns:
            New ConversationMemory instance
        """
        memory = ConversationMemory(max_messages=max_messages)
        memory.conversation_id = session_id
        self.sessions[session_id] = memory
        
        logger.info(f"Created session: {session_id}")
        return memory
    
    def get_session(self, session_id: str) -> Optional[ConversationMemory]:
        """
        Get existing session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            ConversationMemory instance or None
        """
        return self.sessions.get(session_id)
    
    def get_or_create_session(
        self,
        session_id: str,
        max_messages: int = 50
    ) -> ConversationMemory:
        """
        Get existing session or create new one.
        
        Args:
            session_id: Session identifier
            max_messages: Maximum messages for new session
            
        Returns:
            ConversationMemory instance
        """
        if session_id in self.sessions:
            return self.sessions[session_id]
        return self.create_session(session_id, max_messages)
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            
            # Delete saved file if exists
            filepath = self.storage_dir / f"{session_id}.json"
            if filepath.exists():
                filepath.unlink()
            
            logger.info(f"Deleted session: {session_id}")
            return True
        return False
    
    def save_session(self, session_id: str) -> bool:
        """
        Save session to disk.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if saved, False if not found
        """
        memory = self.sessions.get(session_id)
        if memory:
            filepath = self.storage_dir / f"{session_id}.json"
            memory.save(str(filepath))
            return True
        return False
    
    def load_session(self, session_id: str) -> Optional[ConversationMemory]:
        """
        Load session from disk.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Loaded ConversationMemory or None
        """
        filepath = self.storage_dir / f"{session_id}.json"
        if filepath.exists():
            memory = ConversationMemory.load(str(filepath))
            self.sessions[session_id] = memory
            return memory
        return None
    
    def list_sessions(self) -> List[str]:
        """
        List all active session IDs.
        
        Returns:
            List of session IDs
        """
        return list(self.sessions.keys())


# Made with Bob