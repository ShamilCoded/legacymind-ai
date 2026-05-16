"""
Main risk analyzer orchestrator.
"""
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from ..architecture.dependency_parser import DependencyParser
from .detectors import (
    CircularDependencyDetector,
    DeadCodeDetector,
    CouplingAnalyzer,
    TestCoverageAnalyzer,
    RiskyFilesDetector,
    ComplexityAnalyzer
)
from .risk_scorer import RiskScorer
from .models import RiskAnalysisResult

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """Main risk analysis orchestrator."""
    
    def __init__(self):
        self.parser = DependencyParser()
        self.circular_detector = CircularDependencyDetector()
        self.dead_code_detector = DeadCodeDetector()
        self.coupling_analyzer = CouplingAnalyzer()
        self.test_coverage_analyzer = TestCoverageAnalyzer()
        self.risky_files_detector = RiskyFilesDetector()
        self.complexity_analyzer = ComplexityAnalyzer()
        self.risk_scorer = RiskScorer()
    
    def analyze(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        include_tests: bool = True,
        include_complexity: bool = True,
        include_dependencies: bool = True
    ) -> RiskAnalysisResult:
        """
        Perform comprehensive risk analysis on a directory.
        
        Args:
            directory: Directory path to analyze
            file_patterns: File patterns to include
            exclude_patterns: Patterns to exclude
            include_tests: Include test coverage analysis
            include_complexity: Include complexity analysis
            include_dependencies: Include dependency analysis
            
        Returns:
            Complete risk analysis result
        """
        logger.info(f"Starting risk analysis for: {directory}")
        
        # Parse all files
        logger.info("Parsing files...")
        parsed_files = self.parser.parse_directory(directory, file_patterns)
        
        if not parsed_files:
            logger.warning("No files found to analyze")
            return self._empty_result(directory)
        
        logger.info(f"Parsed {len(parsed_files)} files")
        
        # Run detectors
        circular_deps = []
        dead_code = []
        coupling = []
        
        if include_dependencies:
            logger.info("Detecting circular dependencies...")
            circular_deps = self.circular_detector.detect(parsed_files)
            logger.info(f"Found {len(circular_deps)} circular dependencies")
            
            logger.info("Analyzing coupling...")
            coupling = self.coupling_analyzer.analyze(parsed_files)
            logger.info(f"Analyzed coupling for {len(coupling)} files")
        
        logger.info("Detecting dead code...")
        dead_code = self.dead_code_detector.detect(parsed_files)
        logger.info(f"Found {len(dead_code)} potential dead code items")
        
        test_coverage = []
        if include_tests:
            logger.info("Analyzing test coverage...")
            test_coverage = self.test_coverage_analyzer.analyze(parsed_files, directory)
            logger.info(f"Analyzed test coverage for {len(test_coverage)} files")
        
        logger.info("Detecting risky files...")
        risky_files = self.risky_files_detector.detect(parsed_files, directory)
        logger.info(f"Found {len(risky_files)} risky files")
        
        complexity = []
        if include_complexity:
            logger.info("Analyzing complexity...")
            complexity = self.complexity_analyzer.analyze(parsed_files)
            logger.info(f"Analyzed complexity for {len(complexity)} files")
        
        # Calculate overall risk score
        logger.info("Calculating risk scores...")
        overall_risk_score = self.risk_scorer.calculate_overall_score(
            circular_deps,
            dead_code,
            coupling,
            test_coverage,
            risky_files,
            complexity
        )
        
        # Generate summary
        summary = self._generate_summary(
            parsed_files,
            circular_deps,
            dead_code,
            coupling,
            test_coverage,
            risky_files,
            complexity,
            overall_risk_score
        )
        
        logger.info("Risk analysis complete")
        
        return RiskAnalysisResult(
            project_path=directory,
            analysis_timestamp=datetime.now().isoformat(),
            overall_risk_score=overall_risk_score,
            circular_dependencies=circular_deps,
            dead_code=dead_code,
            coupling_metrics=coupling,
            test_coverage=test_coverage,
            risky_files=risky_files,
            complexity_metrics=complexity,
            summary=summary,
            metadata={
                'files_analyzed': len(parsed_files),
                'file_patterns': file_patterns,
                'exclude_patterns': exclude_patterns
            }
        )
    
    def analyze_file(self, file_path: str) -> Dict:
        """
        Analyze a single file.
        
        Args:
            file_path: Path to file
            
        Returns:
            Risk analysis for the file
        """
        # Parse single file
        if file_path.endswith('.py'):
            parsed = self.parser.parse_python_file(file_path)
        elif file_path.endswith(('.js', '.ts', '.tsx', '.jsx')):
            parsed = self.parser.parse_javascript_file(file_path)
        else:
            return {'error': 'Unsupported file type'}
        
        parsed_files = {file_path: parsed}
        
        # Run analyzers
        complexity = self.complexity_analyzer.analyze(parsed_files)
        risky_files = self.risky_files_detector.detect(parsed_files, str(Path(file_path).parent))
        
        return {
            'file_path': file_path,
            'complexity': complexity[0].dict() if complexity else None,
            'risk_assessment': risky_files[0].dict() if risky_files else None,
            'functions': len(parsed.get('functions', [])),
            'classes': len(parsed.get('classes', [])),
            'imports': len(parsed.get('imports', []))
        }
    
    def _empty_result(self, directory: str) -> RiskAnalysisResult:
        """Create empty result when no files found."""
        from .models import RiskScore, RiskLevel
        
        return RiskAnalysisResult(
            project_path=directory,
            analysis_timestamp=datetime.now().isoformat(),
            overall_risk_score=RiskScore(
                overall_score=0,
                risk_level=RiskLevel.INFO,
                category_scores={},
                critical_issues=0,
                high_issues=0,
                medium_issues=0,
                low_issues=0,
                recommendations=["No files found to analyze"]
            ),
            circular_dependencies=[],
            dead_code=[],
            coupling_metrics=[],
            test_coverage=[],
            risky_files=[],
            complexity_metrics=[],
            summary={'files_analyzed': 0},
            metadata={}
        )
    
    def _generate_summary(
        self,
        parsed_files: Dict,
        circular_deps: List,
        dead_code: List,
        coupling: List,
        test_coverage: List,
        risky_files: List,
        complexity: List,
        overall_risk_score
    ) -> Dict:
        """Generate analysis summary."""
        # Count file types
        file_types = {}
        for file_path in parsed_files:
            ext = Path(file_path).suffix
            file_types[ext] = file_types.get(ext, 0) + 1
        
        # Calculate averages
        avg_coupling = sum(c.coupling_score for c in coupling) / len(coupling) if coupling else 0
        avg_complexity = sum(c.cyclomatic_complexity for c in complexity) / len(complexity) if complexity else 0
        avg_coverage = sum(tc.coverage_estimate for tc in test_coverage) / len(test_coverage) if test_coverage else 0
        
        # Top issues
        top_risky_files = sorted(risky_files, key=lambda x: x.risk_score, reverse=True)[:5]
        top_complex_files = sorted(complexity, key=lambda x: x.cyclomatic_complexity, reverse=True)[:5]
        
        return {
            'files_analyzed': len(parsed_files),
            'file_types': file_types,
            'total_issues': (
                len(circular_deps) +
                len(dead_code) +
                overall_risk_score.critical_issues +
                overall_risk_score.high_issues
            ),
            'circular_dependencies_count': len(circular_deps),
            'dead_code_count': len(dead_code),
            'average_coupling': round(avg_coupling, 1),
            'average_complexity': round(avg_complexity, 1),
            'average_test_coverage': round(avg_coverage, 1),
            'files_without_tests': sum(1 for tc in test_coverage if not tc.has_tests),
            'top_risky_files': [
                {
                    'path': rf.file_path,
                    'score': rf.risk_score,
                    'factors': rf.risk_factors
                }
                for rf in top_risky_files
            ],
            'top_complex_files': [
                {
                    'path': cf.file_path,
                    'complexity': cf.cyclomatic_complexity,
                    'maintainability': cf.maintainability_index
                }
                for cf in top_complex_files
            ],
            'risk_distribution': {
                'critical': overall_risk_score.critical_issues,
                'high': overall_risk_score.high_issues,
                'medium': overall_risk_score.medium_issues,
                'low': overall_risk_score.low_issues
            }
        }
    
    def generate_visualization_data(self, result: RiskAnalysisResult) -> Dict:
        """
        Generate data for frontend visualization.
        
        Args:
            result: Risk analysis result
            
        Returns:
            Visualization data
        """
        # Risk heatmap data
        risk_heatmap = {
            'files': [
                {
                    'path': rf.file_path,
                    'score': rf.risk_score,
                    'level': rf.risk_level.value
                }
                for rf in result.risky_files
            ]
        }
        
        # Complexity distribution
        complexity_distribution = {
            'low': sum(1 for c in result.complexity_metrics if c.cyclomatic_complexity < 10),
            'medium': sum(1 for c in result.complexity_metrics if 10 <= c.cyclomatic_complexity < 20),
            'high': sum(1 for c in result.complexity_metrics if 20 <= c.cyclomatic_complexity < 30),
            'very_high': sum(1 for c in result.complexity_metrics if c.cyclomatic_complexity >= 30)
        }
        
        # Top risks
        top_risks = []
        
        # Add circular dependencies
        for cd in result.circular_dependencies[:3]:
            top_risks.append({
                'type': 'circular_dependency',
                'severity': cd.risk_level.value,
                'description': cd.description,
                'impact': cd.impact_score
            })
        
        # Add risky files
        for rf in sorted(result.risky_files, key=lambda x: x.risk_score, reverse=True)[:5]:
            top_risks.append({
                'type': 'risky_file',
                'severity': rf.risk_level.value,
                'description': f"High-risk file: {Path(rf.file_path).name}",
                'impact': rf.risk_score,
                'file': rf.file_path
            })
        
        # Sort by impact
        top_risks.sort(key=lambda x: x['impact'], reverse=True)
        
        return {
            'risk_heatmap': risk_heatmap,
            'complexity_distribution': complexity_distribution,
            'top_risks': top_risks[:10],
            'category_scores': result.overall_risk_score.category_scores,
            'risk_trends': {
                'current_score': result.overall_risk_score.overall_score,
                'risk_level': result.overall_risk_score.risk_level.value
            }
        }

# Made with Bob
