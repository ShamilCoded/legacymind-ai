"""
Cloud migration planner for creating migration strategies and recommendations.
"""
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from .models import (
    CloudMigrationPlan,
    CloudService,
    CloudProvider,
    ArchitecturePattern
)

logger = logging.getLogger(__name__)


class CloudMigrationPlanner:
    """Creates cloud migration plans and recommendations."""
    
    # Cloud service mappings
    CLOUD_SERVICES = {
        CloudProvider.AWS: {
            'compute': {
                'name': 'EC2 / ECS / Lambda',
                'purpose': 'Application hosting and compute',
                'monthly_cost': 200
            },
            'database': {
                'name': 'RDS / DynamoDB',
                'purpose': 'Managed database services',
                'monthly_cost': 150
            },
            'storage': {
                'name': 'S3',
                'purpose': 'Object storage',
                'monthly_cost': 50
            },
            'cache': {
                'name': 'ElastiCache',
                'purpose': 'In-memory caching',
                'monthly_cost': 100
            },
            'queue': {
                'name': 'SQS / SNS',
                'purpose': 'Message queuing and pub/sub',
                'monthly_cost': 30
            },
            'cdn': {
                'name': 'CloudFront',
                'purpose': 'Content delivery network',
                'monthly_cost': 80
            },
            'monitoring': {
                'name': 'CloudWatch',
                'purpose': 'Monitoring and logging',
                'monthly_cost': 50
            }
        },
        CloudProvider.AZURE: {
            'compute': {
                'name': 'Virtual Machines / App Service / Functions',
                'purpose': 'Application hosting and compute',
                'monthly_cost': 220
            },
            'database': {
                'name': 'Azure SQL / Cosmos DB',
                'purpose': 'Managed database services',
                'monthly_cost': 160
            },
            'storage': {
                'name': 'Blob Storage',
                'purpose': 'Object storage',
                'monthly_cost': 55
            },
            'cache': {
                'name': 'Azure Cache for Redis',
                'purpose': 'In-memory caching',
                'monthly_cost': 110
            },
            'queue': {
                'name': 'Service Bus / Event Grid',
                'purpose': 'Message queuing and events',
                'monthly_cost': 35
            },
            'cdn': {
                'name': 'Azure CDN',
                'purpose': 'Content delivery network',
                'monthly_cost': 85
            },
            'monitoring': {
                'name': 'Azure Monitor',
                'purpose': 'Monitoring and logging',
                'monthly_cost': 55
            }
        },
        CloudProvider.GCP: {
            'compute': {
                'name': 'Compute Engine / Cloud Run / Cloud Functions',
                'purpose': 'Application hosting and compute',
                'monthly_cost': 210
            },
            'database': {
                'name': 'Cloud SQL / Firestore',
                'purpose': 'Managed database services',
                'monthly_cost': 155
            },
            'storage': {
                'name': 'Cloud Storage',
                'purpose': 'Object storage',
                'monthly_cost': 52
            },
            'cache': {
                'name': 'Memorystore',
                'purpose': 'In-memory caching',
                'monthly_cost': 105
            },
            'queue': {
                'name': 'Pub/Sub',
                'purpose': 'Message queuing and pub/sub',
                'monthly_cost': 32
            },
            'cdn': {
                'name': 'Cloud CDN',
                'purpose': 'Content delivery network',
                'monthly_cost': 82
            },
            'monitoring': {
                'name': 'Cloud Monitoring',
                'purpose': 'Monitoring and logging',
                'monthly_cost': 52
            }
        }
    }
    
    def create_plan(
        self,
        directory: str,
        target_provider: CloudProvider,
        current_architecture: Optional[ArchitecturePattern] = None,
        include_cost_estimates: bool = False
    ) -> CloudMigrationPlan:
        """
        Create cloud migration plan.
        
        Args:
            directory: Directory to analyze
            target_provider: Target cloud provider
            current_architecture: Current architecture pattern
            include_cost_estimates: Whether to include cost estimates
            
        Returns:
            Cloud migration plan
        """
        logger.info(f"Creating cloud migration plan for {target_provider.value}")
        
        # Determine migration strategy
        strategy = self._determine_migration_strategy(current_architecture)
        
        # Recommend cloud services
        services = self._recommend_services(target_provider, current_architecture)
        
        # Determine containerization needs
        needs_containers = self._needs_containerization(current_architecture)
        container_strategy = self._recommend_container_strategy(
            target_provider, needs_containers
        )
        
        # Recommend IaC tool
        iac_tool = self._recommend_iac_tool(target_provider)
        
        # CI/CD recommendations
        cicd_recommendations = self._recommend_cicd(target_provider)
        
        # Security considerations
        security = self._identify_security_considerations(target_provider)
        
        # Compliance requirements
        compliance = self._identify_compliance_requirements()
        
        # Estimate migration time
        migration_weeks = self._estimate_migration_time(
            strategy, len(services), needs_containers
        )
        
        # Calculate costs
        migration_cost = 0
        monthly_cost = 0
        
        if include_cost_estimates:
            migration_cost = self._estimate_migration_cost(
                strategy, len(services), migration_weeks
            )
            monthly_cost = sum(s.estimated_cost_monthly for s in services)
        
        return CloudMigrationPlan(
            target_provider=target_provider,
            migration_strategy=strategy,
            recommended_services=services,
            containerization_needed=needs_containers,
            container_strategy=container_strategy,
            infrastructure_as_code=iac_tool,
            ci_cd_recommendations=cicd_recommendations,
            security_considerations=security,
            compliance_requirements=compliance,
            estimated_migration_weeks=migration_weeks,
            estimated_total_cost=migration_cost,
            monthly_operational_cost=monthly_cost
        )
    
    def _determine_migration_strategy(
        self,
        current_architecture: Optional[ArchitecturePattern]
    ) -> str:
        """Determine migration strategy."""
        if current_architecture == ArchitecturePattern.MONOLITH:
            return "Lift-and-shift initially, then re-architect to microservices"
        elif current_architecture == ArchitecturePattern.MICROSERVICES:
            return "Re-platform with containerization and orchestration"
        elif current_architecture == ArchitecturePattern.SERVERLESS:
            return "Direct migration to cloud serverless services"
        else:
            return "Hybrid approach: lift-and-shift with gradual modernization"
    
    def _recommend_services(
        self,
        provider: CloudProvider,
        current_architecture: Optional[ArchitecturePattern]
    ) -> List[CloudService]:
        """Recommend cloud services."""
        services = []
        service_map = self.CLOUD_SERVICES.get(provider, {})
        
        # Core compute service
        compute = service_map.get('compute', {})
        services.append(CloudService(
            service_name=compute.get('name', 'Compute Service'),
            provider=provider,
            purpose=compute.get('purpose', 'Application hosting'),
            current_equivalent='On-premise servers',
            migration_steps=[
                'Set up cloud account and networking',
                'Create compute instances or containers',
                'Deploy application',
                'Configure load balancing',
                'Set up auto-scaling'
            ],
            estimated_cost_monthly=compute.get('monthly_cost', 200),
            configuration_notes='Start with development environment, then staging, then production'
        ))
        
        # Database service
        database = service_map.get('database', {})
        services.append(CloudService(
            service_name=database.get('name', 'Database Service'),
            provider=provider,
            purpose=database.get('purpose', 'Managed database'),
            current_equivalent='Self-managed database',
            migration_steps=[
                'Choose appropriate database service',
                'Set up database instance',
                'Migrate schema',
                'Migrate data with minimal downtime',
                'Update application connection strings',
                'Set up backups and replication'
            ],
            estimated_cost_monthly=database.get('monthly_cost', 150),
            configuration_notes='Use read replicas for high availability'
        ))
        
        # Storage service
        storage = service_map.get('storage', {})
        services.append(CloudService(
            service_name=storage.get('name', 'Storage Service'),
            provider=provider,
            purpose=storage.get('purpose', 'Object storage'),
            current_equivalent='File system storage',
            migration_steps=[
                'Create storage buckets',
                'Migrate static assets',
                'Update application to use cloud storage',
                'Set up CDN integration',
                'Configure lifecycle policies'
            ],
            estimated_cost_monthly=storage.get('monthly_cost', 50),
            configuration_notes='Use appropriate storage classes for cost optimization'
        ))
        
        # Caching service
        cache = service_map.get('cache', {})
        services.append(CloudService(
            service_name=cache.get('name', 'Cache Service'),
            provider=provider,
            purpose=cache.get('purpose', 'In-memory caching'),
            current_equivalent='Local cache or Redis',
            migration_steps=[
                'Set up cache cluster',
                'Update application cache configuration',
                'Migrate cache data if needed',
                'Configure cache policies'
            ],
            estimated_cost_monthly=cache.get('monthly_cost', 100),
            configuration_notes='Use for session storage and frequently accessed data'
        ))
        
        # Message queue service
        queue = service_map.get('queue', {})
        services.append(CloudService(
            service_name=queue.get('name', 'Queue Service'),
            provider=provider,
            purpose=queue.get('purpose', 'Message queuing'),
            current_equivalent='RabbitMQ or similar',
            migration_steps=[
                'Create message queues',
                'Update application to use cloud queues',
                'Migrate queue consumers',
                'Set up dead letter queues',
                'Configure monitoring'
            ],
            estimated_cost_monthly=queue.get('monthly_cost', 30),
            configuration_notes='Use for asynchronous processing and service decoupling'
        ))
        
        # Monitoring service
        monitoring = service_map.get('monitoring', {})
        services.append(CloudService(
            service_name=monitoring.get('name', 'Monitoring Service'),
            provider=provider,
            purpose=monitoring.get('purpose', 'Monitoring and logging'),
            current_equivalent='Self-hosted monitoring',
            migration_steps=[
                'Set up monitoring dashboards',
                'Configure application logging',
                'Set up alerts and notifications',
                'Create custom metrics',
                'Configure log retention'
            ],
            estimated_cost_monthly=monitoring.get('monthly_cost', 50),
            configuration_notes='Essential for production operations'
        ))
        
        return services
    
    def _needs_containerization(
        self,
        current_architecture: Optional[ArchitecturePattern]
    ) -> bool:
        """Determine if containerization is needed."""
        return current_architecture in [
            ArchitecturePattern.MONOLITH,
            ArchitecturePattern.MICROSERVICES,
            ArchitecturePattern.LAYERED
        ]
    
    def _recommend_container_strategy(
        self,
        provider: CloudProvider,
        needs_containers: bool
    ) -> str:
        """Recommend container strategy."""
        if not needs_containers:
            return "Containerization not required for serverless architecture"
        
        strategies = {
            CloudProvider.AWS: "Use ECS with Fargate for serverless containers, or EKS for Kubernetes",
            CloudProvider.AZURE: "Use Azure Container Instances or AKS for Kubernetes",
            CloudProvider.GCP: "Use Cloud Run for serverless containers, or GKE for Kubernetes",
            CloudProvider.KUBERNETES: "Deploy to managed Kubernetes service",
            CloudProvider.DOCKER: "Use Docker Compose for development, Kubernetes for production"
        }
        
        return strategies.get(provider, "Containerize with Docker and orchestrate with Kubernetes")
    
    def _recommend_iac_tool(self, provider: CloudProvider) -> str:
        """Recommend Infrastructure as Code tool."""
        recommendations = {
            CloudProvider.AWS: "Terraform or AWS CloudFormation",
            CloudProvider.AZURE: "Terraform or Azure Resource Manager (ARM) templates",
            CloudProvider.GCP: "Terraform or Google Cloud Deployment Manager",
            CloudProvider.KUBERNETES: "Helm charts and Kustomize",
            CloudProvider.DOCKER: "Docker Compose and Terraform"
        }
        
        return recommendations.get(provider, "Terraform (cloud-agnostic)")
    
    def _recommend_cicd(self, provider: CloudProvider) -> List[str]:
        """Recommend CI/CD practices."""
        return [
            "Implement automated testing in CI pipeline",
            "Use blue-green or canary deployments",
            "Automate infrastructure provisioning",
            "Implement automated rollback mechanisms",
            "Use feature flags for gradual rollouts",
            f"Integrate with {provider.value} native CI/CD tools",
            "Set up automated security scanning",
            "Implement deployment approval workflows"
        ]
    
    def _identify_security_considerations(self, provider: CloudProvider) -> List[str]:
        """Identify security considerations."""
        return [
            "Implement least privilege access control (IAM)",
            "Enable encryption at rest and in transit",
            "Set up network segmentation with VPC/VNet",
            "Configure security groups and firewalls",
            "Enable audit logging and monitoring",
            "Implement secrets management",
            "Set up DDoS protection",
            "Regular security assessments and penetration testing",
            "Implement Web Application Firewall (WAF)",
            "Enable multi-factor authentication (MFA)"
        ]
    
    def _identify_compliance_requirements(self) -> List[str]:
        """Identify compliance requirements."""
        return [
            "Data residency and sovereignty requirements",
            "GDPR compliance for EU data",
            "HIPAA compliance for healthcare data",
            "PCI DSS for payment card data",
            "SOC 2 compliance for service providers",
            "Regular compliance audits",
            "Data backup and disaster recovery",
            "Incident response procedures"
        ]
    
    def _estimate_migration_time(
        self,
        strategy: str,
        service_count: int,
        needs_containers: bool
    ) -> float:
        """Estimate migration time in weeks."""
        base_weeks = 8  # Base migration time
        
        # Add time based on strategy
        if "re-architect" in strategy.lower():
            base_weeks += 8
        elif "re-platform" in strategy.lower():
            base_weeks += 4
        
        # Add time per service
        base_weeks += service_count * 1.5
        
        # Add time for containerization
        if needs_containers:
            base_weeks += 4
        
        return round(base_weeks, 1)
    
    def _estimate_migration_cost(
        self,
        strategy: str,
        service_count: int,
        migration_weeks: float
    ) -> float:
        """Estimate total migration cost."""
        # Assume team of 3 engineers at $150/hour
        hourly_rate = 150
        team_size = 3
        hours_per_week = 40
        
        labor_cost = migration_weeks * hours_per_week * team_size * hourly_rate
        
        # Add infrastructure costs during migration
        infrastructure_cost = migration_weeks * 500  # $500/week for dev/staging
        
        # Add training and consulting
        training_cost = 10000
        
        total = labor_cost + infrastructure_cost + training_cost
        
        return round(total, 2)


# Made with Bob