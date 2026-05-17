'use client';

import { useState } from 'react';
import ArchitectureGraph from '@/components/features/architecture/ArchitectureGraph';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  generateArchitectureGraph,
  architectureQueryKeys,
  type ArchitectureGraphResponse,
} from '@/lib/api/architecture';

export default function ArchitecturePage() {
  const [directory, setDirectory] = useState('./backend/src');
  const [inputValue, setInputValue] = useState('./backend/src');
  const [selectedView, setSelectedView] = useState<'full' | 'modules' | 'layers'>('full');
  const [data, setData] = useState<ArchitectureGraphResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await generateArchitectureGraph(inputValue);
      setData(result);
      setDirectory(inputValue);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleNodeClick = (node: any) => {
    console.log('Node clicked:', node);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Architecture Visualization
          </h1>
          <p className="text-gray-600">
            Visualize your codebase architecture with interactive dependency graphs
          </p>
        </div>

        {/* Controls */}
        <Card className="p-6 space-y-4">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Directory Path
              </label>
              <Input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="./backend/src"
                className="w-full"
              />
            </div>
            <div className="flex items-end">
              <Button
                onClick={handleGenerate}
                disabled={isLoading}
                className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                {isLoading ? 'Generating...' : 'Generate Graph'}
              </Button>
            </div>
          </div>

          {/* View Selector */}
          <div className="flex gap-2">
            <span className="text-sm font-medium text-gray-700 self-center">View:</span>
            <Button
              variant={selectedView === 'full' ? 'primary' : 'outline'}
              onClick={() => setSelectedView('full')}
              size="sm"
            >
              Full Graph
            </Button>
            <Button
              variant={selectedView === 'modules' ? 'primary' : 'outline'}
              onClick={() => setSelectedView('modules')}
              size="sm"
            >
              By Modules
            </Button>
            <Button
              variant={selectedView === 'layers' ? 'primary' : 'outline'}
              onClick={() => setSelectedView('layers')}
              size="sm"
            >
              By Layers
            </Button>
          </div>
        </Card>

        {/* Error Display */}
        {error && (
          <Card className="p-4 bg-red-50 border-red-200">
            <div className="flex items-start gap-3">
              <span className="text-red-600 text-xl">⚠️</span>
              <div>
                <h3 className="font-semibold text-red-900">Error</h3>
                <p className="text-red-700 text-sm">
                  {error instanceof Error ? error.message : 'Failed to generate graph'}
                </p>
              </div>
            </div>
          </Card>
        )}

        {/* Graph Display */}
        {data && (
          <>
            {/* Metrics Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card className="p-4">
                <div className="text-sm text-gray-600">Total Files</div>
                <div className="text-2xl font-bold text-blue-600">
                  {data.metrics.total_nodes}
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-sm text-gray-600">Dependencies</div>
                <div className="text-2xl font-bold text-purple-600">
                  {data.metrics.total_edges}
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-sm text-gray-600">Avg Dependencies</div>
                <div className="text-2xl font-bold text-green-600">
                  {data.metrics.avg_dependencies.toFixed(1)}
                </div>
              </Card>
              <Card className="p-4">
                <div className="text-sm text-gray-600">Isolated Files</div>
                <div className="text-2xl font-bold text-orange-600">
                  {data.metrics.isolated_nodes}
                </div>
              </Card>
            </div>

            {/* Modules & Layers Info */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="p-4">
                <h3 className="font-semibold mb-3">Modules</h3>
                <div className="space-y-2">
                  {data.modules.slice(0, 5).map((module) => (
                    <div key={module.name} className="flex justify-between items-center">
                      <span className="text-sm">{module.name}</span>
                      <Badge>{module.file_count} files</Badge>
                    </div>
                  ))}
                </div>
              </Card>
              <Card className="p-4">
                <h3 className="font-semibold mb-3">Architecture Layers</h3>
                <div className="space-y-2">
                  {data.layers.map((layer) => (
                    <div key={layer.name} className="flex justify-between items-center">
                      <span className="text-sm">{layer.name}</span>
                      <Badge>{layer.file_count} files</Badge>
                    </div>
                  ))}
                </div>
              </Card>
            </div>

            {/* Graph Visualization */}
            <Card className="p-0 overflow-hidden">
              <div className="h-[600px]">
                <ArchitectureGraph data={data} onNodeClick={handleNodeClick} />
              </div>
            </Card>
          </>
        )}

        {/* Empty State */}
        {!data && !isLoading && !error && (
          <Card className="p-12 text-center">
            <div className="space-y-4">
              <div className="text-6xl">📊</div>
              <h3 className="text-xl font-semibold text-gray-700">
                No Graph Generated Yet
              </h3>
              <p className="text-gray-500">
                Enter a directory path and click &quot;Generate Graph&quot; to visualize your codebase
                architecture
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

// Made with Bob
