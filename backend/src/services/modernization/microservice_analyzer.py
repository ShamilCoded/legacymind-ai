"""
Microservice analyzer for monolith decomposition recommendations.
"""
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Set, Optional
from collections import defaultdict

from .models import (
    MicroserviceRecommendation,
    ServiceBoundary,
    ArchitecturePattern,
    MigrationComplexity,
    ModernizationPriority
)

logger = logging.getLogger(__name__)


class MicroserviceAnalyzer:
    """Analyzes monolithic applications for microservice decomposition."""
    
    # Common service patterns
    SERVICE_PATTERNS = {
        'auth': ['auth', 'login', 'user', 'account', 'session', 'token'],
        'payment': ['payment', 'billing', 'invoice', 'transaction', 'checkout'],
        'notification': ['notification', 'email', 'sms', 'alert', 'message'],
        'analytics': ['analytics', 'metrics', 'stats', 'report', 'dashboard'],
        'search': ['search', 'index', 'query', 'elasticsearch', 'solr'],
        'media': ['media', 'image', 'video', 'upload', 'storage', 'file'],
        'api': ['api', 'endpoint', 'route', 'controller'],
        'data': ['database', 'model', 'repository', 'dao', 'entity'],
        'service': ['service', 'business', 'logic', 'domain'],
        'integration': ['integration', 'external', 'third-party', 'webhook']
    }
    
    def __init__(self):
        """Initialize microservice analyzer."""
        self.file_patterns = ['*.py', '*.js', '*.ts', '*.java', '*.go']
    
    def analyze(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> MicroserviceRecommendation:
        """
        Analyze codebase for microservice opportunities.
        
        Args:
            directory: Directory to analyze
            file_patterns: File patterns to include
            exclude_patterns: Patterns to exclude
            
        Returns:
            Microservice recommendations
        """
        logger.info(f"Analyzing {directory} for microservice opportunities")
        
        dir_path = Path(directory)
        patterns = file_patterns or self.file_patterns
        
        # Collect all files
        files = self._collect_files(dir_path, patterns, exclude_patterns)
        
        # Detect current architecture
        current_arch = self._detect_architecture(files)
        
        # Analyze file structure and dependencies
        file_analysis = self._analyze_files(files)
        
        # Identify potential service boundaries
        services = self._identify_services(file_analysis)
        
        # Analyze service cohesion and coupling
        for service in services:
            service.cohesion_score = self._calculate_cohesion(service, file_analysis)
            service.coupling_score = self._calculate_coupling(service, services, file_analysis)
        
        # Determine if microservices are suitable
        is_suitable = self._is_suitable_for_microservices(
            len(files), services, file_analysis
        )
        
        # Recommend architecture
        recommended_arch = ArchitecturePattern.MICROSERVICES if is_suitable else current_arch
        
        # Identify shared components
        shared_components = self._identify_shared_components(services, file_analysis)
        
        # Recommend communication patterns
        communication_patterns = self._recommend_communication_patterns(services)
        
        # Recommend data management strategy
        data_strategy = self._recommend_data_strategy(services)
        
        # Assess migration complexity
        complexity = self._assess_migration_complexity(
            len(files), services, file_analysis
        )
        
        # Identify benefits and challenges
        benefits = self._identify_benefits(is_suitable, services)
        challenges = self._identify_challenges(services, file_analysis)
        
        # Estimate effort
        effort_weeks = self._estimate_migration_effort(
            len(files), services, complexity
        )
        
        return MicroserviceRecommendation(
            current_architecture=current_arch,
            recommended_architecture=recommended_arch,
            is_suitable_for_microservices=is_suitable,
            identified_services=services,
            shared_components=shared_components,
            communication_patterns=communication_patterns,
            data_management_strategy=data_strategy,
            migration_complexity=complexity,
            benefits=benefits,
            challenges=challenges,
            estimated_effort_weeks=effort_weeks
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
                # Check exclusions
                if any(re.search(ex, str(file_path)) for ex in exclude):
                    continue
                if file_path.is_file():
                    files.append(file_path)
        
        return files
    
    def _detect_architecture(self, files: List[Path]) -> ArchitecturePattern:
        """Detect current architecture pattern."""
        # Simple heuristics based on directory structure
        paths = [str(f) for f in files]
        
        # Check for microservices indicators
        if any('service' in p.lower() for p in paths):
            if len([p for p in paths if 'service' in p.lower()]) > 3:
                return ArchitecturePattern.MICROSERVICES
        
        # Check for serverless indicators
        if any('lambda' in p.lower() or 'function' in p.lower() for p in paths):
            return ArchitecturePattern.SERVERLESS
        
        # Check for layered architecture
        layers = ['controller', 'service', 'repository', 'model']
        if sum(1 for layer in layers if any(layer in p.lower() for p in paths)) >= 3:
            return ArchitecturePattern.LAYERED
        
        # Default to monolith
        return ArchitecturePattern.MONOLITH
    
    def _analyze_files(self, files: List[Path]) -> Dict[str, Any]:
        """Analyze files for structure and dependencies."""
        analysis = {
            'files': {},
            'dependencies': defaultdict(set),
            'entities': defaultdict(list),
            'endpoints': defaultdict(list)
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_key = str(file_path)
                
                # Extract imports/dependencies
                imports = self._extract_imports(content, file_path.suffix)
                analysis['dependencies'][file_key] = imports
                
                # Extract classes/entities
                classes = self._extract_classes(content, file_path.suffix)
                analysis['entities'][file_key] = classes
                
                # Extract API endpoints
                endpoints = self._extract_endpoints(content, file_path.suffix)
                analysis['endpoints'][file_key] = endpoints
                
                # Store file info
                analysis['files'][file_key] = {
                    'path': file_path,
                    'size': len(content),
                    'imports': len(imports),
                    'classes': len(classes),
                    'endpoints': len(endpoints)
                }
            
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
        
        return analysis
    
    def _extract_imports(self, content: str, suffix: str) -> Set[str]:
        """Extract import statements."""
        imports = set()
        
        if suffix == '.py':
            # Python imports
            for match in re.finditer(r'(?:from|import)\s+([\w.]+)', content):
                imports.add(match.group(1))
        
        elif suffix in ['.js', '.ts']:
            # JavaScript/TypeScript imports
            for match in re.finditer(r'import\s+.*?\s+from\s+[\'"](.+?)[\'"]', content):
                imports.add(match.group(1))
        
        elif suffix == '.java':
            # Java imports
            for match in re.finditer(r'import\s+([\w.]+);', content):
                imports.add(match.group(1))
        
        return imports
    
    def _extract_classes(self, content: str, suffix: str) -> List[str]:
        """Extract class definitions."""
        classes = []
        
        if suffix == '.py':
            for match in re.finditer(r'class\s+(\w+)', content):
                classes.append(match.group(1))
        
        elif suffix in ['.js', '.ts']:
            for match in re.finditer(r'class\s+(\w+)', content):
                classes.append(match.group(1))
        
        elif suffix == '.java':
            for match in re.finditer(r'(?:public|private|protected)?\s*class\s+(\w+)', content):
                classes.append(match.group(1))
        
        return classes
    
    def _extract_endpoints(self, content: str, suffix: str) -> List[str]:
        """Extract API endpoints."""
        endpoints = []
        
        if suffix == '.py':
            # Flask/FastAPI routes
            for match in re.finditer(r'@(?:app|router)\.\w+\([\'"](.+?)[\'"]\)', content):
                endpoints.append(match.group(1))
        
        elif suffix in ['.js', '.ts']:
            # Express routes
            for match in re.finditer(r'(?:app|router)\.\w+\([\'"](.+?)[\'"]\)', content):
                endpoints.append(match.group(1))
        
        return endpoints
    
    def _identify_services(self, file_analysis: Dict[str, Any]) -> List[ServiceBoundary]:
        """Identify potential service boundaries."""
        services = []
        
        # Group files by directory/module
        file_groups = defaultdict(list)
        for file_path in file_analysis['files'].keys():
            parts = Path(file_path).parts
            if len(parts) > 1:
                # Use second-level directory as grouping
                group = parts[1] if len(parts) > 2 else parts[0]
                file_groups[group].append(file_path)
        
        # Create service boundaries
        for group_name, group_files in file_groups.items():
            if len(group_files) < 2:
                continue
            
            # Determine service type
            service_type = self._classify_service(group_name, group_files, file_analysis)
            
            # Extract responsibilities
            responsibilities = self._extract_responsibilities(group_files, file_analysis)
            
            # Extract dependencies
            dependencies = self._extract_service_dependencies(
                group_files, file_groups, file_analysis
            )
            
            # Extract API endpoints
            endpoints = []
            for file_path in group_files:
                endpoints.extend(file_analysis['endpoints'].get(file_path, []))
            
            # Extract data entities
            entities = []
            for file_path in group_files:
                entities.extend(file_analysis['entities'].get(file_path, []))
            
            service = ServiceBoundary(
                name=f"{service_type.title()} Service" if service_type else group_name.title(),
                files=group_files,
                responsibilities=responsibilities,
                dependencies=dependencies,
                api_endpoints=endpoints,
                data_entities=entities,
                cohesion_score=0.0,  # Will be calculated later
                coupling_score=0.0   # Will be calculated later
            )
            
            services.append(service)
        
        return services
    
    def _classify_service(
        self,
        name: str,
        files: List[str],
        file_analysis: Dict[str, Any]
    ) -> str:
        """Classify service type based on patterns."""
        name_lower = name.lower()
        
        # Check against known patterns
        for service_type, keywords in self.SERVICE_PATTERNS.items():
            if any(keyword in name_lower for keyword in keywords):
                return service_type
        
        # Check file contents
        for file_path in files:
            file_lower = file_path.lower()
            for service_type, keywords in self.SERVICE_PATTERNS.items():
                if any(keyword in file_lower for keyword in keywords):
                    return service_type
        
        return 'business'
    
    def _extract_responsibilities(
        self,
        files: List[str],
        file_analysis: Dict[str, Any]
    ) -> List[str]:
        """Extract service responsibilities."""
        responsibilities = set()
        
        for file_path in files:
            # Add based on file name
            file_name = Path(file_path).stem
            if 'controller' in file_name.lower():
                responsibilities.add("Handle HTTP requests and responses")
            elif 'service' in file_name.lower():
                responsibilities.add("Implement business logic")
            elif 'repository' in file_name.lower() or 'dao' in file_name.lower():
                responsibilities.add("Manage data persistence")
            elif 'model' in file_name.lower() or 'entity' in file_name.lower():
                responsibilities.add("Define data models")
            
            # Add based on endpoints
            endpoints = file_analysis['endpoints'].get(file_path, [])
            if endpoints:
                responsibilities.add(f"Expose {len(endpoints)} API endpoints")
        
        return list(responsibilities) if responsibilities else ["Core business functionality"]
    
    def _extract_service_dependencies(
        self,
        service_files: List[str],
        all_groups: Dict[str, List[str]],
        file_analysis: Dict[str, Any]
    ) -> List[str]:
        """Extract dependencies on other services."""
        dependencies = set()
        
        for file_path in service_files:
            file_imports = file_analysis['dependencies'].get(file_path, set())
            
            # Check which other services are imported
            for group_name, group_files in all_groups.items():
                if any(imp in str(gf) for imp in file_imports for gf in group_files):
                    if not any(gf in service_files for gf in group_files):
                        dependencies.add(group_name.title())
        
        return list(dependencies)
    
    def _calculate_cohesion(
        self,
        service: ServiceBoundary,
        file_analysis: Dict[str, Any]
    ) -> float:
        """Calculate internal cohesion score (0-1)."""
        if len(service.files) < 2:
            return 1.0
        
        # Calculate based on shared dependencies
        all_imports = []
        for file_path in service.files:
            all_imports.extend(file_analysis['dependencies'].get(file_path, []))
        
        if not all_imports:
            return 0.5
        
        # Count shared imports
        from collections import Counter
        import_counts = Counter(all_imports)
        shared = sum(1 for count in import_counts.values() if count > 1)
        
        cohesion = shared / len(import_counts) if import_counts else 0.5
        return min(1.0, cohesion)
    
    def _calculate_coupling(
        self,
        service: ServiceBoundary,
        all_services: List[ServiceBoundary],
        file_analysis: Dict[str, Any]
    ) -> float:
        """Calculate external coupling score (0-1)."""
        if len(all_services) < 2:
            return 0.0
        
        # Count dependencies on other services
        external_deps = len(service.dependencies)
        max_possible = len(all_services) - 1
        
        coupling = external_deps / max_possible if max_possible > 0 else 0.0
        return min(1.0, coupling)
    
    def _is_suitable_for_microservices(
        self,
        file_count: int,
        services: List[ServiceBoundary],
        file_analysis: Dict[str, Any]
    ) -> bool:
        """Determine if codebase is suitable for microservices."""
        # Need sufficient size
        if file_count < 20:
            return False
        
        # Need clear service boundaries
        if len(services) < 3:
            return False
        
        # Check average cohesion
        avg_cohesion = sum(s.cohesion_score for s in services) / len(services)
        if avg_cohesion < 0.3:
            return False
        
        # Check coupling
        avg_coupling = sum(s.coupling_score for s in services) / len(services)
        if avg_coupling > 0.7:
            return False
        
        return True
    
    def _identify_shared_components(
        self,
        services: List[ServiceBoundary],
        file_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify shared components across services."""
        shared = []
        
        # Common utilities
        if any('util' in f.lower() for s in services for f in s.files):
            shared.append("Utility libraries")
        
        # Common models
        if any('model' in f.lower() for s in services for f in s.files):
            shared.append("Data models")
        
        # Authentication
        if any('auth' in f.lower() for s in services for f in s.files):
            shared.append("Authentication/Authorization")
        
        # Logging
        shared.append("Logging and monitoring")
        shared.append("Configuration management")
        
        return shared
    
    def _recommend_communication_patterns(
        self,
        services: List[ServiceBoundary]
    ) -> Dict[str, str]:
        """Recommend communication patterns."""
        return {
            'synchronous': 'REST APIs for request-response patterns',
            'asynchronous': 'Message queues (RabbitMQ/Kafka) for event-driven communication',
            'service_discovery': 'Service registry (Consul/Eureka) for dynamic discovery',
            'api_gateway': 'API Gateway for unified entry point and routing'
        }
    
    def _recommend_data_strategy(self, services: List[ServiceBoundary]) -> str:
        """Recommend data management strategy."""
        return (
            "Database per service pattern: Each microservice should own its data and database. "
            "Use event sourcing or saga pattern for distributed transactions. "
            "Consider CQRS for read-heavy services."
        )
    
    def _assess_migration_complexity(
        self,
        file_count: int,
        services: List[ServiceBoundary],
        file_analysis: Dict[str, Any]
    ) -> MigrationComplexity:
        """Assess migration complexity."""
        # Calculate complexity factors
        avg_coupling = sum(s.coupling_score for s in services) / len(services) if services else 0
        
        if file_count < 50 and len(services) <= 5 and avg_coupling < 0.3:
            return MigrationComplexity.SIMPLE
        elif file_count < 200 and len(services) <= 10 and avg_coupling < 0.5:
            return MigrationComplexity.MODERATE
        elif file_count < 500 and avg_coupling < 0.7:
            return MigrationComplexity.COMPLEX
        else:
            return MigrationComplexity.VERY_COMPLEX
    
    def _identify_benefits(
        self,
        is_suitable: bool,
        services: List[ServiceBoundary]
    ) -> List[str]:
        """Identify migration benefits."""
        if not is_suitable:
            return [
                "Current architecture is appropriate for the codebase size",
                "Lower operational complexity",
                "Simpler deployment process"
            ]
        
        return [
            "Independent deployment and scaling of services",
            "Technology diversity - use best tool for each service",
            "Improved fault isolation and resilience",
            "Faster development cycles with smaller, focused teams",
            "Better alignment with business domains",
            f"Clear service boundaries with {len(services)} identified services"
        ]
    
    def _identify_challenges(
        self,
        services: List[ServiceBoundary],
        file_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify migration challenges."""
        challenges = [
            "Increased operational complexity",
            "Need for robust service discovery and communication",
            "Distributed transaction management",
            "Data consistency across services",
            "Monitoring and debugging across services",
            "Network latency and reliability"
        ]
        
        # Add specific challenges
        high_coupling = [s for s in services if s.coupling_score > 0.6]
        if high_coupling:
            challenges.append(
                f"{len(high_coupling)} services have high coupling requiring careful refactoring"
            )
        
        return challenges
    
    def _estimate_migration_effort(
        self,
        file_count: int,
        services: List[ServiceBoundary],
        complexity: MigrationComplexity
    ) -> float:
        """Estimate migration effort in weeks."""
        base_effort = {
            MigrationComplexity.SIMPLE: 8,
            MigrationComplexity.MODERATE: 16,
            MigrationComplexity.COMPLEX: 32,
            MigrationComplexity.VERY_COMPLEX: 52
        }
        
        effort = base_effort[complexity]
        
        # Add effort per service
        effort += len(services) * 2
        
        # Add effort for file count
        effort += (file_count / 100) * 2
        
        return round(effort, 1)


# Made with Bob