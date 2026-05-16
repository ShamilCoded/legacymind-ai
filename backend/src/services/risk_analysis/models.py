"""
Data models for risk analysis results.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum


class RiskLevel(str, Enum):
    """Risk severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class CircularDependency(BaseModel):
    """Circular dependency detection result."""
    cycle: List[str] = Field(..., description="List of files in the circular dependency")
    cycle_length: int = Field(..., description="Number of files in the cycle")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    impact_score: float = Field(..., description="Impact score (0-100)")
    description: str = Field(..., description="Human-readable description")


class DeadCodeItem(BaseModel):
    """Dead code detection result."""
    file_path: str = Field(..., description="Path to file containing dead code")
    item_type: str = Field(..., description="Type of dead code (function, class, variable)")
    item_name: str = Field(..., description="Name of the dead code item")
    line_number: int = Field(..., description="Line number where item is defined")
    reason: str = Field(..., description="Reason why it's considered dead code")
    confidence: float = Field(..., description="Confidence score (0-1)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")


class CouplingMetrics(BaseModel):
    """Coupling analysis metrics."""
    file_path: str = Field(..., description="Path to analyzed file")
    afferent_coupling: int = Field(..., description="Number of files that depend on this file")
    efferent_coupling: int = Field(..., description="Number of files this file depends on")
    instability: float = Field(..., description="Instability metric (0-1)")
    coupling_score: float = Field(..., description="Overall coupling score (0-100)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    dependencies: List[str] = Field(default_factory=list, description="List of dependencies")
    dependents: List[str] = Field(default_factory=list, description="List of dependents")


class TestCoverageReport(BaseModel):
    """Test coverage analysis report."""
    file_path: str = Field(..., description="Path to source file")
    has_tests: bool = Field(..., description="Whether tests exist for this file")
    test_files: List[str] = Field(default_factory=list, description="Associated test files")
    coverage_estimate: float = Field(..., description="Estimated coverage percentage (0-100)")
    untested_functions: List[str] = Field(default_factory=list, description="Functions without tests")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    recommendation: str = Field(..., description="Testing recommendation")


class RiskyFile(BaseModel):
    """Risky file detection result."""
    file_path: str = Field(..., description="Path to risky file")
    risk_factors: List[str] = Field(..., description="List of risk factors")
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    file_size: int = Field(..., description="File size in bytes")
    lines_of_code: int = Field(..., description="Number of lines of code")
    complexity_score: float = Field(..., description="Complexity score")
    change_frequency: Optional[int] = Field(None, description="Number of recent changes")
    last_modified: Optional[str] = Field(None, description="Last modification date")


class ComplexityMetrics(BaseModel):
    """Code complexity metrics."""
    file_path: str = Field(..., description="Path to analyzed file")
    cyclomatic_complexity: int = Field(..., description="Cyclomatic complexity")
    cognitive_complexity: int = Field(..., description="Cognitive complexity")
    max_nesting_depth: int = Field(..., description="Maximum nesting depth")
    function_count: int = Field(..., description="Number of functions")
    class_count: int = Field(..., description="Number of classes")
    lines_of_code: int = Field(..., description="Lines of code")
    complex_functions: List[Dict[str, Any]] = Field(default_factory=list, description="Complex functions")
    risk_level: RiskLevel = Field(..., description="Risk severity level")
    maintainability_index: float = Field(..., description="Maintainability index (0-100)")


class RiskScore(BaseModel):
    """Overall risk score for a file or project."""
    overall_score: float = Field(..., description="Overall risk score (0-100)")
    risk_level: RiskLevel = Field(..., description="Overall risk level")
    category_scores: Dict[str, float] = Field(..., description="Scores by category")
    critical_issues: int = Field(..., description="Number of critical issues")
    high_issues: int = Field(..., description="Number of high severity issues")
    medium_issues: int = Field(..., description="Number of medium severity issues")
    low_issues: int = Field(..., description="Number of low severity issues")
    recommendations: List[str] = Field(default_factory=list, description="Prioritized recommendations")


class RiskAnalysisResult(BaseModel):
    """Complete risk analysis result."""
    project_path: str = Field(..., description="Path to analyzed project")
    analysis_timestamp: str = Field(..., description="Analysis timestamp")
    overall_risk_score: RiskScore = Field(..., description="Overall risk assessment")
    circular_dependencies: List[CircularDependency] = Field(default_factory=list)
    dead_code: List[DeadCodeItem] = Field(default_factory=list)
    coupling_metrics: List[CouplingMetrics] = Field(default_factory=list)
    test_coverage: List[TestCoverageReport] = Field(default_factory=list)
    risky_files: List[RiskyFile] = Field(default_factory=list)
    complexity_metrics: List[ComplexityMetrics] = Field(default_factory=list)
    summary: Dict[str, Any] = Field(default_factory=dict, description="Analysis summary")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RiskAnalysisRequest(BaseModel):
    """Request model for risk analysis."""
    directory: str = Field(..., description="Directory to analyze")
    file_patterns: Optional[List[str]] = Field(None, description="File patterns to include")
    exclude_patterns: Optional[List[str]] = Field(None, description="Patterns to exclude")
    include_tests: bool = Field(True, description="Include test coverage analysis")
    include_complexity: bool = Field(True, description="Include complexity analysis")
    include_dependencies: bool = Field(True, description="Include dependency analysis")
    max_depth: Optional[int] = Field(None, description="Maximum directory depth")


class RiskVisualization(BaseModel):
    """Visualization data for risk analysis."""
    risk_heatmap: Dict[str, Any] = Field(..., description="Risk heatmap data")
    dependency_graph: Dict[str, Any] = Field(..., description="Dependency graph with risk overlay")
    complexity_distribution: Dict[str, Any] = Field(..., description="Complexity distribution chart")
    risk_trends: Dict[str, Any] = Field(..., description="Risk trends over time")
    top_risks: List[Dict[str, Any]] = Field(..., description="Top risk items")

# Made with Bob
