"""
Risk Analysis Engine - Usage Examples

This file demonstrates various ways to use the risk analysis engine.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.risk_analysis import RiskAnalyzer
from src.services.risk_analysis.risk_scorer import RiskTrendAnalyzer
from datetime import datetime
import json


def example_1_basic_analysis():
    """Example 1: Basic repository analysis"""
    print("=" * 60)
    print("Example 1: Basic Repository Analysis")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    # Analyze the backend directory
    result = analyzer.analyze(
        directory="./backend/src",
        file_patterns=["*.py"],
        include_tests=True,
        include_complexity=True,
        include_dependencies=True
    )
    
    # Print overall results
    print(f"\n📊 Overall Risk Score: {result.overall_risk_score.overall_score:.1f}")
    print(f"🎯 Risk Level: {result.overall_risk_score.risk_level.value.upper()}")
    print(f"📁 Files Analyzed: {result.summary['files_analyzed']}")
    print(f"\n⚠️  Issues Found:")
    print(f"   🔴 Critical: {result.overall_risk_score.critical_issues}")
    print(f"   🟠 High: {result.overall_risk_score.high_issues}")
    print(f"   🟡 Medium: {result.overall_risk_score.medium_issues}")
    print(f"   🔵 Low: {result.overall_risk_score.low_issues}")
    
    print(f"\n💡 Top Recommendations:")
    for i, rec in enumerate(result.overall_risk_score.recommendations[:5], 1):
        print(f"   {i}. {rec}")
    
    print("\n" + "=" * 60 + "\n")


def example_2_circular_dependencies():
    """Example 2: Focus on circular dependencies"""
    print("=" * 60)
    print("Example 2: Circular Dependency Detection")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=False,
        include_complexity=False,
        include_dependencies=True
    )
    
    if result.circular_dependencies:
        print(f"\n⚠️  Found {len(result.circular_dependencies)} circular dependencies:\n")
        
        for i, dep in enumerate(result.circular_dependencies, 1):
            print(f"{i}. Cycle Length: {dep.cycle_length}")
            print(f"   Risk Level: {dep.risk_level.value.upper()}")
            print(f"   Impact Score: {dep.impact_score:.1f}")
            print(f"   Description: {dep.description}")
            print(f"   Files involved:")
            for file in dep.cycle:
                print(f"      → {file}")
            print()
    else:
        print("\n✅ No circular dependencies found!")
    
    print("=" * 60 + "\n")


def example_3_risky_files():
    """Example 3: Identify risky files"""
    print("=" * 60)
    print("Example 3: Risky Files Detection")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=False,
        include_complexity=True,
        include_dependencies=False
    )
    
    if result.risky_files:
        print(f"\n🔍 Found {len(result.risky_files)} risky files\n")
        print("Top 10 Risky Files:")
        print("-" * 60)
        
        for i, file in enumerate(result.risky_files[:10], 1):
            print(f"\n{i}. {Path(file.file_path).name}")
            print(f"   Path: {file.file_path}")
            print(f"   Risk Score: {file.risk_score:.1f}/100")
            print(f"   Risk Level: {file.risk_level.value.upper()}")
            print(f"   Lines of Code: {file.lines_of_code}")
            print(f"   Complexity: {file.complexity_score:.1f}")
            print(f"   Risk Factors:")
            for factor in file.risk_factors:
                print(f"      • {factor}")
    else:
        print("\n✅ No high-risk files detected!")
    
    print("\n" + "=" * 60 + "\n")


def example_4_complexity_analysis():
    """Example 4: Code complexity analysis"""
    print("=" * 60)
    print("Example 4: Complexity Analysis")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=False,
        include_complexity=True,
        include_dependencies=False
    )
    
    if result.complexity_metrics:
        # Calculate statistics
        avg_cyclomatic = sum(c.cyclomatic_complexity for c in result.complexity_metrics) / len(result.complexity_metrics)
        avg_maintainability = sum(c.maintainability_index for c in result.complexity_metrics) / len(result.complexity_metrics)
        
        print(f"\n📊 Complexity Statistics:")
        print(f"   Average Cyclomatic Complexity: {avg_cyclomatic:.1f}")
        print(f"   Average Maintainability Index: {avg_maintainability:.1f}")
        
        # Find most complex files
        complex_files = sorted(
            result.complexity_metrics,
            key=lambda x: x.cyclomatic_complexity,
            reverse=True
        )[:5]
        
        print(f"\n🔥 Top 5 Most Complex Files:")
        print("-" * 60)
        
        for i, file in enumerate(complex_files, 1):
            print(f"\n{i}. {Path(file.file_path).name}")
            print(f"   Cyclomatic Complexity: {file.cyclomatic_complexity}")
            print(f"   Cognitive Complexity: {file.cognitive_complexity}")
            print(f"   Max Nesting Depth: {file.max_nesting_depth}")
            print(f"   Maintainability Index: {file.maintainability_index:.1f}")
            print(f"   Functions: {file.function_count}, Classes: {file.class_count}")
            
            if file.complex_functions:
                print(f"   Complex Functions:")
                for func in file.complex_functions[:3]:
                    print(f"      • {func['name']} (line {func['line']}, complexity: {func['complexity']})")
    
    print("\n" + "=" * 60 + "\n")


def example_5_test_coverage():
    """Example 5: Test coverage analysis"""
    print("=" * 60)
    print("Example 5: Test Coverage Analysis")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=True,
        include_complexity=False,
        include_dependencies=False
    )
    
    if result.test_coverage:
        # Calculate statistics
        total_files = len(result.test_coverage)
        files_with_tests = sum(1 for tc in result.test_coverage if tc.has_tests)
        avg_coverage = sum(tc.coverage_estimate for tc in result.test_coverage) / total_files
        
        print(f"\n📝 Test Coverage Statistics:")
        print(f"   Total Files: {total_files}")
        print(f"   Files with Tests: {files_with_tests} ({files_with_tests/total_files*100:.1f}%)")
        print(f"   Average Coverage: {avg_coverage:.1f}%")
        
        # Files without tests
        no_tests = [tc for tc in result.test_coverage if not tc.has_tests]
        
        if no_tests:
            print(f"\n⚠️  Files Without Tests ({len(no_tests)}):")
            print("-" * 60)
            
            for i, tc in enumerate(no_tests[:10], 1):
                print(f"{i}. {Path(tc.file_path).name}")
                print(f"   Path: {tc.file_path}")
                print(f"   Recommendation: {tc.recommendation}")
                if tc.untested_functions:
                    print(f"   Untested Functions: {', '.join(tc.untested_functions[:5])}")
                print()
    
    print("=" * 60 + "\n")


def example_6_single_file_analysis():
    """Example 6: Analyze a single file"""
    print("=" * 60)
    print("Example 6: Single File Analysis")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    # Analyze a specific file
    file_path = "./backend/src/api/app.py"
    
    if os.path.exists(file_path):
        result = analyzer.analyze_file(file_path)
        
        print(f"\n📄 File: {file_path}")
        print("-" * 60)
        
        if 'error' not in result:
            print(f"Functions: {result['functions']}")
            print(f"Classes: {result['classes']}")
            print(f"Imports: {result['imports']}")
            
            if result.get('complexity'):
                comp = result['complexity']
                print(f"\nComplexity Metrics:")
                print(f"   Cyclomatic Complexity: {comp['cyclomatic_complexity']}")
                print(f"   Cognitive Complexity: {comp['cognitive_complexity']}")
                print(f"   Maintainability Index: {comp['maintainability_index']:.1f}")
            
            if result.get('risk_assessment'):
                risk = result['risk_assessment']
                print(f"\nRisk Assessment:")
                print(f"   Risk Score: {risk['risk_score']:.1f}/100")
                print(f"   Risk Level: {risk['risk_level'].upper()}")
                print(f"   Risk Factors: {', '.join(risk['risk_factors'])}")
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"\n❌ File not found: {file_path}")
    
    print("\n" + "=" * 60 + "\n")


def example_7_visualization_data():
    """Example 7: Generate visualization data"""
    print("=" * 60)
    print("Example 7: Visualization Data Generation")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=True,
        include_complexity=True,
        include_dependencies=True
    )
    
    viz_data = analyzer.generate_visualization_data(result)
    
    print("\n📊 Visualization Data:")
    print("-" * 60)
    
    # Risk heatmap
    print(f"\n🗺️  Risk Heatmap ({len(viz_data['risk_heatmap']['files'])} files):")
    for file in viz_data['risk_heatmap']['files'][:5]:
        print(f"   {Path(file['path']).name}: {file['score']:.1f} ({file['level']})")
    
    # Complexity distribution
    dist = viz_data['complexity_distribution']
    print(f"\n📈 Complexity Distribution:")
    print(f"   Low: {dist['low']}")
    print(f"   Medium: {dist['medium']}")
    print(f"   High: {dist['high']}")
    print(f"   Very High: {dist['very_high']}")
    
    # Top risks
    print(f"\n⚠️  Top Risks:")
    for i, risk in enumerate(viz_data['top_risks'][:5], 1):
        print(f"   {i}. [{risk['severity'].upper()}] {risk['description']}")
        print(f"      Impact: {risk['impact']:.1f}")
    
    print("\n" + "=" * 60 + "\n")


def example_8_export_results():
    """Example 8: Export results to JSON"""
    print("=" * 60)
    print("Example 8: Export Results to JSON")
    print("=" * 60)
    
    analyzer = RiskAnalyzer()
    
    result = analyzer.analyze(
        directory="./backend/src",
        include_tests=True,
        include_complexity=True,
        include_dependencies=True
    )
    
    # Convert to dict for JSON serialization
    output = {
        'project_path': result.project_path,
        'analysis_timestamp': result.analysis_timestamp,
        'overall_risk_score': {
            'overall_score': result.overall_risk_score.overall_score,
            'risk_level': result.overall_risk_score.risk_level.value,
            'category_scores': result.overall_risk_score.category_scores,
            'critical_issues': result.overall_risk_score.critical_issues,
            'high_issues': result.overall_risk_score.high_issues,
            'medium_issues': result.overall_risk_score.medium_issues,
            'low_issues': result.overall_risk_score.low_issues,
            'recommendations': result.overall_risk_score.recommendations
        },
        'summary': result.summary
    }
    
    # Save to file
    output_file = "risk_analysis_report.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Results exported to: {output_file}")
    print(f"   File size: {os.path.getsize(output_file)} bytes")
    
    print("\n" + "=" * 60 + "\n")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("RISK ANALYSIS ENGINE - EXAMPLES")
    print("=" * 60 + "\n")
    
    try:
        example_1_basic_analysis()
        example_2_circular_dependencies()
        example_3_risky_files()
        example_4_complexity_analysis()
        example_5_test_coverage()
        example_6_single_file_analysis()
        example_7_visualization_data()
        example_8_export_results()
        
        print("\n✅ All examples completed successfully!\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

# Made with Bob
