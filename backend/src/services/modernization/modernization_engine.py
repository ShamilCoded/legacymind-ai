"""
Modernization recommendation engine for legacy repositories.

Provides comprehensive analysis and recommendations for:
- Monolith to microservice migration
- Outdated dependency detection
- Refactoring recommendations
- Cloud migration guidance
- Scalability analysis
"""
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

from .models import (
    ModernizationRequest,
    ModernizationResult,
    ModernizationRoadmap,
    MigrationPhase,
    MigrationTask,
    ModernizationPriority,
    MigrationComplexity
)
from .dependency_analyzer import DependencyAnalyzer
from .microservice_analyzer import MicroserviceAnalyzer
from .refactoring_analyzer import RefactoringAnalyzer
from .cloud_migration_planner import CloudMigrationPlanner
from .scalability_analyzer import ScalabilityAnalyzer
from .roadmap_generator import RoadmapGenerator

logger = logging.getLogger(__name__)


class ModernizationEngine:
    """Main engine for modernization recommendations."""
    
    def __init__(self):
        """Initialize modernization engine."""
        self.dependency_analyzer = DependencyAnalyzer()
        self.microservice_analyzer = MicroserviceAnalyzer()
        self.refactoring_analyzer = RefactoringAnalyzer()
        self.cloud_migration_planner = CloudMigrationPlanner()
        self.scalability_analyzer = ScalabilityAnalyzer()
        self.roadmap_generator = RoadmapGenerator()
    
    def analyze(self, request: ModernizationRequest) -> ModernizationResult:
        """
        Perform comprehensive modernization analysis.
        
        Args:
            request: Modernization request with configuration
            
        Returns:
            Complete modernization analysis result
        """
        logger.info(f"Starting modernization analysis for {request.directory}")
        
        directory = Path(request.directory)
        if not directory.exists():
            raise ValueError(f"Directory not found: {request.directory}")
        
        # Initialize result components
        dependency_analysis = None
        microservice_recommendation = None
        refactoring_recommendation = None
        cloud_migration_plan = None
        scalability_analysis = None
        
        # 1. Analyze dependencies
        if request.analyze_dependencies:
            logger.info("Analyzing dependencies...")
            dependency_analysis = self.dependency_analyzer.analyze(str(directory))
        
        # 2. Analyze architecture for microservices
        if request.analyze_architecture:
            logger.info("Analyzing architecture for microservices...")
            microservice_recommendation = self.microservice_analyzer.analyze(
                str(directory),
                file_patterns=request.file_patterns,
                exclude_patterns=request.exclude_patterns
            )
        
        # 3. Analyze code quality and refactoring needs
        logger.info("Analyzing code quality...")
        refactoring_recommendation = self.refactoring_analyzer.analyze(
            str(directory),
            file_patterns=request.file_patterns,
            exclude_patterns=request.exclude_patterns
        )
        
        # 4. Create cloud migration plan
        if request.target_cloud:
            logger.info(f"Creating cloud migration plan for {request.target_cloud}...")
            cloud_migration_plan = self.cloud_migration_planner.create_plan(
                directory=str(directory),
                target_provider=request.target_cloud,
                current_architecture=microservice_recommendation.current_architecture if microservice_recommendation else None,
                include_cost_estimates=request.include_cost_estimates
            )
        
        # 5. Analyze scalability
        if request.analyze_scalability:
            logger.info("Analyzing scalability...")
            scalability_analysis = self.scalability_analyzer.analyze(
                str(directory),
                file_patterns=request.file_patterns,
                exclude_patterns=request.exclude_patterns
            )
        
        # 6. Calculate overall modernization score
        overall_score = self._calculate_modernization_score(
            dependency_analysis,
            microservice_recommendation,
            refactoring_recommendation,
            scalability_analysis
        )
        
        # 7. Generate modernization roadmap
        logger.info("Generating modernization roadmap...")
        roadmap = self.roadmap_generator.generate(
            dependency_analysis=dependency_analysis,
            microservice_recommendation=microservice_recommendation,
            refactoring_recommendation=refactoring_recommendation,
            cloud_migration_plan=cloud_migration_plan,
            scalability_analysis=scalability_analysis
        )
        
        # 8. Generate summary and recommendations
        summary = self._generate_summary(
            dependency_analysis,
            microservice_recommendation,
            refactoring_recommendation,
            cloud_migration_plan,
            scalability_analysis
        )
        
        immediate_actions = self._identify_immediate_actions(
            dependency_analysis,
            microservice_recommendation,
            refactoring_recommendation,
            scalability_analysis
        )
        
        long_term_goals = self._identify_long_term_goals(
            microservice_recommendation,
            cloud_migration_plan,
            scalability_analysis
        )
        
        # Calculate total effort and cost
        total_effort_weeks = roadmap.total_duration_weeks
        total_cost = cloud_migration_plan.estimated_total_cost if cloud_migration_plan else 0
        
        # Calculate ROI
        expected_roi = self._calculate_roi(
            total_cost,
            microservice_recommendation,
            scalability_analysis
        )
        
        logger.info(f"Modernization analysis complete. Score: {overall_score}")
        
        return ModernizationResult(
            timestamp=datetime.now(),
            directory=str(directory),
            summary=summary,
            overall_modernization_score=overall_score,
            dependency_analysis=dependency_analysis,
            microservice_recommendation=microservice_recommendation,
            refactoring_recommendation=refactoring_recommendation,
            cloud_migration_plan=cloud_migration_plan,
            scalability_analysis=scalability_analysis,
            roadmap=roadmap,
            immediate_actions=immediate_actions,
            long_term_goals=long_term_goals,
            estimated_total_effort_weeks=total_effort_weeks,
            estimated_total_cost=total_cost,
            expected_roi=expected_roi
        )
    
    def _calculate_modernization_score(
        self,
        dependency_analysis,
        microservice_recommendation,
        refactoring_recommendation,
        scalability_analysis
    ) -> float:
        """Calculate overall modernization score (0-100)."""
        score = 100.0
        
        # Deduct for outdated dependencies
        if dependency_analysis:
            critical_deps = dependency_analysis.critical_updates
            security_issues = dependency_analysis.security_issues
            score -= min(critical_deps * 5, 20)
            score -= min(security_issues * 3, 15)
        
        # Deduct for technical debt
        if refactoring_recommendation:
            debt_score = refactoring_recommendation.technical_debt_score
            score -= (debt_score / 100) * 25
        
        # Deduct for scalability issues
        if scalability_analysis:
            scalability_score = scalability_analysis.current_scalability_score
            score -= (100 - scalability_score) * 0.2
        
        # Deduct for monolithic architecture
        if microservice_recommendation and not microservice_recommendation.is_suitable_for_microservices:
            score -= 10
        
        return max(0, min(100, round(score, 1)))
    
    def _generate_summary(
        self,
        dependency_analysis,
        microservice_recommendation,
        refactoring_recommendation,
        cloud_migration_plan,
        scalability_analysis
    ) -> str:
        """Generate executive summary."""
        parts = []
        
        # Architecture assessment
        if microservice_recommendation:
            if microservice_recommendation.is_suitable_for_microservices:
                parts.append(
                    f"The codebase is suitable for microservices migration with "
                    f"{len(microservice_recommendation.identified_services)} potential services identified."
                )
            else:
                parts.append(
                    f"The codebase follows a {microservice_recommendation.current_architecture.value} "
                    f"architecture pattern."
                )
        
        # Dependency issues
        if dependency_analysis:
            if dependency_analysis.critical_updates > 0:
                parts.append(
                    f"Found {dependency_analysis.critical_updates} critical dependency updates "
                    f"and {dependency_analysis.security_issues} security issues requiring immediate attention."
                )
        
        # Technical debt
        if refactoring_recommendation:
            debt_level = "high" if refactoring_recommendation.technical_debt_score > 60 else \
                        "moderate" if refactoring_recommendation.technical_debt_score > 30 else "low"
            parts.append(
                f"Technical debt is {debt_level} with a maintainability index of "
                f"{refactoring_recommendation.maintainability_index:.1f}/100."
            )
        
        # Cloud migration
        if cloud_migration_plan:
            parts.append(
                f"Cloud migration to {cloud_migration_plan.target_provider.value} is recommended "
                f"using a {cloud_migration_plan.migration_strategy} strategy."
            )
        
        # Scalability
        if scalability_analysis:
            parts.append(
                f"Current scalability score is {scalability_analysis.current_scalability_score:.1f}/100 "
                f"with {len(scalability_analysis.identified_bottlenecks)} bottlenecks identified."
            )
        
        return " ".join(parts)
    
    def _identify_immediate_actions(
        self,
        dependency_analysis,
        microservice_recommendation,
        refactoring_recommendation,
        scalability_analysis
    ) -> List[str]:
        """Identify immediate action items."""
        actions = []
        
        # Critical security updates
        if dependency_analysis and dependency_analysis.critical_updates > 0:
            actions.append(
                f"Update {dependency_analysis.critical_updates} critical dependencies with security vulnerabilities"
            )
        
        # High priority refactorings
        if refactoring_recommendation:
            priority_items = refactoring_recommendation.priority_refactorings[:3]
            actions.extend(priority_items)
        
        # Critical bottlenecks
        if scalability_analysis:
            critical_bottlenecks = [
                b for b in scalability_analysis.identified_bottlenecks
                if b.severity == ModernizationPriority.CRITICAL
            ]
            if critical_bottlenecks:
                actions.append(
                    f"Address {len(critical_bottlenecks)} critical performance bottlenecks"
                )
        
        # Containerization
        if microservice_recommendation and microservice_recommendation.is_suitable_for_microservices:
            actions.append("Implement containerization with Docker")
        
        return actions[:5]  # Top 5 immediate actions
    
    def _identify_long_term_goals(
        self,
        microservice_recommendation,
        cloud_migration_plan,
        scalability_analysis
    ) -> List[str]:
        """Identify long-term goals."""
        goals = []
        
        # Microservices migration
        if microservice_recommendation and microservice_recommendation.is_suitable_for_microservices:
            goals.append(
                f"Migrate to microservices architecture with {len(microservice_recommendation.identified_services)} services"
            )
        
        # Cloud migration
        if cloud_migration_plan:
            goals.append(
                f"Complete cloud migration to {cloud_migration_plan.target_provider.value}"
            )
        
        # Scalability improvements
        if scalability_analysis:
            goals.append(
                f"Improve scalability score to 90+ (current: {scalability_analysis.current_scalability_score:.1f})"
            )
        
        # Architecture modernization
        goals.append("Achieve 90+ maintainability index")
        goals.append("Implement comprehensive monitoring and observability")
        goals.append("Establish automated CI/CD pipeline")
        
        return goals
    
    def _calculate_roi(
        self,
        total_cost: float,
        microservice_recommendation,
        scalability_analysis
    ) -> str:
        """Calculate expected return on investment."""
        if total_cost == 0:
            return "ROI calculation requires cost estimates"
        
        benefits = []
        
        # Scalability benefits
        if scalability_analysis:
            capacity_increase = scalability_analysis.estimated_capacity_increase
            if capacity_increase:
                benefits.append(f"Capacity increase: {capacity_increase}")
        
        # Microservices benefits
        if microservice_recommendation and microservice_recommendation.is_suitable_for_microservices:
            benefits.extend([
                "Improved development velocity (30-50%)",
                "Better fault isolation and reliability",
                "Independent scaling of services"
            ])
        
        # Cost savings
        estimated_savings = total_cost * 0.3  # 30% annual savings estimate
        payback_period = total_cost / estimated_savings if estimated_savings > 0 else 0
        
        roi_text = f"Expected payback period: {payback_period:.1f} years. "
        roi_text += "Benefits: " + "; ".join(benefits)
        
        return roi_text


# Made with Bob