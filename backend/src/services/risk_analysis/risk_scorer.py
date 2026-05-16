"""
Risk scoring and aggregation system.
"""
from typing import Dict, List, Any
from datetime import datetime

from .models import (
    RiskScore, RiskLevel, CircularDependency, DeadCodeItem,
    CouplingMetrics, TestCoverageReport, RiskyFile, ComplexityMetrics
)


class RiskScorer:
    """Calculate and aggregate risk scores."""
    
    # Weight factors for different risk categories
    WEIGHTS = {
        'circular_dependencies': 0.25,
        'dead_code': 0.10,
        'coupling': 0.20,
        'test_coverage': 0.20,
        'risky_files': 0.15,
        'complexity': 0.10
    }
    
    def calculate_overall_score(
        self,
        circular_deps: List[CircularDependency],
        dead_code: List[DeadCodeItem],
        coupling: List[CouplingMetrics],
        test_coverage: List[TestCoverageReport],
        risky_files: List[RiskyFile],
        complexity: List[ComplexityMetrics]
    ) -> RiskScore:
        """
        Calculate overall risk score from all analysis results.
        
        Args:
            circular_deps: Circular dependency results
            dead_code: Dead code results
            coupling: Coupling metrics
            test_coverage: Test coverage reports
            risky_files: Risky file results
            complexity: Complexity metrics
            
        Returns:
            Overall risk score
        """
        # Calculate category scores
        category_scores = {
            'circular_dependencies': self._score_circular_deps(circular_deps),
            'dead_code': self._score_dead_code(dead_code),
            'coupling': self._score_coupling(coupling),
            'test_coverage': self._score_test_coverage(test_coverage),
            'risky_files': self._score_risky_files(risky_files),
            'complexity': self._score_complexity(complexity)
        }
        
        # Calculate weighted overall score
        overall_score = sum(
            score * self.WEIGHTS[category]
            for category, score in category_scores.items()
        )
        
        # Count issues by severity
        critical_issues = self._count_issues(
            [circular_deps, dead_code, coupling, test_coverage, risky_files, complexity],
            RiskLevel.CRITICAL
        )
        high_issues = self._count_issues(
            [circular_deps, dead_code, coupling, test_coverage, risky_files, complexity],
            RiskLevel.HIGH
        )
        medium_issues = self._count_issues(
            [circular_deps, dead_code, coupling, test_coverage, risky_files, complexity],
            RiskLevel.MEDIUM
        )
        low_issues = self._count_issues(
            [circular_deps, dead_code, coupling, test_coverage, risky_files, complexity],
            RiskLevel.LOW
        )
        
        # Determine overall risk level
        if overall_score >= 80 or critical_issues > 0:
            risk_level = RiskLevel.CRITICAL
        elif overall_score >= 60 or high_issues > 5:
            risk_level = RiskLevel.HIGH
        elif overall_score >= 40 or medium_issues > 10:
            risk_level = RiskLevel.MEDIUM
        elif overall_score >= 20:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.INFO
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            category_scores,
            critical_issues,
            high_issues,
            circular_deps,
            test_coverage,
            risky_files
        )
        
        return RiskScore(
            overall_score=round(overall_score, 1),
            risk_level=risk_level,
            category_scores=category_scores,
            critical_issues=critical_issues,
            high_issues=high_issues,
            medium_issues=medium_issues,
            low_issues=low_issues,
            recommendations=recommendations
        )
    
    def _score_circular_deps(self, circular_deps: List[CircularDependency]) -> float:
        """Score circular dependencies (0-100, higher is worse)."""
        if not circular_deps:
            return 0.0
        
        # Weight by impact score
        total_impact = sum(dep.impact_score for dep in circular_deps)
        avg_impact = total_impact / len(circular_deps)
        
        # Penalize multiple cycles
        cycle_penalty = min(len(circular_deps) * 10, 50)
        
        return min(avg_impact + cycle_penalty, 100)
    
    def _score_dead_code(self, dead_code: List[DeadCodeItem]) -> float:
        """Score dead code (0-100, higher is worse)."""
        if not dead_code:
            return 0.0
        
        # Weight by confidence
        weighted_count = sum(item.confidence for item in dead_code)
        
        # Scale to 0-100
        score = min(weighted_count * 5, 100)
        
        return score
    
    def _score_coupling(self, coupling: List[CouplingMetrics]) -> float:
        """Score coupling metrics (0-100, higher is worse)."""
        if not coupling:
            return 0.0
        
        # Average coupling score
        avg_coupling = sum(c.coupling_score for c in coupling) / len(coupling)
        
        # Count high coupling files
        high_coupling = sum(1 for c in coupling if c.coupling_score >= 60)
        high_coupling_penalty = min(high_coupling * 5, 30)
        
        return min(avg_coupling + high_coupling_penalty, 100)
    
    def _score_test_coverage(self, test_coverage: List[TestCoverageReport]) -> float:
        """Score test coverage (0-100, higher is worse)."""
        if not test_coverage:
            return 50.0  # No coverage data is medium risk
        
        # Calculate average coverage
        avg_coverage = sum(tc.coverage_estimate for tc in test_coverage) / len(test_coverage)
        
        # Invert score (low coverage = high risk)
        score = 100 - avg_coverage
        
        # Count files without tests
        no_tests = sum(1 for tc in test_coverage if not tc.has_tests)
        no_tests_penalty = min(no_tests * 2, 30)
        
        return min(score + no_tests_penalty, 100)
    
    def _score_risky_files(self, risky_files: List[RiskyFile]) -> float:
        """Score risky files (0-100, higher is worse)."""
        if not risky_files:
            return 0.0
        
        # Average risk score
        avg_risk = sum(rf.risk_score for rf in risky_files) / len(risky_files)
        
        # Count critical files
        critical_files = sum(1 for rf in risky_files if rf.risk_level == RiskLevel.CRITICAL)
        critical_penalty = min(critical_files * 10, 40)
        
        return min(avg_risk + critical_penalty, 100)
    
    def _score_complexity(self, complexity: List[ComplexityMetrics]) -> float:
        """Score complexity metrics (0-100, higher is worse)."""
        if not complexity:
            return 0.0
        
        # Average maintainability index (inverted)
        avg_maintainability = sum(c.maintainability_index for c in complexity) / len(complexity)
        score = 100 - avg_maintainability
        
        # Count high complexity files
        high_complexity = sum(1 for c in complexity if c.cyclomatic_complexity > 30)
        complexity_penalty = min(high_complexity * 5, 30)
        
        return min(score + complexity_penalty, 100)
    
    def _count_issues(self, result_lists: List[List[Any]], risk_level: RiskLevel) -> int:
        """Count issues of a specific risk level."""
        count = 0
        for results in result_lists:
            for item in results:
                if hasattr(item, 'risk_level') and item.risk_level == risk_level:
                    count += 1
        return count
    
    def _generate_recommendations(
        self,
        category_scores: Dict[str, float],
        critical_issues: int,
        high_issues: int,
        circular_deps: List[CircularDependency],
        test_coverage: List[TestCoverageReport],
        risky_files: List[RiskyFile]
    ) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []
        
        # Critical issues first
        if critical_issues > 0:
            recommendations.append(f"🚨 Address {critical_issues} critical issue(s) immediately")
        
        # Circular dependencies
        if category_scores['circular_dependencies'] >= 60:
            recommendations.append(
                f"⚠️ Break {len(circular_deps)} circular dependency cycle(s) to improve maintainability"
            )
        
        # Test coverage
        if category_scores['test_coverage'] >= 60:
            no_tests = sum(1 for tc in test_coverage if not tc.has_tests)
            if no_tests > 0:
                recommendations.append(
                    f"📝 Add tests for {no_tests} file(s) without test coverage"
                )
        
        # Risky files
        if category_scores['risky_files'] >= 60:
            top_risky = sorted(risky_files, key=lambda x: x.risk_score, reverse=True)[:3]
            if top_risky:
                recommendations.append(
                    f"🔍 Refactor high-risk files: {', '.join([rf.file_path.split('/')[-1] for rf in top_risky])}"
                )
        
        # Coupling
        if category_scores['coupling'] >= 60:
            recommendations.append(
                "🔗 Reduce coupling by introducing interfaces and dependency injection"
            )
        
        # Complexity
        if category_scores['complexity'] >= 60:
            recommendations.append(
                "📊 Simplify complex functions and reduce nesting depth"
            )
        
        # Dead code
        if category_scores['dead_code'] >= 40:
            recommendations.append(
                "🧹 Remove unused code to improve maintainability"
            )
        
        # General recommendations
        if high_issues > 10:
            recommendations.append(
                f"⚡ Prioritize fixing {high_issues} high-severity issues"
            )
        
        if not recommendations:
            recommendations.append("✅ Code quality is good. Continue maintaining best practices.")
        
        return recommendations[:8]  # Limit to top 8 recommendations


class RiskTrendAnalyzer:
    """Analyze risk trends over time."""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
    
    def add_snapshot(self, risk_score: RiskScore, timestamp: datetime):
        """Add a risk score snapshot."""
        self.history.append({
            'timestamp': timestamp.isoformat(),
            'overall_score': risk_score.overall_score,
            'risk_level': risk_score.risk_level.value,
            'category_scores': risk_score.category_scores,
            'critical_issues': risk_score.critical_issues,
            'high_issues': risk_score.high_issues
        })
    
    def get_trend(self, days: int = 30) -> Dict[str, Any]:
        """Get risk trend for the last N days."""
        if not self.history:
            return {'trend': 'stable', 'change': 0, 'data': []}
        
        recent = self.history[-days:] if len(self.history) > days else self.history
        
        if len(recent) < 2:
            return {'trend': 'stable', 'change': 0, 'data': recent}
        
        # Calculate trend
        first_score = recent[0]['overall_score']
        last_score = recent[-1]['overall_score']
        change = last_score - first_score
        
        if change > 10:
            trend = 'increasing'
        elif change < -10:
            trend = 'decreasing'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change': round(change, 1),
            'data': recent,
            'average': round(sum(s['overall_score'] for s in recent) / len(recent), 1)
        }
    
    def get_category_trends(self) -> Dict[str, Dict[str, Any]]:
        """Get trends for each risk category."""
        if not self.history:
            return {}
        
        trends = {}
        categories = self.history[0]['category_scores'].keys()
        
        for category in categories:
            scores = [h['category_scores'][category] for h in self.history]
            
            if len(scores) >= 2:
                change = scores[-1] - scores[0]
                trend = 'increasing' if change > 5 else 'decreasing' if change < -5 else 'stable'
            else:
                change = 0
                trend = 'stable'
            
            trends[category] = {
                'trend': trend,
                'change': round(change, 1),
                'current': scores[-1] if scores else 0,
                'average': round(sum(scores) / len(scores), 1) if scores else 0
            }
        
        return trends

# Made with Bob
