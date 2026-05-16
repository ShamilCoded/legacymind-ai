"""
Scalability analyzer for identifying bottlenecks and optimization opportunities.
"""
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from .models import (
    ScalabilityAnalysis,
    BottleneckAnalysis,
    ModernizationPriority
)

logger = logging.getLogger(__name__)


class ScalabilityAnalyzer:
    """Analyzes code for scalability issues and optimization opportunities."""
    
    # Bottleneck patterns
    BOTTLENECK_PATTERNS = {
        'database': {
            'patterns': [r'SELECT \*', r'\.all\(\)', r'N\+1', r'\.query\('],
            'type': 'Database I/O',
            'severity': ModernizationPriority.HIGH
        },
        'synchronous': {
            'patterns': [r'\.get\(', r'requests\.', r'urllib', r'time\.sleep'],
            'type': 'Synchronous blocking',
            'severity': ModernizationPriority.MEDIUM
        },
        'loop': {
            'patterns': [r'for .+ in .+:\s+for', r'while .+:\s+while'],
            'type': 'Nested loops',
            'severity': ModernizationPriority.MEDIUM
        },
        'memory': {
            'patterns': [r'\.readlines\(\)', r'\.read\(\)', r'load.*all'],
            'type': 'Memory intensive',
            'severity': ModernizationPriority.MEDIUM
        }
    }
    
    def __init__(self):
        """Initialize scalability analyzer."""
        self.file_patterns = ['*.py', '*.js', '*.ts', '*.java', '*.go']
    
    def analyze(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> ScalabilityAnalysis:
        """
        Analyze code for scalability issues.
        
        Args:
            directory: Directory to analyze
            file_patterns: File patterns to include
            exclude_patterns: Patterns to exclude
            
        Returns:
            Scalability analysis results
        """
        logger.info(f"Analyzing {directory} for scalability issues")
        
        dir_path = Path(directory)
        patterns = file_patterns or self.file_patterns
        
        # Collect files
        files = self._collect_files(dir_path, patterns, exclude_patterns)
        
        # Identify bottlenecks
        bottlenecks = []
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_bottlenecks = self._identify_bottlenecks(file_path, content)
                bottlenecks.extend(file_bottlenecks)
            
            except Exception as e:
                logger.warning(f"Error analyzing {file_path}: {e}")
        
        # Generate recommendations
        caching_recommendations = self._recommend_caching(files, bottlenecks)
        database_optimization = self._recommend_database_optimization(bottlenecks)
        async_opportunities = self._identify_async_opportunities(bottlenecks)
        load_balancing = self._recommend_load_balancing()
        auto_scaling = self._recommend_auto_scaling()
        monitoring = self._recommend_monitoring()
        
        # Assess scalability
        horizontal_scalability = self._assess_horizontal_scalability(files, bottlenecks)
        vertical_scalability = self._assess_vertical_scalability(bottlenecks)
        
        # Calculate scalability score
        scalability_score = self._calculate_scalability_score(
            len(bottlenecks),
            len(files),
            horizontal_scalability,
            vertical_scalability
        )
        
        # Estimate capacity increase
        capacity_increase = self._estimate_capacity_increase(
            len(bottlenecks),
            len(caching_recommendations),
            len(async_opportunities)
        )
        
        return ScalabilityAnalysis(
            current_scalability_score=scalability_score,
            horizontal_scalability=horizontal_scalability,
            vertical_scalability=vertical_scalability,
            identified_bottlenecks=bottlenecks,
            caching_recommendations=caching_recommendations,
            database_optimization=database_optimization,
            async_processing_opportunities=async_opportunities,
            load_balancing_strategy=load_balancing,
            auto_scaling_recommendations=auto_scaling,
            performance_monitoring=monitoring,
            estimated_capacity_increase=capacity_increase
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
    
    def _identify_bottlenecks(
        self,
        file_path: Path,
        content: str
    ) -> List[BottleneckAnalysis]:
        """Identify performance bottlenecks in a file."""
        bottlenecks = []
        lines = content.split('\n')
        
        for category, config in self.BOTTLENECK_PATTERNS.items():
            for pattern in config['patterns']:
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        bottleneck = self._create_bottleneck(
                            file_path,
                            i,
                            category,
                            config['type'],
                            config['severity'],
                            line.strip()
                        )
                        bottlenecks.append(bottleneck)
        
        return bottlenecks
    
    def _create_bottleneck(
        self,
        file_path: Path,
        line_number: int,
        category: str,
        bottleneck_type: str,
        severity: ModernizationPriority,
        code_snippet: str
    ) -> BottleneckAnalysis:
        """Create bottleneck analysis."""
        descriptions = {
            'database': f"Potential database query inefficiency: {code_snippet[:50]}",
            'synchronous': f"Synchronous blocking operation: {code_snippet[:50]}",
            'loop': f"Nested loop detected: {code_snippet[:50]}",
            'memory': f"Memory-intensive operation: {code_snippet[:50]}"
        }
        
        impacts = {
            'database': "High latency under load, database connection exhaustion",
            'synchronous': "Thread blocking, reduced throughput",
            'loop': "CPU intensive, O(n²) or worse complexity",
            'memory': "High memory usage, potential OOM errors"
        }
        
        recommendations = {
            'database': "Use query optimization, indexing, connection pooling, and caching",
            'synchronous': "Convert to asynchronous operations or use background workers",
            'loop': "Optimize algorithm complexity, use better data structures",
            'memory': "Use streaming/chunking, implement pagination"
        }
        
        improvements = {
            'database': "50-90% latency reduction",
            'synchronous': "2-5x throughput increase",
            'loop': "10-100x performance improvement",
            'memory': "70-90% memory reduction"
        }
        
        return BottleneckAnalysis(
            location=f"{file_path}:{line_number}",
            type=bottleneck_type,
            severity=severity,
            description=descriptions.get(category, "Performance bottleneck detected"),
            impact=impacts.get(category, "Performance degradation under load"),
            recommendation=recommendations.get(category, "Optimize implementation"),
            estimated_improvement=improvements.get(category, "Significant improvement expected")
        )
    
    def _recommend_caching(
        self,
        files: List[Path],
        bottlenecks: List[BottleneckAnalysis]
    ) -> List[str]:
        """Recommend caching strategies."""
        recommendations = []
        
        # Check for database bottlenecks
        db_bottlenecks = [b for b in bottlenecks if 'database' in b.type.lower()]
        if db_bottlenecks:
            recommendations.extend([
                "Implement Redis/Memcached for frequently accessed data",
                "Use application-level caching for expensive queries",
                "Implement query result caching with TTL",
                "Cache database connection pools"
            ])
        
        # Check for API calls
        api_files = [f for f in files if 'api' in str(f).lower() or 'controller' in str(f).lower()]
        if api_files:
            recommendations.extend([
                "Implement HTTP response caching with ETags",
                "Use CDN for static assets",
                "Cache API responses at edge locations"
            ])
        
        # General recommendations
        recommendations.extend([
            "Implement multi-level caching strategy (L1: in-memory, L2: Redis)",
            "Use cache warming for predictable access patterns",
            "Implement cache invalidation strategy"
        ])
        
        return recommendations
    
    def _recommend_database_optimization(
        self,
        bottlenecks: List[BottleneckAnalysis]
    ) -> List[str]:
        """Recommend database optimizations."""
        db_bottlenecks = [b for b in bottlenecks if 'database' in b.type.lower()]
        
        if not db_bottlenecks:
            return ["Database performance appears adequate"]
        
        return [
            "Add indexes on frequently queried columns",
            "Optimize SELECT queries - avoid SELECT *",
            "Implement connection pooling",
            "Use read replicas for read-heavy workloads",
            "Implement database query caching",
            "Use batch operations instead of individual queries",
            "Implement database sharding for horizontal scaling",
            "Use materialized views for complex aggregations",
            "Optimize JOIN operations and query plans",
            "Implement query timeout and circuit breakers"
        ]
    
    def _identify_async_opportunities(
        self,
        bottlenecks: List[BottleneckAnalysis]
    ) -> List[str]:
        """Identify async processing opportunities."""
        sync_bottlenecks = [b for b in bottlenecks if 'synchronous' in b.type.lower()]
        
        opportunities = []
        
        if sync_bottlenecks:
            opportunities.extend([
                "Convert synchronous HTTP calls to async/await",
                "Use message queues for background processing",
                "Implement async database operations",
                "Use worker pools for CPU-intensive tasks"
            ])
        
        opportunities.extend([
            "Implement event-driven architecture",
            "Use async I/O for file operations",
            "Implement job queues (Celery, Bull, etc.)",
            "Use streaming for large data processing",
            "Implement webhook callbacks instead of polling"
        ])
        
        return opportunities
    
    def _recommend_load_balancing(self) -> str:
        """Recommend load balancing strategy."""
        return (
            "Implement load balancing strategy: "
            "Use Layer 7 (application) load balancer for HTTP/HTTPS traffic. "
            "Distribute traffic across multiple instances using round-robin or least-connections. "
            "Implement health checks and automatic failover. "
            "Use sticky sessions only when necessary. "
            "Consider geographic load balancing for global applications."
        )
    
    def _recommend_auto_scaling(self) -> List[str]:
        """Recommend auto-scaling strategies."""
        return [
            "Implement horizontal auto-scaling based on CPU/memory metrics",
            "Use predictive scaling for known traffic patterns",
            "Set up scale-out triggers at 70% resource utilization",
            "Configure scale-in with cooldown periods",
            "Use container orchestration (Kubernetes) for automatic scaling",
            "Implement application-level metrics for scaling decisions",
            "Set minimum and maximum instance limits",
            "Use spot/preemptible instances for cost optimization",
            "Implement gradual scale-out to avoid thundering herd",
            "Monitor scaling events and adjust thresholds"
        ]
    
    def _recommend_monitoring(self) -> List[str]:
        """Recommend performance monitoring."""
        return [
            "Implement APM (Application Performance Monitoring)",
            "Track key metrics: response time, throughput, error rate",
            "Set up distributed tracing for microservices",
            "Monitor database query performance",
            "Track memory and CPU utilization",
            "Implement real-user monitoring (RUM)",
            "Set up alerting for performance degradation",
            "Monitor cache hit rates and effectiveness",
            "Track API endpoint performance",
            "Implement log aggregation and analysis",
            "Use profiling tools to identify hotspots",
            "Monitor third-party service dependencies"
        ]
    
    def _assess_horizontal_scalability(
        self,
        files: List[Path],
        bottlenecks: List[BottleneckAnalysis]
    ) -> str:
        """Assess horizontal scalability."""
        issues = []
        
        # Check for state management
        state_files = [f for f in files if 'session' in str(f).lower() or 'state' in str(f).lower()]
        if state_files:
            issues.append("session state management")
        
        # Check for file system dependencies
        file_ops = [b for b in bottlenecks if 'file' in b.description.lower()]
        if file_ops:
            issues.append("file system dependencies")
        
        # Check for singleton patterns
        singleton_files = [f for f in files if 'singleton' in str(f).lower()]
        if singleton_files:
            issues.append("singleton patterns")
        
        if issues:
            return (
                f"Moderate horizontal scalability. Issues to address: {', '.join(issues)}. "
                "Recommend: externalize state, use distributed caching, implement stateless design."
            )
        else:
            return (
                "Good horizontal scalability potential. "
                "Application appears stateless and can scale across multiple instances."
            )
    
    def _assess_vertical_scalability(
        self,
        bottlenecks: List[BottleneckAnalysis]
    ) -> str:
        """Assess vertical scalability."""
        cpu_bottlenecks = [b for b in bottlenecks if 'cpu' in b.type.lower() or 'loop' in b.type.lower()]
        memory_bottlenecks = [b for b in bottlenecks if 'memory' in b.type.lower()]
        
        if cpu_bottlenecks and memory_bottlenecks:
            return (
                "Limited vertical scalability due to CPU and memory bottlenecks. "
                "Recommend: optimize algorithms, implement caching, use async processing."
            )
        elif cpu_bottlenecks:
            return (
                "CPU-bound operations limit vertical scalability. "
                "Recommend: optimize algorithms, use parallel processing, offload to workers."
            )
        elif memory_bottlenecks:
            return (
                "Memory-intensive operations limit vertical scalability. "
                "Recommend: implement streaming, use pagination, optimize data structures."
            )
        else:
            return (
                "Good vertical scalability potential. "
                "Can benefit from increased CPU and memory resources."
            )
    
    def _calculate_scalability_score(
        self,
        bottleneck_count: int,
        file_count: int,
        horizontal: str,
        vertical: str
    ) -> float:
        """Calculate scalability score (0-100)."""
        score = 100.0
        
        # Deduct for bottlenecks
        if file_count > 0:
            bottleneck_ratio = bottleneck_count / file_count
            score -= min(bottleneck_ratio * 50, 40)
        
        # Deduct for scalability issues
        if 'limited' in horizontal.lower() or 'limited' in vertical.lower():
            score -= 20
        elif 'moderate' in horizontal.lower() or 'moderate' in vertical.lower():
            score -= 10
        
        return max(0.0, min(100.0, round(score, 1)))
    
    def _estimate_capacity_increase(
        self,
        bottleneck_count: int,
        caching_count: int,
        async_count: int
    ) -> str:
        """Estimate capacity increase after optimizations."""
        if bottleneck_count == 0:
            return "Current capacity is adequate"
        
        # Estimate improvement factors
        base_improvement = 1.0
        
        if caching_count > 0:
            base_improvement *= 2.0  # 2x from caching
        
        if async_count > 0:
            base_improvement *= 1.5  # 1.5x from async
        
        if bottleneck_count > 5:
            base_improvement *= 1.3  # 1.3x from bottleneck fixes
        
        total_improvement = int((base_improvement - 1) * 100)
        
        return f"{total_improvement}% capacity increase expected after optimizations"


# Made with Bob