# AI Risk Analysis Engine

A comprehensive code quality and risk assessment system for repositories that detects potential issues, calculates risk scores, and provides actionable recommendations.

## Features

### 🔍 Detection Capabilities

1. **Circular Dependencies**
   - Detects dependency cycles in code
   - Calculates impact scores
   - Identifies files involved in cycles

2. **Dead Code Detection**
   - Finds unused functions and classes
   - Confidence scoring for each detection
   - Identifies potentially removable code

3. **Coupling Analysis**
   - Measures afferent and efferent coupling
   - Calculates instability metrics
   - Identifies highly coupled modules

4. **Test Coverage Analysis**
   - Estimates test coverage per file
   - Identifies untested functions
   - Suggests testing priorities

5. **Risky Files Detection**
   - Identifies files with multiple risk factors
   - Analyzes file size, complexity, and structure
   - Prioritizes refactoring candidates

6. **Complexity Analysis**
   - Calculates cyclomatic complexity
   - Measures cognitive complexity
   - Tracks maintainability index
   - Identifies complex functions

### 📊 Risk Scoring System

The engine uses a weighted scoring system across six categories:

- **Circular Dependencies** (25%): Impact of dependency cycles
- **Coupling** (20%): Module interdependencies
- **Test Coverage** (20%): Testing completeness
- **Risky Files** (15%): File-level risk factors
- **Complexity** (10%): Code complexity metrics
- **Dead Code** (10%): Unused code presence

**Risk Levels:**
- 🔴 **Critical** (80-100): Immediate attention required
- 🟠 **High** (60-79): High priority issues
- 🟡 **Medium** (40-59): Should be addressed
- 🔵 **Low** (20-39): Minor concerns
- ⚪ **Info** (0-19): Informational

## Installation

### Prerequisites

```bash
# Python 3.8+
pip install -r requirements.txt
```

### Dependencies

The risk analysis engine requires:
- `ast` (built-in): Python code parsing
- `pathlib` (built-in): File system operations
- `logging` (built-in): Logging functionality

## Usage

### Python API

```python
from src.services.risk_analysis import RiskAnalyzer

# Initialize analyzer
analyzer = RiskAnalyzer()

# Analyze a repository
result = analyzer.analyze(
    directory="./my-project",
    file_patterns=["*.py", "*.js", "*.ts"],
    exclude_patterns=["*/node_modules/*", "*/.git/*"],
    include_tests=True,
    include_complexity=True,
    include_dependencies=True
)

# Access results
print(f"Overall Risk Score: {result.overall_risk_score.overall_score}")
print(f"Risk Level: {result.overall_risk_score.risk_level}")
print(f"Critical Issues: {result.overall_risk_score.critical_issues}")

# Get recommendations
for rec in result.overall_risk_score.recommendations:
    print(f"- {rec}")

# Analyze circular dependencies
for dep in result.circular_dependencies:
    print(f"Cycle: {' -> '.join(dep.cycle)}")
    print(f"Impact: {dep.impact_score}")

# Check risky files
for file in result.risky_files:
    print(f"{file.file_path}: {file.risk_score}")
    print(f"Factors: {', '.join(file.risk_factors)}")
```

### REST API

#### Analyze Repository

```bash
POST /risk-analysis
Content-Type: application/json

{
  "directory": "./backend/src",
  "file_patterns": ["*.py"],
  "include_tests": true,
  "include_complexity": true,
  "include_dependencies": true
}
```

**Response:**

```json
{
  "project_path": "./backend/src",
  "analysis_timestamp": "2024-01-15T10:30:00",
  "overall_risk_score": {
    "overall_score": 45.2,
    "risk_level": "medium",
    "category_scores": {
      "circular_dependencies": 30.0,
      "dead_code": 15.5,
      "coupling": 55.0,
      "test_coverage": 40.0,
      "risky_files": 50.0,
      "complexity": 35.0
    },
    "critical_issues": 0,
    "high_issues": 3,
    "medium_issues": 12,
    "low_issues": 8,
    "recommendations": [
      "🔗 Reduce coupling by introducing interfaces",
      "📝 Add tests for 5 file(s) without coverage",
      "🔍 Refactor high-risk files: app.py, utils.py"
    ]
  },
  "circular_dependencies": [...],
  "risky_files": [...],
  "complexity_metrics": [...],
  "summary": {
    "files_analyzed": 45,
    "total_issues": 23,
    "average_complexity": 12.5,
    "average_test_coverage": 65.0
  }
}
```

#### Get Visualization Data

```bash
POST /risk-analysis/visualization
Content-Type: application/json

{
  "directory": "./backend/src"
}
```

#### Analyze Single File

```bash
GET /risk-analysis/file/{file_path}
```

#### Get Risk Summary

```bash
GET /risk-analysis/summary/{directory}
```

## Configuration

### File Patterns

Default patterns include:
- Python: `*.py`
- JavaScript/TypeScript: `*.js`, `*.ts`, `*.tsx`, `*.jsx`
- Documentation: `*.md`, `*.txt`

### Exclude Patterns

Default exclusions:
- `*/node_modules/*`
- `*/.git/*`
- `*/venv/*`
- `*/__pycache__/*`
- `*/dist/*`
- `*/build/*`

### Risk Thresholds

Customize risk level thresholds:

```python
# In risk_scorer.py
WEIGHTS = {
    'circular_dependencies': 0.25,
    'dead_code': 0.10,
    'coupling': 0.20,
    'test_coverage': 0.20,
    'risky_files': 0.15,
    'complexity': 0.10
}
```

## Detection Algorithms

### Circular Dependency Detection

Uses depth-first search (DFS) to find cycles in the dependency graph:

1. Build dependency graph from imports
2. Traverse graph using DFS with recursion stack
3. Detect back edges indicating cycles
4. Calculate impact based on cycle length

### Dead Code Detection

Identifies potentially unused code:

1. Build definition map (functions, classes)
2. Build usage map (imports, calls)
3. Find items with no references
4. Filter out exports and special methods
5. Assign confidence scores

### Coupling Analysis

Measures module interdependencies:

1. Count afferent coupling (Ca): incoming dependencies
2. Count efferent coupling (Ce): outgoing dependencies
3. Calculate instability: I = Ce / (Ce + Ca)
4. Score based on total coupling and instability

### Complexity Analysis

Calculates multiple complexity metrics:

1. **Cyclomatic Complexity**: Decision points + 1
2. **Cognitive Complexity**: Nesting-aware complexity
3. **Maintainability Index**: Simplified MI calculation
4. **Max Nesting Depth**: Maximum indentation level

## Examples

### Example 1: Quick Analysis

```python
from src.services.risk_analysis import RiskAnalyzer

analyzer = RiskAnalyzer()
result = analyzer.analyze("./my-project")

print(f"Risk Score: {result.overall_risk_score.overall_score}")
print(f"Issues: {result.overall_risk_score.critical_issues} critical, "
      f"{result.overall_risk_score.high_issues} high")
```

### Example 2: Focused Analysis

```python
# Analyze only dependencies and coupling
result = analyzer.analyze(
    directory="./backend",
    include_tests=False,
    include_complexity=False,
    include_dependencies=True
)

# Check for circular dependencies
if result.circular_dependencies:
    print("⚠️ Circular dependencies found!")
    for dep in result.circular_dependencies:
        print(f"  - {dep.description}")
```

### Example 3: File-Specific Analysis

```python
# Analyze a single file
file_result = analyzer.analyze_file("./src/app.py")

print(f"Complexity: {file_result['complexity']['cyclomatic_complexity']}")
print(f"Functions: {file_result['functions']}")
print(f"Risk Score: {file_result['risk_assessment']['risk_score']}")
```

### Example 4: Visualization Data

```python
result = analyzer.analyze("./project")
viz_data = analyzer.generate_visualization_data(result)

# Risk heatmap
for file in viz_data['risk_heatmap']['files']:
    print(f"{file['path']}: {file['score']} ({file['level']})")

# Complexity distribution
dist = viz_data['complexity_distribution']
print(f"Low: {dist['low']}, Medium: {dist['medium']}, "
      f"High: {dist['high']}, Very High: {dist['very_high']}")
```

## Frontend Integration

### React Component

```tsx
import { RiskDashboard } from '@/components/features/risk-analysis/RiskDashboard';

export default function RiskAnalysisPage() {
  return <RiskDashboard initialDirectory="./backend/src" />;
}
```

### API Client

```typescript
import { analyzeRepositoryRisk } from '@/lib/api/risk-analysis';

const result = await analyzeRepositoryRisk({
  directory: './backend/src',
  include_tests: true,
  include_complexity: true
});

console.log(`Risk Score: ${result.overall_risk_score.overall_score}`);
```

## Best Practices

### 1. Regular Analysis

Run risk analysis regularly (e.g., in CI/CD):

```bash
# In your CI pipeline
python -m src.services.risk_analysis.cli analyze ./src --output report.json
```

### 2. Set Thresholds

Fail builds on critical issues:

```python
result = analyzer.analyze("./src")
if result.overall_risk_score.critical_issues > 0:
    raise Exception("Critical risk issues found!")
```

### 3. Track Trends

Monitor risk scores over time:

```python
from src.services.risk_analysis.risk_scorer import RiskTrendAnalyzer

trend_analyzer = RiskTrendAnalyzer()
trend_analyzer.add_snapshot(result.overall_risk_score, datetime.now())

trend = trend_analyzer.get_trend(days=30)
print(f"Trend: {trend['trend']}, Change: {trend['change']}")
```

### 4. Prioritize Issues

Focus on high-impact issues first:

```python
# Sort by risk score
risky_files = sorted(
    result.risky_files,
    key=lambda x: x.risk_score,
    reverse=True
)

# Address top 5 risky files
for file in risky_files[:5]:
    print(f"Priority: {file.file_path} (score: {file.risk_score})")
```

## Troubleshooting

### Issue: No files found

**Solution:** Check file patterns and exclude patterns

```python
result = analyzer.analyze(
    directory="./src",
    file_patterns=["*.py"],  # Ensure correct patterns
    exclude_patterns=[]       # Remove overly broad exclusions
)
```

### Issue: High false positives in dead code

**Solution:** Dead code detection uses heuristics. Review confidence scores:

```python
# Filter by confidence
high_confidence_dead_code = [
    item for item in result.dead_code
    if item.confidence > 0.8
]
```

### Issue: Slow analysis on large repos

**Solution:** Limit scope or use parallel processing:

```python
# Analyze specific directories
result = analyzer.analyze(
    directory="./src/core",  # Smaller scope
    max_depth=3              # Limit depth
)
```

## Performance

- **Small projects** (<100 files): < 5 seconds
- **Medium projects** (100-500 files): 10-30 seconds
- **Large projects** (500+ files): 30-120 seconds

Optimize by:
- Excluding test directories if not needed
- Limiting file patterns
- Using specific directories

## Contributing

To add new detectors:

1. Create detector class in `detectors.py`
2. Implement `detect()` or `analyze()` method
3. Add to `RiskAnalyzer` orchestrator
4. Update risk scoring weights
5. Add tests

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- GitHub Issues: [repository-url]/issues
- Documentation: [docs-url]
- Email: support@example.com

---

**Made with Bob** 🤖