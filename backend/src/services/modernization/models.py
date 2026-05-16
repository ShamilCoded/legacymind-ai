"""
Data models for modernization recommendation engine.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class ModernizationPriority(str, Enum):
    """Priority levels for modernization recommendations."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MigrationComplexity(str, Enum):
    """Complexity levels for migration tasks."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


class CloudProvider(str, Enum):
    """Supported cloud providers."""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"


class ArchitecturePattern(str, Enum):
    """Architecture patterns."""
    MONOLITH = "monolith"
    MICROSERVICES = "microservices"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"


# Request Models

class ModernizationRequest(BaseModel):
    """Request for modernization analysis."""
    directory: str = Field(..., description="Repository directory path")
    file_patterns: Optional[List[str]] = Field(None, description="File patterns to analyze")
    exclude_patterns: Optional[List[str]] = Field(None, description="Patterns to exclude")
    analyze_dependencies: bool = Field(True, description="Analyze outdated dependencies")
    analyze_architecture: bool = Field(True, description="Analyze architecture patterns")
    analyze_scalability: bool = Field(True, description="Analyze scalability")
    target_cloud: Optional[CloudProvider] = Field(None, description="Target cloud provider")
    include_cost_estimates: bool = Field(False, description="Include migration cost estimates")


# Dependency Analysis Models

class OutdatedDependency(BaseModel):
    """Information about an outdated dependency."""
    name: str = Field(..., description="Dependency name")
    current_version: str = Field(..., description="Current version")
    latest_version: str = Field(..., description="Latest stable version")
    versions_behind: int = Field(..., description="Number of versions behind")
    security_vulnerabilities: int = Field(0, description="Known security vulnerabilities")
    breaking_changes: bool = Field(False, description="Has breaking changes")
    update_priority: ModernizationPriority = Field(..., description="Update priority")
    migration_notes: str = Field("", description="Migration notes")
    estimated_effort_hours: float = Field(0, description="Estimated update effort")


class DependencyAnalysis(BaseModel):
    """Analysis of repository dependencies."""
    total_dependencies: int = Field(0, description="Total number of dependencies")
    outdated_dependencies: List[OutdatedDependency] = Field(default_factory=list)
    critical_updates: int = Field(0, description="Number of critical updates")
    security_issues: int = Field(0, description="Total security issues")
    deprecated_packages: List[str] = Field(default_factory=list)
    alternative_recommendations: Dict[str, str] = Field(default_factory=dict)
    total_update_effort_hours: float = Field(0, description="Total estimated effort")


# Microservice Recommendations

class ServiceBoundary(BaseModel):
    """Identified service boundary for microservice extraction."""
    name: str = Field(..., description="Suggested service name")
    files: List[str] = Field(default_factory=list, description="Files in this service")
    responsibilities: List[str] = Field(default_factory=list, description="Service responsibilities")
    dependencies: List[str] = Field(default_factory=list, description="Dependencies on other services")
    api_endpoints: List[str] = Field(default_factory=list, description="API endpoints")
    data_entities: List[str] = Field(default_factory=list, description="Data entities managed")
    cohesion_score: float = Field(0, description="Internal cohesion score (0-1)")
    coupling_score: float = Field(0, description="External coupling score (0-1)")


class MicroserviceRecommendation(BaseModel):
    """Recommendations for microservice architecture."""
    current_architecture: ArchitecturePattern = Field(..., description="Current architecture")
    recommended_architecture: ArchitecturePattern = Field(..., description="Recommended architecture")
    is_suitable_for_microservices: bool = Field(..., description="Whether microservices are suitable")
    identified_services: List[ServiceBoundary] = Field(default_factory=list)
    shared_components: List[str] = Field(default_factory=list, description="Shared components")
    communication_patterns: Dict[str, str] = Field(default_factory=dict)
    data_management_strategy: str = Field("", description="Recommended data management")
    migration_complexity: MigrationComplexity = Field(..., description="Migration complexity")
    benefits: List[str] = Field(default_factory=list, description="Expected benefits")
    challenges: List[str] = Field(default_factory=list, description="Potential challenges")
    estimated_effort_weeks: float = Field(0, description="Estimated migration effort")


# Refactoring Recommendations

class CodeSmell(BaseModel):
    """Identified code smell."""
    type: str = Field(..., description="Code smell type")
    file_path: str = Field(..., description="File path")
    line_number: int = Field(0, description="Line number")
    severity: ModernizationPriority = Field(..., description="Severity")
    description: str = Field(..., description="Description")
    recommendation: str = Field(..., description="Refactoring recommendation")
    estimated_effort_hours: float = Field(0, description="Estimated effort")


class DesignPatternRecommendation(BaseModel):
    """Design pattern recommendation."""
    pattern_name: str = Field(..., description="Design pattern name")
    applicable_to: List[str] = Field(default_factory=list, description="Applicable files/modules")
    current_approach: str = Field(..., description="Current implementation approach")
    recommended_approach: str = Field(..., description="Recommended pattern approach")
    benefits: List[str] = Field(default_factory=list, description="Benefits")
    implementation_guide: str = Field("", description="Implementation guide")
    estimated_effort_hours: float = Field(0, description="Estimated effort")


class RefactoringRecommendation(BaseModel):
    """Comprehensive refactoring recommendations."""
    code_smells: List[CodeSmell] = Field(default_factory=list)
    design_patterns: List[DesignPatternRecommendation] = Field(default_factory=list)
    duplicate_code_blocks: int = Field(0, description="Number of duplicate code blocks")
    long_methods: int = Field(0, description="Number of long methods")
    large_classes: int = Field(0, description="Number of large classes")
    technical_debt_score: float = Field(0, description="Technical debt score (0-100)")
    maintainability_index: float = Field(0, description="Maintainability index (0-100)")
    priority_refactorings: List[str] = Field(default_factory=list)
    total_refactoring_effort_hours: float = Field(0, description="Total estimated effort")


# Cloud Migration Models

class CloudService(BaseModel):
    """Cloud service recommendation."""
    service_name: str = Field(..., description="Cloud service name")
    provider: CloudProvider = Field(..., description="Cloud provider")
    purpose: str = Field(..., description="Service purpose")
    current_equivalent: str = Field("", description="Current on-premise equivalent")
    migration_steps: List[str] = Field(default_factory=list)
    estimated_cost_monthly: float = Field(0, description="Estimated monthly cost")
    configuration_notes: str = Field("", description="Configuration notes")


class CloudMigrationPlan(BaseModel):
    """Cloud migration plan and recommendations."""
    target_provider: CloudProvider = Field(..., description="Target cloud provider")
    migration_strategy: str = Field(..., description="Migration strategy (lift-shift, re-architect, etc.)")
    recommended_services: List[CloudService] = Field(default_factory=list)
    containerization_needed: bool = Field(False, description="Whether containerization is needed")
    container_strategy: str = Field("", description="Container strategy")
    infrastructure_as_code: str = Field("", description="IaC tool recommendation")
    ci_cd_recommendations: List[str] = Field(default_factory=list)
    security_considerations: List[str] = Field(default_factory=list)
    compliance_requirements: List[str] = Field(default_factory=list)
    estimated_migration_weeks: float = Field(0, description="Estimated migration time")
    estimated_total_cost: float = Field(0, description="Estimated total migration cost")
    monthly_operational_cost: float = Field(0, description="Estimated monthly operational cost")


# Scalability Analysis Models

class BottleneckAnalysis(BaseModel):
    """Identified performance bottleneck."""
    location: str = Field(..., description="Bottleneck location")
    type: str = Field(..., description="Bottleneck type (CPU, I/O, memory, etc.)")
    severity: ModernizationPriority = Field(..., description="Severity")
    description: str = Field(..., description="Description")
    impact: str = Field(..., description="Performance impact")
    recommendation: str = Field(..., description="Optimization recommendation")
    estimated_improvement: str = Field("", description="Expected improvement")


class ScalabilityAnalysis(BaseModel):
    """Scalability analysis and recommendations."""
    current_scalability_score: float = Field(0, description="Current scalability score (0-100)")
    horizontal_scalability: str = Field("", description="Horizontal scalability assessment")
    vertical_scalability: str = Field("", description="Vertical scalability assessment")
    identified_bottlenecks: List[BottleneckAnalysis] = Field(default_factory=list)
    caching_recommendations: List[str] = Field(default_factory=list)
    database_optimization: List[str] = Field(default_factory=list)
    async_processing_opportunities: List[str] = Field(default_factory=list)
    load_balancing_strategy: str = Field("", description="Load balancing recommendations")
    auto_scaling_recommendations: List[str] = Field(default_factory=list)
    performance_monitoring: List[str] = Field(default_factory=list)
    estimated_capacity_increase: str = Field("", description="Expected capacity increase")


# Migration Roadmap Models

class MigrationTask(BaseModel):
    """Individual migration task."""
    task_id: str = Field(..., description="Task identifier")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")
    category: str = Field(..., description="Task category")
    priority: ModernizationPriority = Field(..., description="Task priority")
    complexity: MigrationComplexity = Field(..., description="Task complexity")
    estimated_hours: float = Field(0, description="Estimated effort in hours")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    deliverables: List[str] = Field(default_factory=list, description="Expected deliverables")
    risks: List[str] = Field(default_factory=list, description="Associated risks")
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria")


class MigrationPhase(BaseModel):
    """Migration phase in the roadmap."""
    phase_number: int = Field(..., description="Phase number")
    name: str = Field(..., description="Phase name")
    description: str = Field(..., description="Phase description")
    duration_weeks: float = Field(0, description="Estimated duration in weeks")
    tasks: List[MigrationTask] = Field(default_factory=list)
    milestones: List[str] = Field(default_factory=list, description="Phase milestones")
    success_criteria: List[str] = Field(default_factory=list, description="Phase success criteria")
    rollback_plan: str = Field("", description="Rollback strategy")


class ModernizationRoadmap(BaseModel):
    """Complete modernization roadmap."""
    phases: List[MigrationPhase] = Field(default_factory=list)
    total_duration_weeks: float = Field(0, description="Total estimated duration")
    total_effort_hours: float = Field(0, description="Total estimated effort")
    team_size_recommendation: int = Field(0, description="Recommended team size")
    critical_path: List[str] = Field(default_factory=list, description="Critical path tasks")
    quick_wins: List[str] = Field(default_factory=list, description="Quick win opportunities")
    risk_mitigation: List[str] = Field(default_factory=list, description="Risk mitigation strategies")
    success_metrics: List[str] = Field(default_factory=list, description="Success metrics")


# Main Result Model

class ModernizationResult(BaseModel):
    """Complete modernization analysis result."""
    timestamp: datetime = Field(default_factory=datetime.now)
    directory: str = Field(..., description="Analyzed directory")
    summary: str = Field(..., description="Executive summary")
    overall_modernization_score: float = Field(0, description="Overall modernization score (0-100)")
    
    # Analysis results
    dependency_analysis: Optional[DependencyAnalysis] = None
    microservice_recommendation: Optional[MicroserviceRecommendation] = None
    refactoring_recommendation: Optional[RefactoringRecommendation] = None
    cloud_migration_plan: Optional[CloudMigrationPlan] = None
    scalability_analysis: Optional[ScalabilityAnalysis] = None
    
    # Roadmap
    roadmap: ModernizationRoadmap = Field(..., description="Modernization roadmap")
    
    # Recommendations
    immediate_actions: List[str] = Field(default_factory=list, description="Immediate action items")
    long_term_goals: List[str] = Field(default_factory=list, description="Long-term goals")
    
    # Metrics
    estimated_total_effort_weeks: float = Field(0, description="Total estimated effort")
    estimated_total_cost: float = Field(0, description="Estimated total cost")
    expected_roi: str = Field("", description="Expected return on investment")
    
    class Config:
        json_schema_extra = {
            "example": {
                "directory": "./legacy-app",
                "summary": "Legacy monolith application suitable for microservices migration",
                "overall_modernization_score": 65.5,
                "estimated_total_effort_weeks": 24,
                "immediate_actions": [
                    "Update critical security vulnerabilities",
                    "Implement containerization",
                    "Set up CI/CD pipeline"
                ]
            }
        }


# Made with Bob