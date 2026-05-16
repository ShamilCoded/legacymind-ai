"""
Risk detection algorithms for code analysis.
"""
import ast
import os
import re
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import logging
from collections import defaultdict, deque

from .models import (
    CircularDependency, DeadCodeItem, CouplingMetrics,
    TestCoverageReport, RiskyFile, ComplexityMetrics, RiskLevel
)

logger = logging.getLogger(__name__)


class CircularDependencyDetector:
    """Detect circular dependencies in code."""
    
    def __init__(self):
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        self.cycles: List[List[str]] = []
    
    def detect(self, parsed_files: Dict[str, Dict]) -> List[CircularDependency]:
        """
        Detect circular dependencies.
        
        Args:
            parsed_files: Dictionary of parsed file data
            
        Returns:
            List of circular dependencies found
        """
        # Build dependency graph
        self._build_graph(parsed_files)
        
        # Find cycles using DFS
        self._find_cycles()
        
        # Convert to CircularDependency objects
        results = []
        for cycle in self.cycles:
            cycle_length = len(cycle)
            
            # Determine risk level based on cycle length
            if cycle_length >= 5:
                risk_level = RiskLevel.CRITICAL
                impact = 90 + min(cycle_length - 5, 10)
            elif cycle_length >= 3:
                risk_level = RiskLevel.HIGH
                impact = 70 + (cycle_length - 3) * 10
            else:
                risk_level = RiskLevel.MEDIUM
                impact = 50 + cycle_length * 10
            
            results.append(CircularDependency(
                cycle=cycle,
                cycle_length=cycle_length,
                risk_level=risk_level,
                impact_score=min(impact, 100),
                description=f"Circular dependency involving {cycle_length} files: {' -> '.join([Path(f).name for f in cycle[:3]])}..."
            ))
        
        return results
    
    def _build_graph(self, parsed_files: Dict[str, Dict]):
        """Build dependency graph from parsed files."""
        self.dependency_graph.clear()
        
        for file_path, data in parsed_files.items():
            imports = data.get('imports', [])
            for imp in imports:
                # Resolve import to file path
                target = self._resolve_import(file_path, imp, parsed_files)
                if target and target in parsed_files:
                    self.dependency_graph[file_path].add(target)
    
    def _find_cycles(self):
        """Find all cycles in the dependency graph using DFS."""
        self.cycles.clear()
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    if cycle not in self.cycles:
                        self.cycles.append(cycle)
            
            path.pop()
            rec_stack.remove(node)
            return False
        
        for node in self.dependency_graph:
            if node not in visited:
                dfs(node)
    
    def _resolve_import(self, source_file: str, import_data: Dict, parsed_files: Dict) -> Optional[str]:
        """Resolve import to actual file path."""
        module = import_data.get('module') or import_data.get('source', '')
        
        if module.startswith('.'):
            source_dir = Path(source_file).parent
            level = len(module) - len(module.lstrip('.'))
            module_path = module.lstrip('.')
            
            target_dir = source_dir
            for _ in range(level - 1):
                target_dir = target_dir.parent
            
            for ext in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                potential_path = str(target_dir / f"{module_path}{ext}")
                if potential_path in parsed_files:
                    return potential_path
        
        return None


class DeadCodeDetector:
    """Detect potentially dead/unused code."""
    
    def detect(self, parsed_files: Dict[str, Dict]) -> List[DeadCodeItem]:
        """
        Detect dead code in parsed files.
        
        Args:
            parsed_files: Dictionary of parsed file data
            
        Returns:
            List of dead code items found
        """
        results = []
        
        # Build usage map
        defined_items = self._build_definition_map(parsed_files)
        used_items = self._build_usage_map(parsed_files)
        
        # Find unused items
        for file_path, items in defined_items.items():
            for item in items:
                item_name = item['name']
                item_type = item['type']
                
                # Check if item is used
                is_used = self._is_item_used(item_name, file_path, used_items)
                
                # Check if it's exported (might be used externally)
                is_exported = self._is_exported(item_name, file_path, parsed_files)
                
                # Check if it's a special method or main entry point
                is_special = self._is_special_item(item_name, item_type)
                
                if not is_used and not is_exported and not is_special:
                    confidence = 0.8 if item_type == 'function' else 0.6
                    
                    results.append(DeadCodeItem(
                        file_path=file_path,
                        item_type=item_type,
                        item_name=item_name,
                        line_number=item.get('line', 0),
                        reason=f"No references found to this {item_type}",
                        confidence=confidence,
                        risk_level=RiskLevel.LOW if item_type == 'variable' else RiskLevel.MEDIUM
                    ))
        
        return results
    
    def _build_definition_map(self, parsed_files: Dict) -> Dict[str, List[Dict]]:
        """Build map of defined items."""
        definitions = defaultdict(list)
        
        for file_path, data in parsed_files.items():
            for func in data.get('functions', []):
                definitions[file_path].append({
                    'name': func['name'],
                    'type': 'function',
                    'line': func.get('line', 0)
                })
            
            for cls in data.get('classes', []):
                definitions[file_path].append({
                    'name': cls['name'],
                    'type': 'class',
                    'line': cls.get('line', 0)
                })
        
        return definitions
    
    def _build_usage_map(self, parsed_files: Dict) -> Dict[str, Set[str]]:
        """Build map of used items."""
        usage = defaultdict(set)
        
        for file_path, data in parsed_files.items():
            # Track imports as usage
            for imp in data.get('imports', []):
                name = imp.get('name') or imp.get('module', '')
                if name:
                    usage[file_path].add(name)
        
        return usage
    
    def _is_item_used(self, item_name: str, file_path: str, used_items: Dict) -> bool:
        """Check if item is used anywhere."""
        for uses in used_items.values():
            if item_name in uses:
                return True
        return False
    
    def _is_exported(self, item_name: str, file_path: str, parsed_files: Dict) -> bool:
        """Check if item is exported."""
        data = parsed_files.get(file_path, {})
        exports = data.get('exports', [])
        return any(exp.get('name') == item_name for exp in exports)
    
    def _is_special_item(self, item_name: str, item_type: str) -> bool:
        """Check if item is a special method or entry point."""
        special_names = ['__init__', '__main__', 'main', 'setUp', 'tearDown', 'test_']
        return any(item_name.startswith(special) or item_name == special for special in special_names)


class CouplingAnalyzer:
    """Analyze module coupling and dependencies."""
    
    def analyze(self, parsed_files: Dict[str, Dict]) -> List[CouplingMetrics]:
        """
        Analyze coupling metrics for files.
        
        Args:
            parsed_files: Dictionary of parsed file data
            
        Returns:
            List of coupling metrics
        """
        results = []
        
        # Build dependency maps
        dependencies = self._build_dependency_map(parsed_files)
        dependents = self._build_dependent_map(dependencies)
        
        for file_path in parsed_files:
            deps = dependencies.get(file_path, set())
            depts = dependents.get(file_path, set())
            
            afferent = len(depts)  # Ca: incoming dependencies
            efferent = len(deps)   # Ce: outgoing dependencies
            
            # Calculate instability: I = Ce / (Ce + Ca)
            total = afferent + efferent
            instability = efferent / total if total > 0 else 0
            
            # Calculate coupling score (0-100, higher is worse)
            coupling_score = min((afferent + efferent) * 5, 100)
            
            # Determine risk level
            if coupling_score >= 80 or instability > 0.8:
                risk_level = RiskLevel.HIGH
            elif coupling_score >= 60 or instability > 0.6:
                risk_level = RiskLevel.MEDIUM
            else:
                risk_level = RiskLevel.LOW
            
            results.append(CouplingMetrics(
                file_path=file_path,
                afferent_coupling=afferent,
                efferent_coupling=efferent,
                instability=round(instability, 2),
                coupling_score=round(coupling_score, 1),
                risk_level=risk_level,
                dependencies=list(deps),
                dependents=list(depts)
            ))
        
        return results
    
    def _build_dependency_map(self, parsed_files: Dict) -> Dict[str, Set[str]]:
        """Build map of file dependencies."""
        dependencies = defaultdict(set)
        
        for file_path, data in parsed_files.items():
            for imp in data.get('imports', []):
                target = self._resolve_import(file_path, imp, parsed_files)
                if target:
                    dependencies[file_path].add(target)
        
        return dependencies
    
    def _build_dependent_map(self, dependencies: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
        """Build reverse dependency map."""
        dependents = defaultdict(set)
        
        for file_path, deps in dependencies.items():
            for dep in deps:
                dependents[dep].add(file_path)
        
        return dependents
    
    def _resolve_import(self, source_file: str, import_data: Dict, parsed_files: Dict) -> Optional[str]:
        """Resolve import to file path."""
        module = import_data.get('module') or import_data.get('source', '')
        
        if module.startswith('.'):
            source_dir = Path(source_file).parent
            level = len(module) - len(module.lstrip('.'))
            module_path = module.lstrip('.')
            
            target_dir = source_dir
            for _ in range(level - 1):
                target_dir = target_dir.parent
            
            for ext in ['.py', '.js', '.ts', '.tsx', '.jsx']:
                potential_path = str(target_dir / f"{module_path}{ext}")
                if potential_path in parsed_files:
                    return potential_path
        
        return None


class TestCoverageAnalyzer:
    """Analyze test coverage for source files."""
    
    def analyze(self, parsed_files: Dict[str, Dict], project_dir: str) -> List[TestCoverageReport]:
        """
        Analyze test coverage.
        
        Args:
            parsed_files: Dictionary of parsed file data
            project_dir: Project root directory
            
        Returns:
            List of test coverage reports
        """
        results = []
        
        # Identify test files
        test_files = self._identify_test_files(parsed_files)
        
        # Analyze each source file
        for file_path, data in parsed_files.items():
            if file_path in test_files:
                continue  # Skip test files themselves
            
            # Find associated test files
            associated_tests = self._find_test_files(file_path, test_files, project_dir)
            
            has_tests = len(associated_tests) > 0
            
            # Estimate coverage based on function count
            functions = data.get('functions', [])
            function_names = [f['name'] for f in functions]
            
            untested_functions = []
            if has_tests:
                # Check which functions are tested
                tested_functions = self._find_tested_functions(associated_tests, parsed_files)
                untested_functions = [f for f in function_names if f not in tested_functions]
            else:
                untested_functions = function_names
            
            coverage = 0 if not functions else ((len(functions) - len(untested_functions)) / len(functions)) * 100
            
            # Determine risk level
            if coverage == 0:
                risk_level = RiskLevel.HIGH
                recommendation = "No tests found. Create comprehensive test suite."
            elif coverage < 50:
                risk_level = RiskLevel.MEDIUM
                recommendation = f"Low coverage ({coverage:.0f}%). Add tests for {len(untested_functions)} functions."
            elif coverage < 80:
                risk_level = RiskLevel.LOW
                recommendation = f"Moderate coverage ({coverage:.0f}%). Consider adding more tests."
            else:
                risk_level = RiskLevel.INFO
                recommendation = f"Good coverage ({coverage:.0f}%). Maintain test quality."
            
            results.append(TestCoverageReport(
                file_path=file_path,
                has_tests=has_tests,
                test_files=associated_tests,
                coverage_estimate=round(coverage, 1),
                untested_functions=untested_functions,
                risk_level=risk_level,
                recommendation=recommendation
            ))
        
        return results
    
    def _identify_test_files(self, parsed_files: Dict) -> Set[str]:
        """Identify test files."""
        test_files = set()
        
        for file_path in parsed_files:
            path = Path(file_path)
            name = path.name.lower()
            
            if any([
                name.startswith('test_'),
                name.endswith('_test.py'),
                name.endswith('.test.js'),
                name.endswith('.test.ts'),
                name.endswith('.spec.js'),
                name.endswith('.spec.ts'),
                'test' in path.parts
            ]):
                test_files.add(file_path)
        
        return test_files
    
    def _find_test_files(self, source_file: str, test_files: Set[str], project_dir: str) -> List[str]:
        """Find test files for a source file."""
        source_path = Path(source_file)
        source_name = source_path.stem
        
        associated = []
        for test_file in test_files:
            test_path = Path(test_file)
            test_name = test_path.stem
            
            # Check if test file name matches source file
            if source_name in test_name or test_name.replace('test_', '') == source_name:
                associated.append(test_file)
        
        return associated
    
    def _find_tested_functions(self, test_files: List[str], parsed_files: Dict) -> Set[str]:
        """Find which functions are tested."""
        tested = set()
        
        for test_file in test_files:
            data = parsed_files.get(test_file, {})
            # Look for test function names that might reference source functions
            for func in data.get('functions', []):
                func_name = func['name']
                if func_name.startswith('test_'):
                    # Extract potential source function name
                    source_func = func_name.replace('test_', '')
                    tested.add(source_func)
        
        return tested


class RiskyFilesDetector:
    """Detect files with high risk factors."""
    
    def detect(self, parsed_files: Dict[str, Dict], project_dir: str) -> List[RiskyFile]:
        """
        Detect risky files.
        
        Args:
            parsed_files: Dictionary of parsed file data
            project_dir: Project root directory
            
        Returns:
            List of risky files
        """
        results = []
        
        for file_path, data in parsed_files.items():
            risk_factors = []
            risk_score = 0
            
            # Check file size
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 50000:  # > 50KB
                    risk_factors.append("Large file size")
                    risk_score += 20
            except:
                file_size = 0
            
            # Count lines of code
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                
                if lines > 500:
                    risk_factors.append(f"High line count ({lines} lines)")
                    risk_score += 25
            except:
                lines = 0
            
            # Check complexity indicators
            functions = data.get('functions', [])
            classes = data.get('classes', [])
            
            if len(functions) > 20:
                risk_factors.append(f"Many functions ({len(functions)})")
                risk_score += 15
            
            if len(classes) > 10:
                risk_factors.append(f"Many classes ({len(classes)})")
                risk_score += 15
            
            # Check imports
            imports = data.get('imports', [])
            if len(imports) > 30:
                risk_factors.append(f"Many imports ({len(imports)})")
                risk_score += 10
            
            # Calculate complexity score
            complexity_score = min((len(functions) + len(classes) * 2 + len(imports)) / 2, 100)
            
            if complexity_score > 50:
                risk_factors.append(f"High complexity score ({complexity_score:.0f})")
                risk_score += 20
            
            # Only include if there are risk factors
            if risk_factors:
                # Determine risk level
                if risk_score >= 70:
                    risk_level = RiskLevel.CRITICAL
                elif risk_score >= 50:
                    risk_level = RiskLevel.HIGH
                elif risk_score >= 30:
                    risk_level = RiskLevel.MEDIUM
                else:
                    risk_level = RiskLevel.LOW
                
                results.append(RiskyFile(
                    file_path=file_path,
                    risk_factors=risk_factors,
                    risk_score=min(risk_score, 100),
                    risk_level=risk_level,
                    file_size=file_size,
                    lines_of_code=lines,
                    complexity_score=round(complexity_score, 1),
                    change_frequency=None,
                    last_modified=None
                ))
        
        # Sort by risk score
        results.sort(key=lambda x: x.risk_score, reverse=True)
        
        return results


class ComplexityAnalyzer:
    """Analyze code complexity metrics."""
    
    def analyze(self, parsed_files: Dict[str, Dict]) -> List[ComplexityMetrics]:
        """
        Analyze complexity metrics.
        
        Args:
            parsed_files: Dictionary of parsed file data
            
        Returns:
            List of complexity metrics
        """
        results = []
        
        for file_path, data in parsed_files.items():
            # Calculate metrics
            functions = data.get('functions', [])
            classes = data.get('classes', [])
            
            # Estimate cyclomatic complexity
            cyclomatic = self._estimate_cyclomatic_complexity(file_path, functions)
            
            # Estimate cognitive complexity
            cognitive = self._estimate_cognitive_complexity(file_path)
            
            # Calculate max nesting depth
            max_nesting = self._estimate_max_nesting(file_path)
            
            # Count lines of code
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = len([l for l in f if l.strip() and not l.strip().startswith('#')])
            except:
                lines = 0
            
            # Find complex functions
            complex_functions = []
            for func in functions:
                func_complexity = len(func.get('args', [])) * 2 + len(func.get('decorators', []))
                if func_complexity > 10:
                    complex_functions.append({
                        'name': func['name'],
                        'line': func.get('line', 0),
                        'complexity': func_complexity,
                        'args_count': len(func.get('args', []))
                    })
            
            # Calculate maintainability index (simplified)
            # MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(LOC)
            # Simplified version
            maintainability = max(0, 100 - (cyclomatic * 2) - (lines / 10))
            
            # Determine risk level
            if cyclomatic > 50 or cognitive > 50 or maintainability < 40:
                risk_level = RiskLevel.CRITICAL
            elif cyclomatic > 30 or cognitive > 30 or maintainability < 60:
                risk_level = RiskLevel.HIGH
            elif cyclomatic > 15 or cognitive > 15 or maintainability < 75:
                risk_level = RiskLevel.MEDIUM
            else:
                risk_level = RiskLevel.LOW
            
            results.append(ComplexityMetrics(
                file_path=file_path,
                cyclomatic_complexity=cyclomatic,
                cognitive_complexity=cognitive,
                max_nesting_depth=max_nesting,
                function_count=len(functions),
                class_count=len(classes),
                lines_of_code=lines,
                complex_functions=complex_functions,
                risk_level=risk_level,
                maintainability_index=round(maintainability, 1)
            ))
        
        return results
    
    def _estimate_cyclomatic_complexity(self, file_path: str, functions: List[Dict]) -> int:
        """Estimate cyclomatic complexity."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count decision points
            decision_keywords = ['if', 'elif', 'else', 'for', 'while', 'and', 'or', 'case', 'catch']
            complexity = 1  # Base complexity
            
            for keyword in decision_keywords:
                complexity += content.count(f' {keyword} ')
                complexity += content.count(f' {keyword}(')
            
            return complexity
        except:
            return len(functions) * 2  # Rough estimate
    
    def _estimate_cognitive_complexity(self, file_path: str) -> int:
        """Estimate cognitive complexity."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count nesting and control flow
            complexity = 0
            nesting_level = 0
            
            for line in content.split('\n'):
                stripped = line.strip()
                
                # Increase nesting
                if any(stripped.startswith(kw) for kw in ['if', 'for', 'while', 'def', 'class']):
                    nesting_level += 1
                    complexity += nesting_level
                
                # Decrease nesting
                if stripped and not stripped.startswith('#'):
                    indent = len(line) - len(line.lstrip())
                    if indent == 0:
                        nesting_level = 0
            
            return complexity
        except:
            return 0
    
    def _estimate_max_nesting(self, file_path: str) -> int:
        """Estimate maximum nesting depth."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            max_depth = 0
            current_depth = 0
            
            for line in content.split('\n'):
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                
                indent = len(line) - len(line.lstrip())
                current_depth = indent // 4  # Assuming 4-space indentation
                max_depth = max(max_depth, current_depth)
            
            return max_depth
        except:
            return 0

# Made with Bob
