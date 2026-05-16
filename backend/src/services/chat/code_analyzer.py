"""
Code-aware analysis and response generation for repository chatbot.
"""
from typing import List, Dict, Any, Optional, Set
import re
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class CodeAnalyzer:
    """Analyzes code context and provides code-aware insights."""
    
    # Language-specific patterns
    LANGUAGE_PATTERNS = {
        'python': {
            'function': r'def\s+(\w+)\s*\(',
            'class': r'class\s+(\w+)',
            'import': r'(?:from\s+[\w.]+\s+)?import\s+([\w,\s]+)',
            'decorator': r'@(\w+)',
            'comment': r'#.*$'
        },
        'javascript': {
            'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\()',
            'class': r'class\s+(\w+)',
            'import': r'import\s+.*?from\s+[\'"](.+?)[\'"]',
            'export': r'export\s+(?:default\s+)?(?:class|function|const)\s+(\w+)',
            'comment': r'//.*$|/\*[\s\S]*?\*/'
        },
        'typescript': {
            'function': r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\()',
            'class': r'class\s+(\w+)',
            'interface': r'interface\s+(\w+)',
            'type': r'type\s+(\w+)',
            'import': r'import\s+.*?from\s+[\'"](.+?)[\'"]',
            'comment': r'//.*$|/\*[\s\S]*?\*/'
        },
        'java': {
            'function': r'(?:public|private|protected)?\s*(?:static\s+)?[\w<>]+\s+(\w+)\s*\(',
            'class': r'(?:public\s+)?class\s+(\w+)',
            'interface': r'interface\s+(\w+)',
            'import': r'import\s+([\w.]+)',
            'comment': r'//.*$|/\*[\s\S]*?\*/'
        }
    }
    
    def __init__(self):
        """Initialize code analyzer."""
        self.file_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust'
        }
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """
        Detect programming language from file extension.
        
        Args:
            file_path: Path to file
            
        Returns:
            Language name or None
        """
        ext = Path(file_path).suffix.lower()
        return self.file_extensions.get(ext)
    
    def extract_code_elements(
        self,
        code: str,
        language: str
    ) -> Dict[str, List[str]]:
        """
        Extract code elements (functions, classes, etc.) from code.
        
        Args:
            code: Source code text
            language: Programming language
            
        Returns:
            Dictionary of element types and their names
        """
        elements = {}
        patterns = self.LANGUAGE_PATTERNS.get(language, {})
        
        for element_type, pattern in patterns.items():
            matches = re.findall(pattern, code, re.MULTILINE)
            # Flatten tuples from multiple capture groups
            names = []
            for match in matches:
                if isinstance(match, tuple):
                    names.extend([m for m in match if m])
                else:
                    names.append(match)
            elements[element_type] = names
        
        return elements
    
    def analyze_code_chunk(
        self,
        chunk: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a code chunk and extract metadata.
        
        Args:
            chunk: Chunk dictionary with text and metadata
            
        Returns:
            Enhanced chunk with code analysis
        """
        file_path = chunk.get('metadata', {}).get('file_path', '')
        text = chunk.get('text', '')
        
        language = self.detect_language(file_path)
        
        analysis = {
            'language': language,
            'is_code': language is not None,
            'file_path': file_path,
            'elements': {}
        }
        
        if language and language in self.LANGUAGE_PATTERNS:
            analysis['elements'] = self.extract_code_elements(text, language)
        
        # Add line count
        analysis['line_count'] = len(text.split('\n'))
        
        # Detect if it's a test file
        analysis['is_test'] = self._is_test_file(file_path)
        
        # Detect if it's a config file
        analysis['is_config'] = self._is_config_file(file_path)
        
        return analysis
    
    def _is_test_file(self, file_path: str) -> bool:
        """Check if file is a test file."""
        path_lower = file_path.lower()
        return any(pattern in path_lower for pattern in [
            'test_', '_test.', 'tests/', '/test/', '.test.', '.spec.'
        ])
    
    def _is_config_file(self, file_path: str) -> bool:
        """Check if file is a configuration file."""
        path_lower = file_path.lower()
        config_extensions = ['.json', '.yaml', '.yml', '.toml', '.ini', '.env']
        config_names = ['config', 'settings', 'package.json', 'tsconfig']
        
        return (
            any(path_lower.endswith(ext) for ext in config_extensions) or
            any(name in path_lower for name in config_names)
        )
    
    def find_related_code(
        self,
        results: List[Dict[str, Any]],
        query_type: str = 'general'
    ) -> List[Dict[str, Any]]:
        """
        Find and group related code chunks.
        
        Args:
            results: Search results
            query_type: Type of query (function, class, import, etc.)
            
        Returns:
            Grouped and prioritized results
        """
        # Analyze all results
        analyzed_results = []
        for result in results:
            analysis = self.analyze_code_chunk(result)
            result['code_analysis'] = analysis
            analyzed_results.append(result)
        
        # Prioritize based on query type
        if query_type == 'function':
            # Prioritize chunks with function definitions
            analyzed_results.sort(
                key=lambda x: len(x['code_analysis']['elements'].get('function', [])),
                reverse=True
            )
        elif query_type == 'class':
            # Prioritize chunks with class definitions
            analyzed_results.sort(
                key=lambda x: len(x['code_analysis']['elements'].get('class', [])),
                reverse=True
            )
        elif query_type == 'architecture':
            # Prioritize config and main files
            analyzed_results.sort(
                key=lambda x: (
                    x['code_analysis']['is_config'],
                    'main' in x['code_analysis']['file_path'].lower()
                ),
                reverse=True
            )
        
        return analyzed_results
    
    def generate_code_context(
        self,
        results: List[Dict[str, Any]],
        max_context_length: int = 3000
    ) -> str:
        """
        Generate formatted code context for LLM.
        
        Args:
            results: Search results with code
            max_context_length: Maximum context length
            
        Returns:
            Formatted context string
        """
        context_parts = []
        current_length = 0
        
        for result in results:
            metadata = result.get('metadata', {})
            text = metadata.get('text', '')
            file_path = metadata.get('file_path', 'unknown')
            score = result.get('score', 0)
            
            # Analyze code
            analysis = self.analyze_code_chunk({'text': text, 'metadata': metadata})
            
            # Format context entry
            entry = f"\n--- File: {file_path} (relevance: {score:.2f}) ---\n"
            
            if analysis['is_code'] and analysis['elements']:
                # Add code element summary
                elements_summary = []
                for elem_type, names in analysis['elements'].items():
                    if names and elem_type != 'comment':
                        elements_summary.append(f"{elem_type}s: {', '.join(names[:5])}")
                
                if elements_summary:
                    entry += f"Contains: {'; '.join(elements_summary)}\n"
            
            entry += f"\n{text}\n"
            
            # Check length
            if current_length + len(entry) > max_context_length:
                break
            
            context_parts.append(entry)
            current_length += len(entry)
        
        return '\n'.join(context_parts)
    
    def extract_dependencies(
        self,
        results: List[Dict[str, Any]]
    ) -> Dict[str, Set[str]]:
        """
        Extract dependencies from code results.
        
        Args:
            results: Search results
            
        Returns:
            Dictionary mapping files to their dependencies
        """
        dependencies = {}
        
        for result in results:
            metadata = result.get('metadata', {})
            file_path = metadata.get('file_path', '')
            text = metadata.get('text', '')
            
            language = self.detect_language(file_path)
            if not language:
                continue
            
            # Extract imports/dependencies
            elements = self.extract_code_elements(text, language)
            imports = elements.get('import', [])
            
            if imports:
                dependencies[file_path] = set(imports)
        
        return dependencies
    
    def identify_code_patterns(
        self,
        code: str,
        language: str
    ) -> List[str]:
        """
        Identify common code patterns and design patterns.
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            List of identified patterns
        """
        patterns = []
        
        # Check for common patterns
        if 'singleton' in code.lower():
            patterns.append('Singleton Pattern')
        
        if 'factory' in code.lower():
            patterns.append('Factory Pattern')
        
        if re.search(r'class\s+\w+\(.*\):', code):
            patterns.append('Inheritance')
        
        if '@' in code and language == 'python':
            patterns.append('Decorators')
        
        if 'async' in code or 'await' in code:
            patterns.append('Async/Await')
        
        if 'try:' in code or 'except' in code:
            patterns.append('Exception Handling')
        
        return patterns
    
    def suggest_related_queries(
        self,
        query: str,
        results: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Suggest related queries based on results.
        
        Args:
            query: Original query
            results: Search results
            
        Returns:
            List of suggested queries
        """
        suggestions = []
        
        # Extract common elements from results
        all_functions = set()
        all_classes = set()
        
        for result in results:
            analysis = self.analyze_code_chunk(result)
            all_functions.update(analysis['elements'].get('function', []))
            all_classes.update(analysis['elements'].get('class', []))
        
        # Generate suggestions
        if all_functions:
            func_list = list(all_functions)[:3]
            suggestions.append(f"How does {func_list[0]} work?")
        
        if all_classes:
            class_list = list(all_classes)[:3]
            suggestions.append(f"Explain the {class_list[0]} class")
        
        suggestions.append(f"Show me tests for {query}")
        suggestions.append(f"What are the dependencies of {query}?")
        
        return suggestions[:5]


# Made with Bob