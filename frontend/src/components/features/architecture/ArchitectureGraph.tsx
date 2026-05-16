'use client';

import React, { useCallback, useEffect, useState } from 'react';
import ReactFlow, {
  Controls,
  Background,
  MiniMap,
} from 'reactflow';
import 'reactflow/dist/style.css';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  path: string;
  functions: number;
  classes: number;
  imports: number;
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  type: string;
  label?: string;
}

interface ArchitectureGraphProps {
  data: {
    nodes: GraphNode[];
    edges: GraphEdge[];
    metrics?: {
      total_nodes: number;
      total_edges: number;
      avg_dependencies: number;
    };
  };
  onNodeClick?: (node: any) => void;
}

const nodeColors: Record<string, string> = {
  python: '#3776ab',
  javascript: '#f7df1e',
  typescript: '#3178c6',
  'typescript-react': '#61dafb',
  'javascript-react': '#61dafb',
  unknown: '#6b7280',
};

export default function ArchitectureGraph({ data, onNodeClick }: ArchitectureGraphProps) {
  const [nodes, setNodes] = useState<any[]>([]);
  const [edges, setEdges] = useState<any[]>([]);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  // Convert data to React Flow format
  useEffect(() => {
    if (!data) return;

    // Create nodes with positions using circular layout
    const flowNodes = data.nodes.map((node, index) => {
      const angle = (index / data.nodes.length) * 2 * Math.PI;
      const radius = 300;
      
      return {
        id: node.id,
        type: 'default',
        data: node,
        position: {
          x: 400 + radius * Math.cos(angle),
          y: 300 + radius * Math.sin(angle),
        },
        style: {
          background: nodeColors[node.type] || nodeColors.unknown,
          color: 'white',
          border: '2px solid rgba(255, 255, 255, 0.3)',
          borderRadius: '8px',
          padding: '10px',
          fontSize: '12px',
          width: 180,
        },
      };
    });

    // Create edges
    const flowEdges = data.edges.map((edge) => ({
      id: edge.id,
      source: edge.source,
      target: edge.target,
      type: 'smoothstep',
      animated: edge.type === 'import',
      label: edge.label,
      labelStyle: { fontSize: 10, fill: '#6b7280' },
      style: { stroke: '#94a3b8', strokeWidth: 2 },
      markerEnd: {
        type: 'arrowclosed',
        color: '#94a3b8',
      },
    }));

    setNodes(flowNodes);
    setEdges(flowEdges);
  }, [data]);

  const handleNodeClick = useCallback(
    (_event: React.MouseEvent, node: any) => {
      setSelectedNode(node);
      onNodeClick?.(node);
    },
    [onNodeClick]
  );

  return (
    <div className="w-full h-full relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodeClick={handleNodeClick}
        fitView
        attributionPosition="bottom-left"
      >
        <Background color="#e2e8f0" gap={16} />
        <Controls />
        <MiniMap
          nodeColor={(node: any) => {
            const nodeType = node.data?.type || 'unknown';
            return nodeColors[nodeType] || nodeColors.unknown;
          }}
          maskColor="rgba(0, 0, 0, 0.1)"
        />
        
        {/* Stats Panel */}
        <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg z-10">
            <div className="space-y-2">
              <h3 className="font-semibold text-sm">Graph Statistics</h3>
              {data.metrics && (
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between gap-4">
                    <span className="text-gray-600">Nodes:</span>
                    <span className="font-medium">{data.metrics.total_nodes}</span>
                  </div>
                  <div className="flex justify-between gap-4">
                    <span className="text-gray-600">Edges:</span>
                    <span className="font-medium">{data.metrics.total_edges}</span>
                  </div>
                  <div className="flex justify-between gap-4">
                    <span className="text-gray-600">Avg Dependencies:</span>
                    <span className="font-medium">{data.metrics.avg_dependencies.toFixed(2)}</span>
                  </div>
                </div>
              )}
            </div>
        </div>

        {/* Legend Panel */}
        <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur-sm rounded-lg p-4 shadow-lg z-10">
            <div className="space-y-2">
              <h3 className="font-semibold text-sm">File Types</h3>
              <div className="space-y-1">
                {Object.entries(nodeColors).map(([type, color]) => (
                  <div key={type} className="flex items-center gap-2 text-xs">
                    <div
                      className="w-3 h-3 rounded"
                      style={{ backgroundColor: color }}
                    />
                    <span className="capitalize">{type.replace('-', ' ')}</span>
                  </div>
                ))}
              </div>
          </div>
        </div>
      </ReactFlow>

      {/* Selected Node Details */}
      {selectedNode && (
        <Card className="absolute top-4 left-4 p-4 max-w-sm bg-white/95 backdrop-blur-sm shadow-xl z-10">
          <div className="space-y-2">
            <div className="flex items-start justify-between">
              <h3 className="font-semibold text-sm">{selectedNode.data.label}</h3>
              <button
                onClick={() => setSelectedNode(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            <div className="space-y-1 text-xs">
              <div className="flex items-center gap-2">
                <Badge>{selectedNode.data.type}</Badge>
              </div>
              <div className="text-gray-600 break-all">{selectedNode.data.path}</div>
              <div className="pt-2 space-y-1">
                {selectedNode.data.functions > 0 && (
                  <div>Functions: {selectedNode.data.functions}</div>
                )}
                {selectedNode.data.classes > 0 && (
                  <div>Classes: {selectedNode.data.classes}</div>
                )}
                {selectedNode.data.imports > 0 && (
                  <div>Imports: {selectedNode.data.imports}</div>
                )}
              </div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}

// Made with Bob
