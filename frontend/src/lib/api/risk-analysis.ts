/**
 * API client for risk analysis endpoints
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RiskAnalysisRequest {
  directory: string;
  file_patterns?: string[];
  exclude_patterns?: string[];
  include_tests?: boolean;
  include_complexity?: boolean;
  include_dependencies?: boolean;
  max_depth?: number;
}

export interface RiskScore {
  overall_score: number;
  risk_level: 'critical' | 'high' | 'medium' | 'low' | 'info';
  category_scores: Record<string, number>;
  critical_issues: number;
  high_issues: number;
  medium_issues: number;
  low_issues: number;
  recommendations: string[];
}

export interface CircularDependency {
  cycle: string[];
  cycle_length: number;
  risk_level: string;
  impact_score: number;
  description: string;
}

export interface RiskyFile {
  file_path: string;
  risk_factors: string[];
  risk_score: number;
  risk_level: string;
  file_size: number;
  lines_of_code: number;
  complexity_score: number;
}

export interface ComplexityMetrics {
  file_path: string;
  cyclomatic_complexity: number;
  cognitive_complexity: number;
  max_nesting_depth: number;
  function_count: number;
  class_count: number;
  lines_of_code: number;
  complex_functions: Array<{
    name: string;
    line: number;
    complexity: number;
    args_count: number;
  }>;
  risk_level: string;
  maintainability_index: number;
}

export interface RiskAnalysisResult {
  project_path: string;
  analysis_timestamp: string;
  overall_risk_score: RiskScore;
  circular_dependencies: CircularDependency[];
  dead_code: any[];
  coupling_metrics: any[];
  test_coverage: any[];
  risky_files: RiskyFile[];
  complexity_metrics: ComplexityMetrics[];
  summary: Record<string, any>;
  metadata: Record<string, any>;
}

export interface RiskVisualization {
  risk_heatmap: {
    files: Array<{
      path: string;
      score: number;
      level: string;
    }>;
  };
  dependency_graph: Record<string, any>;
  complexity_distribution: {
    low: number;
    medium: number;
    high: number;
    very_high: number;
  };
  risk_trends: {
    current_score: number;
    risk_level: string;
  };
  top_risks: Array<{
    type: string;
    severity: string;
    description: string;
    impact: number;
    file?: string;
  }>;
}

/**
 * Analyze repository risk
 */
export async function analyzeRepositoryRisk(
  request: RiskAnalysisRequest
): Promise<RiskAnalysisResult> {
  const response = await fetch(`${API_BASE_URL}/risk-analysis`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Risk analysis failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get risk visualization data
 */
export async function getRiskVisualization(
  request: RiskAnalysisRequest
): Promise<RiskVisualization> {
  const response = await fetch(`${API_BASE_URL}/risk-analysis/visualization`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Failed to get visualization: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Analyze single file risk
 */
export async function analyzeFileRisk(filePath: string): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/risk-analysis/file/${encodeURIComponent(filePath)}`
  );

  if (!response.ok) {
    throw new Error(`File analysis failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get risk summary
 */
export async function getRiskSummary(directory: string): Promise<any> {
  const response = await fetch(
    `${API_BASE_URL}/risk-analysis/summary/${encodeURIComponent(directory)}`
  );

  if (!response.ok) {
    throw new Error(`Failed to get summary: ${response.statusText}`);
  }

  return response.json();
}

// Made with Bob
