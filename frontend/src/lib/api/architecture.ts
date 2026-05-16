/**
 * Architecture visualization API client
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  path: string;
  functions: number;
  classes: number;
  imports: number;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
}

export interface GraphMetrics {
  total_nodes: number;
  total_edges: number;
  avg_dependencies: number;
  most_imported: Array<{ node_id: string; count: number }>;
  most_importing: Array<{ node_id: string; count: number }>;
  isolated_nodes: number;
}

export interface ArchitectureGraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  modules: Array<{
    name: string;
    files: string[];
    file_count: number;
  }>;
  layers: Array<{
    name: string;
    files: string[];
    file_count: number;
  }>;
  metrics: GraphMetrics;
  stats: Record<string, any>;
}

export interface DependencyTreeResponse {
  root: GraphNode | null;
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: Record<string, any>;
}

/**
 * Generate architecture graph for a directory
 */
export async function generateArchitectureGraph(
  directory: string,
  filePatterns?: string[],
  maxDepth?: number
): Promise<ArchitectureGraphResponse> {
  const response = await fetch(`${API_BASE_URL}/architecture/graph`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      directory,
      file_patterns: filePatterns,
      max_depth: maxDepth,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'Failed to generate architecture graph');
  }

  return response.json();
}

/**
 * Generate module-specific graph
 */
export async function generateModuleGraph(
  directory: string,
  modulePath: string
): Promise<{ nodes: GraphNode[]; edges: GraphEdge[]; stats: Record<string, any> }> {
  const response = await fetch(
    `${API_BASE_URL}/architecture/module-graph?directory=${encodeURIComponent(
      directory
    )}&module_path=${encodeURIComponent(modulePath)}`,
    {
      method: 'POST',
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'Failed to generate module graph');
  }

  return response.json();
}

/**
 * Generate API relationship graph
 */
export async function generateApiRelationships(
  directory: string
): Promise<{ nodes: GraphNode[]; edges: GraphEdge[]; stats: Record<string, any> }> {
  const response = await fetch(
    `${API_BASE_URL}/architecture/api-relationships?directory=${encodeURIComponent(directory)}`,
    {
      method: 'POST',
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'Failed to generate API relationships');
  }

  return response.json();
}

/**
 * Generate dependency tree for a specific file
 */
export async function generateDependencyTree(
  directory: string,
  targetFile: string
): Promise<DependencyTreeResponse> {
  const response = await fetch(`${API_BASE_URL}/architecture/dependency-tree`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      directory,
      target_file: targetFile,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || 'Failed to generate dependency tree');
  }

  return response.json();
}

/**
 * React Query hooks for architecture visualization
 */
export const architectureQueryKeys = {
  all: ['architecture'] as const,
  graph: (directory: string) => [...architectureQueryKeys.all, 'graph', directory] as const,
  module: (directory: string, modulePath: string) =>
    [...architectureQueryKeys.all, 'module', directory, modulePath] as const,
  api: (directory: string) => [...architectureQueryKeys.all, 'api', directory] as const,
  tree: (directory: string, targetFile: string) =>
    [...architectureQueryKeys.all, 'tree', directory, targetFile] as const,
};

// Made with Bob
