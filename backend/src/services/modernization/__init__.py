"""
Modernization recommendation engine for legacy repositories.

Provides comprehensive analysis and recommendations for:
- Monolith to microservice migration
- Outdated dependency detection
- Refactoring recommendations
- Cloud migration guidance
- Scalability analysis
"""

from .models import (
    ModernizationRequest,
    ModernizationResult,
    DependencyAnalysis,
    MicroserviceRecommendation,
    RefactoringRecommendation,
    CloudMigrationPlan,
    ScalabilityAnalysis,
    ModernizationRoadmap,
    MigrationPhase
)
from .modernization_engine import ModernizationEngine

__all__ = [
    'ModernizationEngine',
    'ModernizationRequest',
    'ModernizationResult',
    'DependencyAnalysis',
    'MicroserviceRecommendation',
    'RefactoringRecommendation',
    'CloudMigrationPlan',
    'ScalabilityAnalysis',
    'ModernizationRoadmap',
    'MigrationPhase'
]

# Made with Bob
