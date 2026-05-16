"""
Roadmap generator for creating modernization migration plans.
"""
import logging
from typing import List, Dict, Any, Optional

from .models import (
    ModernizationRoadmap,
    MigrationPhase,
    MigrationTask,
    ModernizationPriority,
    MigrationComplexity,
    DependencyAnalysis,
    MicroserviceRecommendation,
    RefactoringRecommendation,
    CloudMigrationPlan,
    ScalabilityAnalysis
)

logger = logging.getLogger(__name__)


class RoadmapGenerator:
    """Generates comprehensive modernization roadmaps."""
    
    def generate(
        self,
        dependency_analysis: Optional[DependencyAnalysis] = None,
        microservice_recommendation: Optional[MicroserviceRecommendation] = None,
        refactoring_recommendation: Optional[RefactoringRecommendation] = None,
        cloud_migration_plan: Optional[CloudMigrationPlan] = None,
        scalability_analysis: Optional[ScalabilityAnalysis] = None
    ) -> ModernizationRoadmap:
        """
        Generate modernization roadmap.
        
        Args:
            dependency_analysis: Dependency analysis results
            microservice_recommendation: Microservice recommendations
            refactoring_recommendation: Refactoring recommendations
            cloud_migration_plan: Cloud migration plan
            scalability_analysis: Scalability analysis
            
        Returns:
            Complete modernization roadmap
        """
        logger.info("Generating modernization roadmap")
        
        phases = []
        
        # Phase 1: Foundation and Quick Wins
        phase1 = self._create_foundation_phase(
            dependency_analysis,
            refactoring_recommendation,
            scalability_analysis
        )
        phases.append(phase1)
        
        # Phase 2: Code Quality and Refactoring
        phase2 = self._create_refactoring_phase(
            refactoring_recommendation,
            dependency_analysis
        )
        phases.append(phase2)
        
        # Phase 3: Containerization and Infrastructure
        phase3 = self._create_infrastructure_phase(
            cloud_migration_plan,
            microservice_recommendation
        )
        phases.append(phase3)
        
        # Phase 4: Architecture Modernization
        if microservice_recommendation and microservice_recommendation.is_suitable_for_microservices:
            phase4 = self._create_architecture_phase(
                microservice_recommendation
            )
            phases.append(phase4)
        
        # Phase 5: Cloud Migration
        if cloud_migration_plan:
            phase5 = self._create_cloud_migration_phase(
                cloud_migration_plan
            )
            phases.append(phase5)
        
        # Phase 6: Optimization and Scaling
        phase6 = self._create_optimization_phase(
            scalability_analysis
        )
        phases.append(phase6)
        
        # Calculate totals
        total_duration = sum(p.duration_weeks for p in phases)
        total_effort = sum(
            sum(t.estimated_hours for t in p.tasks)
            for p in phases
        )
        
        # Identify critical path
        critical_path = self._identify_critical_path(phases)
        
        # Identify quick wins
        quick_wins = self._identify_quick_wins(phases)
        
        # Generate risk mitigation strategies
        risk_mitigation = self._generate_risk_mitigation()
        
        # Define success metrics
        success_metrics = self._define_success_metrics()
        
        # Recommend team size
        team_size = self._recommend_team_size(total_duration, total_effort)
        
        return ModernizationRoadmap(
            phases=phases,
            total_duration_weeks=total_duration,
            total_effort_hours=total_effort,
            team_size_recommendation=team_size,
            critical_path=critical_path,
            quick_wins=quick_wins,
            risk_mitigation=risk_mitigation,
            success_metrics=success_metrics
        )
    
    def _create_foundation_phase(
        self,
        dependency_analysis: Optional[DependencyAnalysis],
        refactoring_recommendation: Optional[RefactoringRecommendation],
        scalability_analysis: Optional[ScalabilityAnalysis]
    ) -> MigrationPhase:
        """Create foundation and quick wins phase."""
        tasks = []
        
        # Critical dependency updates
        if dependency_analysis and dependency_analysis.critical_updates > 0:
            tasks.append(MigrationTask(
                task_id="F1",
                title="Update Critical Dependencies",
                description=f"Update {dependency_analysis.critical_updates} critical dependencies with security vulnerabilities",
                category="Dependencies",
                priority=ModernizationPriority.CRITICAL,
                complexity=MigrationComplexity.SIMPLE,
                estimated_hours=dependency_analysis.total_update_effort_hours,
                dependencies=[],
                deliverables=[
                    "Updated dependency files",
                    "Passing test suite",
                    "Security scan report"
                ],
                risks=["Breaking changes in dependencies", "Test failures"],
                success_criteria=[
                    "All critical vulnerabilities resolved",
                    "All tests passing",
                    "Application running stable"
                ]
            ))
        
        # Set up CI/CD
        tasks.append(MigrationTask(
            task_id="F2",
            title="Establish CI/CD Pipeline",
            description="Set up automated testing and deployment pipeline",
            category="Infrastructure",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=16.0,
            dependencies=[],
            deliverables=[
                "CI/CD pipeline configuration",
                "Automated test execution",
                "Deployment automation"
            ],
            risks=["Integration issues", "Learning curve"],
            success_criteria=[
                "Automated builds on commit",
                "Automated test execution",
                "Successful deployments"
            ]
        ))
        
        # Code documentation
        tasks.append(MigrationTask(
            task_id="F3",
            title="Document Current Architecture",
            description="Create comprehensive documentation of current system",
            category="Documentation",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.SIMPLE,
            estimated_hours=12.0,
            dependencies=[],
            deliverables=[
                "Architecture diagrams",
                "API documentation",
                "Deployment guide"
            ],
            risks=["Incomplete documentation"],
            success_criteria=[
                "All major components documented",
                "Team review completed"
            ]
        ))
        
        # Monitoring setup
        tasks.append(MigrationTask(
            task_id="F4",
            title="Implement Monitoring and Logging",
            description="Set up comprehensive monitoring and logging infrastructure",
            category="Observability",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=20.0,
            dependencies=["F2"],
            deliverables=[
                "Monitoring dashboards",
                "Log aggregation",
                "Alert configuration"
            ],
            risks=["Data overload", "Alert fatigue"],
            success_criteria=[
                "Key metrics tracked",
                "Alerts configured",
                "Logs centralized"
            ]
        ))
        
        return MigrationPhase(
            phase_number=1,
            name="Foundation and Quick Wins",
            description="Establish foundation for modernization with critical updates and infrastructure",
            duration_weeks=4.0,
            tasks=tasks,
            milestones=[
                "Critical vulnerabilities resolved",
                "CI/CD pipeline operational",
                "Monitoring in place"
            ],
            success_criteria=[
                "All critical dependencies updated",
                "Automated deployment working",
                "System health visible"
            ],
            rollback_plan="Maintain current production environment until phase completion verified"
        )
    
    def _create_refactoring_phase(
        self,
        refactoring_recommendation: Optional[RefactoringRecommendation],
        dependency_analysis: Optional[DependencyAnalysis]
    ) -> MigrationPhase:
        """Create code quality and refactoring phase."""
        tasks = []
        
        # Address code smells
        if refactoring_recommendation:
            tasks.append(MigrationTask(
                task_id="R1",
                title="Refactor High-Priority Code Smells",
                description="Address critical and high-priority code quality issues",
                category="Code Quality",
                priority=ModernizationPriority.HIGH,
                complexity=MigrationComplexity.MODERATE,
                estimated_hours=refactoring_recommendation.total_refactoring_effort_hours * 0.3,
                dependencies=["F1"],
                deliverables=[
                    "Refactored code",
                    "Updated tests",
                    "Code review approval"
                ],
                risks=["Regression bugs", "Scope creep"],
                success_criteria=[
                    "Code smell count reduced by 50%",
                    "All tests passing",
                    "Code coverage maintained"
                ]
            ))
        
        # Implement design patterns
        if refactoring_recommendation and refactoring_recommendation.design_patterns:
            tasks.append(MigrationTask(
                task_id="R2",
                title="Implement Design Patterns",
                description="Apply recommended design patterns for better architecture",
                category="Architecture",
                priority=ModernizationPriority.MEDIUM,
                complexity=MigrationComplexity.COMPLEX,
                estimated_hours=sum(p.estimated_effort_hours for p in refactoring_recommendation.design_patterns),
                dependencies=["R1"],
                deliverables=[
                    "Pattern implementations",
                    "Updated documentation",
                    "Code examples"
                ],
                risks=["Over-engineering", "Team learning curve"],
                success_criteria=[
                    "Patterns correctly implemented",
                    "Code more maintainable",
                    "Team trained on patterns"
                ]
            ))
        
        # Update remaining dependencies
        if dependency_analysis:
            tasks.append(MigrationTask(
                task_id="R3",
                title="Update Non-Critical Dependencies",
                description="Update remaining outdated dependencies",
                category="Dependencies",
                priority=ModernizationPriority.MEDIUM,
                complexity=MigrationComplexity.SIMPLE,
                estimated_hours=dependency_analysis.total_update_effort_hours * 0.5,
                dependencies=["F1"],
                deliverables=[
                    "Updated dependencies",
                    "Compatibility testing",
                    "Migration notes"
                ],
                risks=["Breaking changes", "Compatibility issues"],
                success_criteria=[
                    "All dependencies up to date",
                    "No security vulnerabilities",
                    "Tests passing"
                ]
            ))
        
        return MigrationPhase(
            phase_number=2,
            name="Code Quality and Refactoring",
            description="Improve code quality and implement better design patterns",
            duration_weeks=6.0,
            tasks=tasks,
            milestones=[
                "Major code smells addressed",
                "Design patterns implemented",
                "Dependencies updated"
            ],
            success_criteria=[
                "Technical debt reduced by 40%",
                "Maintainability index improved",
                "Code review standards met"
            ],
            rollback_plan="Feature flags allow gradual rollout with quick rollback"
        )
    
    def _create_infrastructure_phase(
        self,
        cloud_migration_plan: Optional[CloudMigrationPlan],
        microservice_recommendation: Optional[MicroserviceRecommendation]
    ) -> MigrationPhase:
        """Create containerization and infrastructure phase."""
        tasks = []
        
        # Containerization
        if cloud_migration_plan and cloud_migration_plan.containerization_needed:
            tasks.append(MigrationTask(
                task_id="I1",
                title="Containerize Application",
                description="Create Docker containers for application components",
                category="Infrastructure",
                priority=ModernizationPriority.HIGH,
                complexity=MigrationComplexity.MODERATE,
                estimated_hours=24.0,
                dependencies=["R1"],
                deliverables=[
                    "Dockerfiles",
                    "Docker Compose configuration",
                    "Container registry setup"
                ],
                risks=["Configuration complexity", "Image size"],
                success_criteria=[
                    "Application runs in containers",
                    "Development environment containerized",
                    "Images optimized"
                ]
            ))
        
        # Infrastructure as Code
        tasks.append(MigrationTask(
            task_id="I2",
            title="Implement Infrastructure as Code",
            description="Define infrastructure using IaC tools",
            category="Infrastructure",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=32.0,
            dependencies=["I1"] if cloud_migration_plan and cloud_migration_plan.containerization_needed else [],
            deliverables=[
                "IaC templates",
                "Environment configurations",
                "Deployment scripts"
            ],
            risks=["Learning curve", "State management"],
            success_criteria=[
                "Infrastructure reproducible",
                "Environments consistent",
                "Deployment automated"
            ]
        ))
        
        # Service mesh (if microservices)
        if microservice_recommendation and microservice_recommendation.is_suitable_for_microservices:
            tasks.append(MigrationTask(
                task_id="I3",
                title="Set Up Service Mesh",
                description="Implement service mesh for microservices communication",
                category="Infrastructure",
                priority=ModernizationPriority.MEDIUM,
                complexity=MigrationComplexity.COMPLEX,
                estimated_hours=40.0,
                dependencies=["I1", "I2"],
                deliverables=[
                    "Service mesh configuration",
                    "Traffic management rules",
                    "Security policies"
                ],
                risks=["Complexity", "Performance overhead"],
                success_criteria=[
                    "Service discovery working",
                    "Traffic routing configured",
                    "Observability enabled"
                ]
            ))
        
        return MigrationPhase(
            phase_number=3,
            name="Containerization and Infrastructure",
            description="Modernize infrastructure with containers and automation",
            duration_weeks=5.0,
            tasks=tasks,
            milestones=[
                "Application containerized",
                "IaC implemented",
                "Infrastructure automated"
            ],
            success_criteria=[
                "Containers running stable",
                "Infrastructure reproducible",
                "Deployment time reduced"
            ],
            rollback_plan="Maintain parallel traditional deployment until containers proven"
        )
    
    def _create_architecture_phase(
        self,
        microservice_recommendation: MicroserviceRecommendation
    ) -> MigrationPhase:
        """Create architecture modernization phase."""
        tasks = []
        
        service_count = len(microservice_recommendation.identified_services)
        
        tasks.append(MigrationTask(
            task_id="A1",
            title="Extract First Microservice",
            description="Extract and deploy first microservice as proof of concept",
            category="Architecture",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.COMPLEX,
            estimated_hours=80.0,
            dependencies=["I2"],
            deliverables=[
                "Extracted service",
                "API contracts",
                "Service deployment"
            ],
            risks=["Data consistency", "Service boundaries"],
            success_criteria=[
                "Service independently deployable",
                "API working correctly",
                "Performance acceptable"
            ]
        ))
        
        tasks.append(MigrationTask(
            task_id="A2",
            title=f"Extract Remaining {service_count - 1} Microservices",
            description="Systematically extract remaining microservices",
            category="Architecture",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.VERY_COMPLEX,
            estimated_hours=microservice_recommendation.estimated_effort_weeks * 40 * 0.7,
            dependencies=["A1"],
            deliverables=[
                "All services extracted",
                "Service communication established",
                "Data migration completed"
            ],
            risks=["Distributed transactions", "Service coordination"],
            success_criteria=[
                "All services operational",
                "End-to-end flows working",
                "Performance targets met"
            ]
        ))
        
        tasks.append(MigrationTask(
            task_id="A3",
            title="Implement API Gateway",
            description="Set up API gateway for unified entry point",
            category="Architecture",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=24.0,
            dependencies=["A2"],
            deliverables=[
                "API gateway configuration",
                "Routing rules",
                "Authentication/authorization"
            ],
            risks=["Single point of failure", "Performance bottleneck"],
            success_criteria=[
                "Gateway routing correctly",
                "Security enforced",
                "Performance acceptable"
            ]
        ))
        
        return MigrationPhase(
            phase_number=4,
            name="Architecture Modernization",
            description="Migrate to microservices architecture",
            duration_weeks=microservice_recommendation.estimated_effort_weeks,
            tasks=tasks,
            milestones=[
                "First service extracted",
                "All services operational",
                "API gateway deployed"
            ],
            success_criteria=[
                "Microservices architecture implemented",
                "Services independently scalable",
                "System reliability maintained"
            ],
            rollback_plan="Strangler pattern allows gradual migration with fallback to monolith"
        )
    
    def _create_cloud_migration_phase(
        self,
        cloud_migration_plan: CloudMigrationPlan
    ) -> MigrationPhase:
        """Create cloud migration phase."""
        tasks = []
        
        for i, service in enumerate(cloud_migration_plan.recommended_services[:3], 1):
            tasks.append(MigrationTask(
                task_id=f"C{i}",
                title=f"Migrate to {service.service_name}",
                description=f"Migrate {service.purpose.lower()} to cloud",
                category="Cloud Migration",
                priority=ModernizationPriority.HIGH,
                complexity=MigrationComplexity.MODERATE,
                estimated_hours=40.0,
                dependencies=[f"C{i-1}"] if i > 1 else ["I2"],
                deliverables=[
                    f"{service.service_name} configured",
                    "Data migrated",
                    "Application updated"
                ],
                risks=["Data loss", "Downtime", "Cost overruns"],
                success_criteria=[
                    "Service operational in cloud",
                    "Data integrity verified",
                    "Performance acceptable"
                ]
            ))
        
        tasks.append(MigrationTask(
            task_id="C4",
            title="Complete Cloud Migration",
            description="Finalize cloud migration and decommission on-premise",
            category="Cloud Migration",
            priority=ModernizationPriority.HIGH,
            complexity=MigrationComplexity.COMPLEX,
            estimated_hours=60.0,
            dependencies=[f"C{len(tasks)}"],
            deliverables=[
                "All services in cloud",
                "DNS updated",
                "On-premise decommissioned"
            ],
            risks=["Service disruption", "Data synchronization"],
            success_criteria=[
                "100% traffic on cloud",
                "No on-premise dependencies",
                "Cost targets met"
            ]
        ))
        
        return MigrationPhase(
            phase_number=5,
            name="Cloud Migration",
            description=f"Migrate to {cloud_migration_plan.target_provider.value}",
            duration_weeks=cloud_migration_plan.estimated_migration_weeks,
            tasks=tasks,
            milestones=[
                "Core services migrated",
                "Data migration complete",
                "Production cutover"
            ],
            success_criteria=[
                "All services running in cloud",
                "Performance improved",
                "Cost within budget"
            ],
            rollback_plan="Maintain on-premise as hot standby during migration"
        )
    
    def _create_optimization_phase(
        self,
        scalability_analysis: Optional[ScalabilityAnalysis]
    ) -> MigrationPhase:
        """Create optimization and scaling phase."""
        tasks = []
        
        tasks.append(MigrationTask(
            task_id="O1",
            title="Implement Caching Strategy",
            description="Deploy comprehensive caching solution",
            category="Performance",
            priority=ModernizationPriority.MEDIUM,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=32.0,
            dependencies=[],
            deliverables=[
                "Cache infrastructure",
                "Cache policies",
                "Performance metrics"
            ],
            risks=["Cache invalidation", "Stale data"],
            success_criteria=[
                "Cache hit rate > 80%",
                "Response time improved",
                "Database load reduced"
            ]
        ))
        
        tasks.append(MigrationTask(
            task_id="O2",
            title="Optimize Database Performance",
            description="Implement database optimizations and scaling",
            category="Performance",
            priority=ModernizationPriority.MEDIUM,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=40.0,
            dependencies=[],
            deliverables=[
                "Query optimizations",
                "Indexes added",
                "Read replicas configured"
            ],
            risks=["Query complexity", "Replication lag"],
            success_criteria=[
                "Query time reduced by 50%",
                "Database CPU < 70%",
                "No slow queries"
            ]
        ))
        
        tasks.append(MigrationTask(
            task_id="O3",
            title="Implement Auto-Scaling",
            description="Configure automatic scaling based on load",
            category="Scalability",
            priority=ModernizationPriority.MEDIUM,
            complexity=MigrationComplexity.MODERATE,
            estimated_hours=24.0,
            dependencies=["O1", "O2"],
            deliverables=[
                "Scaling policies",
                "Load testing results",
                "Cost analysis"
            ],
            risks=["Scaling delays", "Cost spikes"],
            success_criteria=[
                "Auto-scaling working",
                "Handle 3x traffic",
                "Cost optimized"
            ]
        ))
        
        return MigrationPhase(
            phase_number=6,
            name="Optimization and Scaling",
            description="Optimize performance and implement auto-scaling",
            duration_weeks=4.0,
            tasks=tasks,
            milestones=[
                "Caching implemented",
                "Database optimized",
                "Auto-scaling configured"
            ],
            success_criteria=[
                "Performance targets met",
                "System scales automatically",
                "Cost efficiency achieved"
            ],
            rollback_plan="Performance optimizations can be reverted individually"
        )
    
    def _identify_critical_path(self, phases: List[MigrationPhase]) -> List[str]:
        """Identify critical path tasks."""
        critical = []
        for phase in phases:
            for task in phase.tasks:
                if task.priority == ModernizationPriority.CRITICAL or \
                   task.priority == ModernizationPriority.HIGH:
                    critical.append(f"{task.task_id}: {task.title}")
        return critical[:10]
    
    def _identify_quick_wins(self, phases: List[MigrationPhase]) -> List[str]:
        """Identify quick win opportunities."""
        quick_wins = []
        for phase in phases:
            for task in phase.tasks:
                if task.complexity == MigrationComplexity.SIMPLE and \
                   task.estimated_hours <= 16:
                    quick_wins.append(task.title)
        return quick_wins[:5]
    
    def _generate_risk_mitigation(self) -> List[str]:
        """Generate risk mitigation strategies."""
        return [
            "Implement feature flags for gradual rollout",
            "Maintain comprehensive test coverage",
            "Use blue-green deployments for zero-downtime",
            "Establish rollback procedures for each phase",
            "Conduct regular security audits",
            "Maintain parallel systems during critical migrations",
            "Implement circuit breakers for service resilience",
            "Regular stakeholder communication and demos",
            "Budget contingency for unexpected issues",
            "Team training and knowledge sharing sessions"
        ]
    
    def _define_success_metrics(self) -> List[str]:
        """Define success metrics."""
        return [
            "Deployment frequency increased by 10x",
            "Mean time to recovery (MTTR) < 1 hour",
            "System uptime > 99.9%",
            "Response time < 200ms for 95th percentile",
            "Zero critical security vulnerabilities",
            "Technical debt reduced by 60%",
            "Developer productivity increased by 40%",
            "Infrastructure costs optimized by 30%",
            "Customer satisfaction score improved",
            "Team satisfaction with development process"
        ]
    
    def _recommend_team_size(self, duration_weeks: float, effort_hours: float) -> int:
        """Recommend team size."""
        # Calculate based on effort and duration
        hours_per_week = 40
        total_person_weeks = effort_hours / hours_per_week
        avg_team_size = total_person_weeks / duration_weeks if duration_weeks > 0 else 3
        
        # Round up and ensure minimum of 3
        return max(3, int(avg_team_size) + 1)


# Made with Bob