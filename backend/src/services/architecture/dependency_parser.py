"""
Dependency parser for analyzing code dependencies and relationships.
"""
import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DependencyParser:
    """Parse and analyze code dependencies."""
    
    def __init__(self):
        self.file_dependencies: Dict[str, Set[str]] = {}
        self.import_graph: Dict[str, List[Dict]] = {}
        self.function_calls: Dict[str, List[str]] = {}
        
    def parse_python_file(self, file_path: str) -> Dict:
        """
        Parse a Python file for dependencies.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dictionary with imports, functions, classes, and dependencies
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            imports = []
            functions = []
            classes = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            'type': 'import',
                            'module': alias.name,
                            'alias': alias.asname
                        })
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.append({
                            'type': 'from_import',
                            'module': module,
                            'name': alias.name,
                            'alias': alias.asname
                        })
                
                elif isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'line': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'decorators': [self._get_decorator_name(d) for d in node.decorator_list]
                    })
                
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'line': node.lineno,
                        'bases': [self._get_base_name(base) for base in node.bases],
                        'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                    })
            
            return {
                'file_path': file_path,
                'imports': imports,
                'functions': functions,
                'classes': classes
            }
        
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return {
                'file_path': file_path,
                'imports': [],
                'functions': [],
                'classes': [],
                'error': str(e)
            }
    
    def parse_javascript_file(self, file_path: str) -> Dict:
        """
        Parse a JavaScript/TypeScript file for dependencies.
        
        Args:
            file_path: Path to JS/TS file
            
        Returns:
            Dictionary with imports, functions, and exports
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            imports = []
            exports = []
            functions = []
            
            # Parse imports (ES6 and CommonJS)
            import_patterns = [
                r'import\s+(?:{([^}]+)}|(\w+))\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'import\s+\*\s+as\s+(\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
                r'const\s+(?:{([^}]+)}|(\w+))\s*=\s*require\([\'"]([^\'"]+)[\'"]\)',
            ]
            
            for pattern in import_patterns:
                for match in re.finditer(pattern, content):
                    groups = match.groups()
                    if 'import' in pattern:
                        imports.append({
                            'type': 'es6_import',
                            'names': groups[0] or groups[1] or groups[2],
                            'source': groups[-1]
                        })
                    else:
                        imports.append({
                            'type': 'require',
                            'names': groups[0] or groups[1],
                            'source': groups[-1]
                        })
            
            # Parse exports
            export_patterns = [
                r'export\s+(?:default\s+)?(?:function|class|const|let|var)\s+(\w+)',
                r'export\s+{([^}]+)}',
                r'module\.exports\s*=\s*(\w+)',
            ]
            
            for pattern in export_patterns:
                for match in re.finditer(pattern, content):
                    exports.append({
                        'type': 'export',
                        'name': match.group(1)
                    })
            
            # Parse function declarations
            func_pattern = r'(?:function|const|let|var)\s+(\w+)\s*=?\s*(?:\([^)]*\)|async\s*\([^)]*\))\s*(?:=>)?\s*{'
            for match in re.finditer(func_pattern, content):
                functions.append({
                    'name': match.group(1),
                    'type': 'function'
                })
            
            return {
                'file_path': file_path,
                'imports': imports,
                'exports': exports,
                'functions': functions
            }
        
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return {
                'file_path': file_path,
                'imports': [],
                'exports': [],
                'functions': [],
                'error': str(e)
            }
    
    def parse_directory(self, directory: str, file_patterns: Optional[List[str]] = None) -> Dict:
        """
        Parse all files in a directory.
        
        Args:
            directory: Directory path
            file_patterns: List of file patterns to include
            
        Returns:
            Dictionary with all parsed files
        """
        if file_patterns is None:
            file_patterns = ['*.py', '*.js', '*.ts', '*.tsx', '*.jsx']
        
        parsed_files = {}
        directory_path = Path(directory)
        
        for pattern in file_patterns:
            for file_path in directory_path.rglob(pattern):
                if self._should_skip_file(str(file_path)):
                    continue
                
                file_str = str(file_path)
                
                if pattern == '*.py':
                    parsed_files[file_str] = self.parse_python_file(file_str)
                elif pattern in ['*.js', '*.ts', '*.tsx', '*.jsx']:
                    parsed_files[file_str] = self.parse_javascript_file(file_str)
        
        return parsed_files
    
    def build_dependency_graph(self, parsed_files: Dict) -> Dict:
        """
        Build a dependency graph from parsed files.
        
        Args:
            parsed_files: Dictionary of parsed files
            
        Returns:
            Dependency graph with nodes and edges
        """
        nodes = []
        edges = []
        node_map = {}
        
        # Create nodes for each file
        for file_path, data in parsed_files.items():
            node_id = self._get_node_id(file_path)
            node_type = self._get_file_type(file_path)
            
            node = {
                'id': node_id,
                'label': Path(file_path).name,
                'type': node_type,
                'path': file_path,
                'functions': len(data.get('functions', [])),
                'classes': len(data.get('classes', [])),
                'imports': len(data.get('imports', []))
            }
            
            nodes.append(node)
            node_map[file_path] = node_id
        
        # Create edges for dependencies
        for file_path, data in parsed_files.items():
            source_id = node_map.get(file_path)
            if not source_id:
                continue
            
            imports = data.get('imports', [])
            for imp in imports:
                # Try to resolve import to actual file
                target_path = self._resolve_import(file_path, imp, parsed_files)
                if target_path and target_path in node_map:
                    target_id = node_map[target_path]
                    
                    edge = {
                        'id': f"{source_id}-{target_id}",
                        'source': source_id,
                        'target': target_id,
                        'type': imp.get('type', 'import'),
                        'label': imp.get('module', imp.get('source', ''))
                    }
                    
                    edges.append(edge)
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_files': len(nodes),
                'total_dependencies': len(edges),
                'file_types': self._count_file_types(nodes)
            }
        }
    
    def _get_decorator_name(self, decorator) -> str:
        """Get decorator name from AST node."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        return 'unknown'
    
    def _get_base_name(self, base) -> str:
        """Get base class name from AST node."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{self._get_base_name(base.value)}.{base.attr}"
        return 'unknown'
    
    def _should_skip_file(self, file_path: str) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            'node_modules',
            '__pycache__',
            '.git',
            'venv',
            'dist',
            'build',
            '.next',
            'target'
        ]
        
        return any(pattern in file_path for pattern in skip_patterns)
    
    def _get_node_id(self, file_path: str) -> str:
        """Generate unique node ID from file path."""
        return file_path.replace('/', '_').replace('\\', '_').replace('.', '_')
    
    def _get_file_type(self, file_path: str) -> str:
        """Get file type from extension."""
        ext = Path(file_path).suffix
        type_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript-react',
            '.jsx': 'javascript-react'
        }
        return type_map.get(ext, 'unknown')
    
    def _resolve_import(self, source_file: str, import_data: Dict, parsed_files: Dict) -> Optional[str]:
        """
        Resolve import to actual file path.
        
        Args:
            source_file: Source file path
            import_data: Import data dictionary
            parsed_files: All parsed files
            
        Returns:
            Resolved file path or None
        """
        module = import_data.get('module') or import_data.get('source', '')
        
        # Handle relative imports
        if module.startswith('.'):
            source_dir = Path(source_file).parent
            
            # Count leading dots
            level = len(module) - len(module.lstrip('.'))
            module_path = module.lstrip('.')
            
            # Go up directories
            target_dir = source_dir
            for _ in range(level - 1):
                target_dir = target_dir.parent
            
            # Try different extensions
            for ext in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                potential_path = str(target_dir / f"{module_path}{ext}")
                if potential_path in parsed_files:
                    return potential_path
                
                # Try as directory with index file
                potential_path = str(target_dir / module_path / f"index{ext}")
                if potential_path in parsed_files:
                    return potential_path
        
        # Handle absolute imports (simplified)
        for file_path in parsed_files.keys():
            if module in file_path:
                return file_path
        
        return None
    
    def _count_file_types(self, nodes: List[Dict]) -> Dict[str, int]:
        """Count files by type."""
        counts = {}
        for node in nodes:
            file_type = node.get('type', 'unknown')
            counts[file_type] = counts.get(file_type, 0) + 1
        return counts


# Made with Bob