"""
Graph generator for creating architecture visualizations.
"""
from typing import Dict, List, Optional, Set
from pathlib import Path
import logging

from .dependency_parser import DependencyParser

logger = logging.getLogger(__name__)


class GraphGenerator:
    """Generate architecture visualization graphs."""
    
    def __init__(self):
        self.parser = DependencyParser()
        
    def generate_architecture_graph(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        max_depth: Optional[int] = None
    ) -> Dict:
        """
        Generate complete architecture graph.
        
        Args:
            directory: Root directory to analyze
            file_patterns: File patterns to include
            max_depth: Maximum directory depth
            
        Returns:
            Graph data with nodes and edges
        """
        logger.info(f"Generating architecture graph for {directory}")
        
        # Parse all files
        parsed_files = self.parser.parse_directory(directory, file_patterns)
        
        # Build dependency graph
        graph = self.parser.build_dependency_graph(parsed_files)
        
        # Add module grouping
        graph['modules'] = self._group_by_module(graph['nodes'], directory)
        
        # Add architecture layers
        graph['layers'] = self._detect_layers(graph['nodes'], parsed_files)
        
        # Calculate metrics
        graph['metrics'] = self._calculate_metrics(graph)
        
        logger.info(f"Generated graph with {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
        
        return graph
    
    def generate_module_graph(self, directory: str, module_path: str) -> Dict:
        """
        Generate graph for a specific module.
        
        Args:
            directory: Root directory
            module_path: Path to specific module
            
        Returns:
            Module-specific graph
        """
        parsed_files = self.parser.parse_directory(directory)
        full_graph = self.parser.build_dependency_graph(parsed_files)
        
        # Filter to module
        module_nodes = [
            node for node in full_graph['nodes']
            if module_path in node['path']
        ]
        
        module_node_ids = {node['id'] for node in module_nodes}
        
        module_edges = [
            edge for edge in full_graph['edges']
            if edge['source'] in module_node_ids or edge['target'] in module_node_ids
        ]
        
        return {
            'nodes': module_nodes,
            'edges': module_edges,
            'stats': {
                'total_files': len(module_nodes),
                'total_dependencies': len(module_edges)
            }
        }
    
    def generate_api_relationship_graph(self, directory: str) -> Dict:
        """
        Generate graph showing API relationships.
        
        Args:
            directory: Root directory
            
        Returns:
            API relationship graph
        """
        parsed_files = self.parser.parse_directory(directory)
        
        api_nodes = []
        api_edges = []
        
        # Find API endpoints
        for file_path, data in parsed_files.items():
            if 'api' in file_path.lower() or 'route' in file_path.lower():
                functions = data.get('functions', [])
                
                for func in functions:
                    # Check if it's an API endpoint
                    decorators = func.get('decorators', [])
                    if any(d in ['app.get', 'app.post', 'app.put', 'app.delete', 'router.get', 'router.post'] 
                           for d in decorators):
                        
                        node = {
                            'id': f"{file_path}_{func['name']}",
                            'label': func['name'],
                            'type': 'api_endpoint',
                            'file': file_path,
                            'method': self._extract_http_method(decorators)
                        }
                        api_nodes.append(node)
        
        # Find service dependencies
        full_graph = self.parser.build_dependency_graph(parsed_files)
        
        for edge in full_graph['edges']:
            # Check if edge connects API to service
            source_is_api = any(node['id'] == edge['source'] and node['type'] == 'api_endpoint' 
                               for node in api_nodes)
            
            if source_is_api:
                api_edges.append(edge)
        
        return {
            'nodes': api_nodes,
            'edges': api_edges,
            'stats': {
                'total_endpoints': len(api_nodes),
                'total_connections': len(api_edges)
            }
        }
    
    def generate_dependency_tree(self, directory: str, target_file: str) -> Dict:
        """
        Generate dependency tree for a specific file.
        
        Args:
            directory: Root directory
            target_file: Target file to analyze
            
        Returns:
            Dependency tree
        """
        parsed_files = self.parser.parse_directory(directory)
        full_graph = self.parser.build_dependency_graph(parsed_files)
        
        # Find target node
        target_node = None
        for node in full_graph['nodes']:
            if target_file in node['path']:
                target_node = node
                break
        
        if not target_node:
            return {
                'error': 'Target file not found',
                'nodes': [],
                'edges': []
            }
        
        # Build tree
        visited = set()
        tree_nodes = []
        tree_edges = []
        
        def traverse(node_id: str, depth: int = 0):
            if node_id in visited or depth > 5:  # Prevent infinite loops
                return
            
            visited.add(node_id)
            
            # Find node
            node = next((n for n in full_graph['nodes'] if n['id'] == node_id), None)
            if node:
                tree_nodes.append({**node, 'depth': depth})
            
            # Find dependencies
            for edge in full_graph['edges']:
                if edge['source'] == node_id:
                    tree_edges.append(edge)
                    traverse(edge['target'], depth + 1)
        
        traverse(target_node['id'])
        
        return {
            'root': target_node,
            'nodes': tree_nodes,
            'edges': tree_edges,
            'stats': {
                'total_dependencies': len(tree_nodes) - 1,
                'max_depth': max((n.get('depth', 0) for n in tree_nodes), default=0)
            }
        }
    
    def _group_by_module(self, nodes: List[Dict], root_dir: str) -> List[Dict]:
        """Group nodes by module/directory."""
        modules = {}
        
        for node in nodes:
            path = Path(node['path'])
            relative_path = path.relative_to(root_dir) if root_dir else path
            
            # Get first directory as module
            parts = relative_path.parts
            if len(parts) > 1:
                module_name = parts[0]
            else:
                module_name = 'root'
            
            if module_name not in modules:
                modules[module_name] = {
                    'name': module_name,
                    'files': [],
                    'file_count': 0
                }
            
            modules[module_name]['files'].append(node['id'])
            modules[module_name]['file_count'] += 1
        
        return list(modules.values())
    
    def _detect_layers(self, nodes: List[Dict], parsed_files: Dict) -> List[Dict]:
        """Detect architectural layers."""
        layers = {
            'api': {'name': 'API Layer', 'files': []},
            'service': {'name': 'Service Layer', 'files': []},
            'data': {'name': 'Data Layer', 'files': []},
            'util': {'name': 'Utility Layer', 'files': []},
            'other': {'name': 'Other', 'files': []}
        }
        
        for node in nodes:
            path = node['path'].lower()
            
            if 'api' in path or 'route' in path or 'endpoint' in path:
                layers['api']['files'].append(node['id'])
            elif 'service' in path or 'business' in path:
                layers['service']['files'].append(node['id'])
            elif 'model' in path or 'schema' in path or 'db' in path or 'database' in path:
                layers['data']['files'].append(node['id'])
            elif 'util' in path or 'helper' in path or 'common' in path:
                layers['util']['files'].append(node['id'])
            else:
                layers['other']['files'].append(node['id'])
        
        return [
            {**layer, 'file_count': len(layer['files'])}
            for layer in layers.values()
            if layer['files']
        ]
    
    def _calculate_metrics(self, graph: Dict) -> Dict:
        """Calculate graph metrics."""
        nodes = graph['nodes']
        edges = graph['edges']
        
        # Calculate in-degree and out-degree
        in_degree = {}
        out_degree = {}
        
        for edge in edges:
            source = edge['source']
            target = edge['target']
            
            out_degree[source] = out_degree.get(source, 0) + 1
            in_degree[target] = in_degree.get(target, 0) + 1
        
        # Find most connected files
        most_imported = sorted(
            [(node_id, count) for node_id, count in in_degree.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        most_importing = sorted(
            [(node_id, count) for node_id, count in out_degree.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            'total_nodes': len(nodes),
            'total_edges': len(edges),
            'avg_dependencies': len(edges) / len(nodes) if nodes else 0,
            'most_imported': [
                {'node_id': node_id, 'count': count}
                for node_id, count in most_imported
            ],
            'most_importing': [
                {'node_id': node_id, 'count': count}
                for node_id, count in most_importing
            ],
            'isolated_nodes': len([n for n in nodes if n['id'] not in in_degree and n['id'] not in out_degree])
        }
    
    def _extract_http_method(self, decorators: List[str]) -> str:
        """Extract HTTP method from decorators."""
        for decorator in decorators:
            if 'get' in decorator.lower():
                return 'GET'
            elif 'post' in decorator.lower():
                return 'POST'
            elif 'put' in decorator.lower():
                return 'PUT'
            elif 'delete' in decorator.lower():
                return 'DELETE'
            elif 'patch' in decorator.lower():
                return 'PATCH'
        return 'UNKNOWN'


# Made with Bob