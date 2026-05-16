'use client';

import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  analyzeRepositoryRisk,
  getRiskVisualization,
  type RiskAnalysisResult,
  type RiskVisualization,
} from '@/lib/api/risk-analysis';

interface RiskDashboardProps {
  initialDirectory?: string;
}

export function RiskDashboard({ initialDirectory = '' }: RiskDashboardProps) {
  const [directory, setDirectory] = useState(initialDirectory);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RiskAnalysisResult | null>(null);
  const [visualization, setVisualization] = useState<RiskVisualization | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    if (!directory) {
      setError('Please enter a directory path');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const [analysisResult, vizData] = await Promise.all([
        analyzeRepositoryRisk({ directory }),
        getRiskVisualization({ directory }),
      ]);

      setResult(analysisResult);
      setVisualization(vizData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (level: string) => {
    switch (level) {
      case 'critical':
        return 'bg-red-500';
      case 'high':
        return 'bg-orange-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getRiskLevelBadge = (level: string) => {
    const colors = {
      critical: 'bg-red-100 text-red-800 border-red-300',
      high: 'bg-orange-100 text-orange-800 border-orange-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-blue-100 text-blue-800 border-blue-300',
      info: 'bg-gray-100 text-gray-800 border-gray-300',
    };

    return (
      <Badge className={colors[level as keyof typeof colors] || colors.info}>
        {level.toUpperCase()}
      </Badge>
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Risk Analysis Dashboard</h1>
          <p className="text-muted-foreground mt-2">
            Comprehensive code quality and risk assessment
          </p>
        </div>
      </div>

      {/* Input Section */}
      <Card className="p-6">
        <div className="flex gap-4">
          <Input
            placeholder="Enter repository path (e.g., ./backend/src)"
            value={directory}
            onChange={(e) => setDirectory(e.target.value)}
            className="flex-1"
          />
          <Button onClick={handleAnalyze} disabled={loading}>
            {loading ? 'Analyzing...' : 'Analyze'}
          </Button>
        </div>
        {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
      </Card>

      {/* Results */}
      {result && (
        <>
          {/* Overall Score */}
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold mb-2">Overall Risk Score</h2>
                <div className="flex items-center gap-4">
                  <div className="text-5xl font-bold">
                    {result.overall_risk_score.overall_score.toFixed(1)}
                  </div>
                  <div>{getRiskLevelBadge(result.overall_risk_score.risk_level)}</div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-muted-foreground mb-2">Issues Found</div>
                <div className="space-y-1">
                  <div className="flex items-center gap-2 justify-end">
                    <span className="text-red-600 font-semibold">
                      {result.overall_risk_score.critical_issues}
                    </span>
                    <span className="text-sm">Critical</span>
                  </div>
                  <div className="flex items-center gap-2 justify-end">
                    <span className="text-orange-600 font-semibold">
                      {result.overall_risk_score.high_issues}
                    </span>
                    <span className="text-sm">High</span>
                  </div>
                  <div className="flex items-center gap-2 justify-end">
                    <span className="text-yellow-600 font-semibold">
                      {result.overall_risk_score.medium_issues}
                    </span>
                    <span className="text-sm">Medium</span>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Category Scores */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Risk Categories</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {Object.entries(result.overall_risk_score.category_scores).map(
                ([category, score]) => (
                  <div key={category} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium capitalize">
                        {category.replace(/_/g, ' ')}
                      </span>
                      <span className="text-sm font-bold">{score.toFixed(1)}</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          score >= 70
                            ? 'bg-red-500'
                            : score >= 50
                            ? 'bg-orange-500'
                            : score >= 30
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                        }`}
                        style={{ width: `${score}%` }}
                      />
                    </div>
                  </div>
                )
              )}
            </div>
          </Card>

          {/* Recommendations */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Recommendations</h2>
            <ul className="space-y-2">
              {result.overall_risk_score.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-lg mt-0.5">{rec.split(' ')[0]}</span>
                  <span>{rec.substring(rec.indexOf(' ') + 1)}</span>
                </li>
              ))}
            </ul>
          </Card>

          {/* Risky Files */}
          {result.risky_files.length > 0 && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">
                Top Risky Files ({result.risky_files.length})
              </h2>
              <div className="space-y-3">
                {result.risky_files.slice(0, 10).map((file, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <div className="font-mono text-sm">{file.file_path}</div>
                      <div className="flex flex-wrap gap-2 mt-2">
                        {file.risk_factors.map((factor, i) => (
                          <Badge key={i} className="text-xs border border-gray-300">
                            {factor}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <div className="flex items-center gap-3 ml-4">
                      <div className="text-right">
                        <div className="text-2xl font-bold">{file.risk_score.toFixed(0)}</div>
                        <div className="text-xs text-muted-foreground">Risk Score</div>
                      </div>
                      {getRiskLevelBadge(file.risk_level)}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Circular Dependencies */}
          {result.circular_dependencies.length > 0 && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">
                Circular Dependencies ({result.circular_dependencies.length})
              </h2>
              <div className="space-y-3">
                {result.circular_dependencies.map((dep, idx) => (
                  <div key={idx} className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-semibold">Cycle Length: {dep.cycle_length}</span>
                      {getRiskLevelBadge(dep.risk_level)}
                    </div>
                    <p className="text-sm text-gray-700 mb-2">{dep.description}</p>
                    <div className="text-xs font-mono text-gray-600">
                      {dep.cycle.join(' → ')}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Complexity Distribution */}
          {visualization && (
            <Card className="p-6">
              <h2 className="text-xl font-semibold mb-4">Complexity Distribution</h2>
              <div className="grid grid-cols-4 gap-4">
                {Object.entries(visualization.complexity_distribution).map(([level, count]) => (
                  <div key={level} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-3xl font-bold">{count}</div>
                    <div className="text-sm text-muted-foreground capitalize mt-1">
                      {level.replace(/_/g, ' ')}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Summary Stats */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Analysis Summary</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold">{result.summary.files_analyzed}</div>
                <div className="text-sm text-muted-foreground mt-1">Files Analyzed</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold">{result.summary.total_issues}</div>
                <div className="text-sm text-muted-foreground mt-1">Total Issues</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold">
                  {result.summary.average_complexity?.toFixed(1) || 0}
                </div>
                <div className="text-sm text-muted-foreground mt-1">Avg Complexity</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold">
                  {result.summary.average_test_coverage?.toFixed(0) || 0}%
                </div>
                <div className="text-sm text-muted-foreground mt-1">Test Coverage</div>
              </div>
            </div>
          </Card>
        </>
      )}
    </div>
  );
}

// Made with Bob
