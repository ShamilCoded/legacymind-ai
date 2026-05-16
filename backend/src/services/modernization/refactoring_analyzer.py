"""
Refactoring analyzer for code quality and technical debt assessment.
"""
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict

from .models import (
    RefactoringRecommendation,
    CodeSmell,
    DesignPatternRecommendation,
    ModernizationPriority
)

logger = logging.getLogger(__name__)


class RefactoringAnalyzer:
    """Analyzes code for refactoring opportunities and technical debt."""
    
    # Code smell thresholds
    MAX_METHOD_LINES = 50
    MAX_CLASS_LINES = 300
    MAX_PARAMETERS = 5
    MAX_COMPLEXITY = 10
    
    # Design patterns to recommend
    DESIGN_PATTERNS = {
        'singleton': {
            'indicator': 'global state',
            'benefit': 'Ensure single instance and global access point'
        },
        'factory': {
            'indicator': 'object creation',
            'benefit': 'Encapsulate object creation logic'
        },
        'strategy': {
            'indicator': 'conditional logic',
            'benefit': 'Replace conditional with polymorphism'
        },
        'observer': {
            'indicator': 'event handling',
            'benefit': 'Decouple event producers from consumers'
        },
        'decorator': {
            'indicator': 'extending functionality',
            'benefit': 'Add responsibilities dynamically'
        }
    }
    
    def __init__(self):
        """Initialize refactoring analyzer."""
        self.file_patterns = ['*.py', '*.js', '*.ts', '*.java', '*.go']
    
    def analyze(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> RefactoringRecommendation:
        """
        Analyze code for refactoring opportunities.
        
        Args:
            directory: Directory to analyze
            file_patterns: File patterns to include
            exclude_patterns: Patterns to exclude
            
        Returns:
            Refactoring recommendations
        """
        logger.info(f"Analyzing {directory} for refactoring opportunities")
        
        dir_path = Path(directory)
        patterns = file_patterns or self.file_patterns
        
        # Collect files
        files = self._collect_files(dir_path, patterns, exclude_patterns)
        
        # Analyze each file
        code_smells = []
        duplicate_blocks = 0
        long_methods = 0
        large_classes = 0
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Detect code smells
                smells = self._detect_code_smells(file_path, content)
                code_smells.extend(smells)
                
                # Count metrics
                long_methods += self._count_long_methods(content, file_path.suffix)
                large_classes += self._count_large_classes(content, file_path.suffix)
                
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
        
        # Detect duplicate code
        duplicate_blocks = self._detect_duplicate_code(files)
        
        # Recommend design patterns
        design_patterns = self._recommend_design_patterns(files, code_smells)
        
        # Calculate technical debt score
        tech_debt_score = self._calculate_technical_debt(
            len(code_smells),
            duplicate_blocks,
            long_methods,
            large_classes,
            len(files)
        )
        
        # Calculate maintainability index
        maintainability = self._calculate_maintainability_index(
            tech_debt_score,
            len(code_smells),
            len(files)
        )
        
        # Identify priority refactorings
        priority_refactorings = self._identify_priority_refactorings(
            code_smells,
            design_patterns
        )
        
        # Calculate total effort
        total_effort = sum(smell.estimated_effort_hours for smell in code_smells)
        total_effort += sum(pattern.estimated_effort_hours for pattern in design_patterns)
        
        return RefactoringRecommendation(
            code_smells=code_smells,
            design_patterns=design_patterns,
            duplicate_code_blocks=duplicate_blocks,
            long_methods=long_methods,
            large_classes=large_classes,
            technical_debt_score=tech_debt_score,
            maintainability_index=maintainability,
            priority_refactorings=priority_refactorings,
            total_refactoring_effort_hours=total_effort
        )
    
    def _collect_files(
        self,
        directory: Path,
        patterns: List[str],
        exclude_patterns: Optional[List[str]]
    ) -> List[Path]:
        """Collect files matching patterns."""
        files = []
        exclude = exclude_patterns or []
        
        for pattern in patterns:
            for file_path in directory.rglob(pattern):
                if any(re.search(ex, str(file_path)) for ex in exclude):
                    continue
                if file_path.is_file():
                    files.append(file_path)
        
        return files
    
    def _detect_code_smells(self, file_path: Path, content: str) -> List[CodeSmell]:
        """Detect code smells in a file."""
        smells = []
        lines = content.split('\n')
        
        # Detect long methods
        methods = self._extract_methods(content, file_path.suffix)
        for method_name, start_line, end_line in methods:
            method_length = end_line - start_line
            if method_length > self.MAX_METHOD_LINES:
                smells.append(CodeSmell(
                    type="Long Method",
                    file_path=str(file_path),
                    line_number=start_line,
                    severity=ModernizationPriority.MEDIUM,
                    description=f"Method '{method_name}' has {method_length} lines (max: {self.MAX_METHOD_LINES})",
                    recommendation="Break down into smaller, focused methods",
                    estimated_effort_hours=2.0
                ))
        
        # Detect large classes
        classes = self._extract_classes_with_lines(content, file_path.suffix)
        for class_name, start_line, end_line in classes:
            class_length = end_line - start_line
            if class_length > self.MAX_CLASS_LINES:
                smells.append(CodeSmell(
                    type="Large Class",
                    file_path=str(file_path),
                    line_number=start_line,
                    severity=ModernizationPriority.MEDIUM,
                    description=f"Class '{class_name}' has {class_length} lines (max: {self.MAX_CLASS_LINES})",
                    recommendation="Split into smaller, cohesive classes",
                    estimated_effort_hours=4.0
                ))
        
        # Detect long parameter lists
        for i, line in enumerate(lines, 1):
            params = self._count_parameters(line)
            if params > self.MAX_PARAMETERS:
                smells.append(CodeSmell(
                    type="Long Parameter List",
                    file_path=str(file_path),
                    line_number=i,
                    severity=ModernizationPriority.LOW,
                    description=f"Function has {params} parameters (max: {self.MAX_PARAMETERS})",
                    recommendation="Use parameter object or builder pattern",
                    estimated_effort_hours=1.0
                ))
        
        # Detect duplicate code patterns
        if self._has_duplicate_patterns(content):
            smells.append(CodeSmell(
                type="Duplicate Code",
                file_path=str(file_path),
                line_number=0,
                severity=ModernizationPriority.MEDIUM,
                description="File contains duplicate code patterns",
                recommendation="Extract common code into reusable functions",
                estimated_effort_hours=2.0
            ))
        
        # Detect magic numbers
        magic_numbers = self._find_magic_numbers(content)
        if magic_numbers:
            smells.append(CodeSmell(
                type="Magic Numbers",
                file_path=str(file_path),
                line_number=0,
                severity=ModernizationPriority.LOW,
                description=f"Found {len(magic_numbers)} magic numbers",
                recommendation="Replace with named constants",
                estimated_effort_hours=0.5
            ))
        
        # Detect commented code
        commented_lines = self._count_commented_code(lines)
        if commented_lines > 10:
            smells.append(CodeSmell(
                type="Commented Code",
                file_path=str(file_path),
                line_number=0,
                severity=ModernizationPriority.LOW,
                description=f"Found {commented_lines} lines of commented code",
                recommendation="Remove commented code and use version control",
                estimated_effort_hours=0.5
            ))
        
        return smells
    
    def _extract_methods(self, content: str, suffix: str) -> List[tuple]:
        """Extract method definitions with line numbers."""
        methods = []
        lines = content.split('\n')
        
        if suffix == '.py':
            current_method = None
            indent_level = 0
            
            for i, line in enumerate(lines, 1):
                if re.match(r'\s*def\s+(\w+)', line):
                    if current_method:
                        methods.append((current_method[0], current_method[1], i - 1))
                    match = re.match(r'\s*def\s+(\w+)', line)
                    current_method = (match.group(1), i)
                    indent_level = len(line) - len(line.lstrip())
                elif current_method and line.strip() and not line.startswith(' ' * (indent_level + 1)):
                    methods.append((current_method[0], current_method[1], i - 1))
                    current_method = None
            
            if current_method:
                methods.append((current_method[0], current_method[1], len(lines)))
        
        elif suffix in ['.js', '.ts']:
            for match in re.finditer(r'function\s+(\w+)|(\w+)\s*=\s*(?:async\s+)?(?:function|\()', content):
                name = match.group(1) or match.group(2)
                line_num = content[:match.start()].count('\n') + 1
                # Estimate end (simplified)
                methods.append((name, line_num, line_num + 20))
        
        return methods
    
    def _extract_classes_with_lines(self, content: str, suffix: str) -> List[tuple]:
        """Extract class definitions with line numbers."""
        classes = []
        lines = content.split('\n')
        
        if suffix == '.py':
            current_class = None
            indent_level = 0
            
            for i, line in enumerate(lines, 1):
                if re.match(r'\s*class\s+(\w+)', line):
                    if current_class:
                        classes.append((current_class[0], current_class[1], i - 1))
                    match = re.match(r'\s*class\s+(\w+)', line)
                    current_class = (match.group(1), i)
                    indent_level = len(line) - len(line.lstrip())
                elif current_class and line.strip() and not line.startswith(' ' * indent_level) and not line.strip().startswith('#'):
                    classes.append((current_class[0], current_class[1], i - 1))
                    current_class = None
            
            if current_class:
                classes.append((current_class[0], current_class[1], len(lines)))
        
        return classes
    
    def _count_parameters(self, line: str) -> int:
        """Count parameters in a function definition."""
        match = re.search(r'def\s+\w+\((.*?)\)|function\s+\w+\((.*?)\)', line)
        if match:
            params = match.group(1) or match.group(2)
            if params:
                return len([p.strip() for p in params.split(',') if p.strip()])
        return 0
    
    def _has_duplicate_patterns(self, content: str) -> bool:
        """Check for duplicate code patterns."""
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        
        # Simple check: look for repeated sequences of 3+ lines
        for i in range(len(lines) - 3):
            pattern = tuple(lines[i:i+3])
            for j in range(i + 3, len(lines) - 3):
                if tuple(lines[j:j+3]) == pattern:
                    return True
        
        return False
    
    def _find_magic_numbers(self, content: str) -> List[int]:
        """Find magic numbers in code."""
        # Find numeric literals (excluding 0, 1, -1)
        numbers = re.findall(r'\b(\d+)\b', content)
        magic = [int(n) for n in numbers if int(n) not in [0, 1, -1] and int(n) < 1000]
        return magic
    
    def _count_commented_code(self, lines: List[str]) -> int:
        """Count lines of commented code."""
        count = 0
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                # Check if it looks like code (has operators, keywords, etc.)
                if any(op in stripped for op in ['=', '(', ')', '{', '}', 'def', 'class', 'function']):
                    count += 1
        return count
    
    def _count_long_methods(self, content: str, suffix: str) -> int:
        """Count long methods."""
        methods = self._extract_methods(content, suffix)
        return sum(1 for _, start, end in methods if end - start > self.MAX_METHOD_LINES)
    
    def _count_large_classes(self, content: str, suffix: str) -> int:
        """Count large classes."""
        classes = self._extract_classes_with_lines(content, suffix)
        return sum(1 for _, start, end in classes if end - start > self.MAX_CLASS_LINES)
    
    def _detect_duplicate_code(self, files: List[Path]) -> int:
        """Detect duplicate code blocks across files."""
        # Simplified: count files with similar names
        file_names = [f.stem for f in files]
        duplicates = len(file_names) - len(set(file_names))
        return max(0, duplicates)
    
    def _recommend_design_patterns(
        self,
        files: List[Path],
        code_smells: List[CodeSmell]
    ) -> List[DesignPatternRecommendation]:
        """Recommend design patterns."""
        patterns = []
        
        # Recommend Factory pattern for object creation
        creation_files = [f for f in files if 'factory' not in str(f).lower() and 
                         any(keyword in str(f).lower() for keyword in ['create', 'build', 'new'])]
        if creation_files:
            patterns.append(DesignPatternRecommendation(
                pattern_name="Factory Pattern",
                applicable_to=[str(f) for f in creation_files[:3]],
                current_approach="Direct object instantiation scattered across codebase",
                recommended_approach="Centralize object creation in factory classes",
                benefits=[
                    "Encapsulate object creation logic",
                    "Easy to add new types",
                    "Reduce coupling"
                ],
                implementation_guide="Create factory classes that handle object instantiation based on parameters",
                estimated_effort_hours=8.0
            ))
        
        # Recommend Strategy pattern for conditional logic
        if any(smell.type == "Long Method" for smell in code_smells):
            patterns.append(DesignPatternRecommendation(
                pattern_name="Strategy Pattern",
                applicable_to=["Files with complex conditional logic"],
                current_approach="Large if-else or switch statements",
                recommended_approach="Extract each branch into separate strategy classes",
                benefits=[
                    "Replace conditional with polymorphism",
                    "Easy to add new strategies",
                    "Improved testability"
                ],
                implementation_guide="Define strategy interface and implement concrete strategies for each case",
                estimated_effort_hours=6.0
            ))
        
        # Recommend Repository pattern for data access
        data_files = [f for f in files if any(keyword in str(f).lower() 
                     for keyword in ['model', 'entity', 'database', 'dao'])]
        if data_files and not any('repository' in str(f).lower() for f in files):
            patterns.append(DesignPatternRecommendation(
                pattern_name="Repository Pattern",
                applicable_to=[str(f) for f in data_files[:3]],
                current_approach="Direct database access from business logic",
                recommended_approach="Introduce repository layer for data access",
                benefits=[
                    "Separate data access from business logic",
                    "Easy to switch data sources",
                    "Improved testability with mocks"
                ],
                implementation_guide="Create repository interfaces and implementations for each entity",
                estimated_effort_hours=12.0
            ))
        
        return patterns
    
    def _calculate_technical_debt(
        self,
        smell_count: int,
        duplicate_blocks: int,
        long_methods: int,
        large_classes: int,
        file_count: int
    ) -> float:
        """Calculate technical debt score (0-100)."""
        if file_count == 0:
            return 0.0
        
        # Normalize metrics
        smell_ratio = (smell_count / file_count) * 10
        duplicate_ratio = (duplicate_blocks / max(file_count, 1)) * 20
        method_ratio = (long_methods / max(file_count, 1)) * 15
        class_ratio = (large_classes / max(file_count, 1)) * 15
        
        debt = smell_ratio + duplicate_ratio + method_ratio + class_ratio
        return min(100.0, round(debt, 1))
    
    def _calculate_maintainability_index(
        self,
        tech_debt_score: float,
        smell_count: int,
        file_count: int
    ) -> float:
        """Calculate maintainability index (0-100)."""
        # Higher is better
        base_score = 100.0
        
        # Deduct for technical debt
        base_score -= tech_debt_score * 0.5
        
        # Deduct for code smells
        smell_penalty = (smell_count / max(file_count, 1)) * 20
        base_score -= smell_penalty
        
        return max(0.0, min(100.0, round(base_score, 1)))
    
    def _identify_priority_refactorings(
        self,
        code_smells: List[CodeSmell],
        design_patterns: List[DesignPatternRecommendation]
    ) -> List[str]:
        """Identify priority refactoring tasks."""
        priorities = []
        
        # Critical and high severity smells
        critical_smells = [s for s in code_smells if s.severity == ModernizationPriority.CRITICAL]
        high_smells = [s for s in code_smells if s.severity == ModernizationPriority.HIGH]
        
        if critical_smells:
            priorities.append(f"Fix {len(critical_smells)} critical code smells")
        
        if high_smells:
            priorities.append(f"Address {len(high_smells)} high-priority code smells")
        
        # Large classes and long methods
        large_classes = [s for s in code_smells if s.type == "Large Class"]
        if large_classes:
            priorities.append(f"Refactor {len(large_classes)} large classes")
        
        long_methods = [s for s in code_smells if s.type == "Long Method"]
        if long_methods:
            priorities.append(f"Break down {len(long_methods)} long methods")
        
        # Design patterns
        for pattern in design_patterns[:2]:
            priorities.append(f"Implement {pattern.pattern_name}")
        
        return priorities[:5]


# Made with Bob