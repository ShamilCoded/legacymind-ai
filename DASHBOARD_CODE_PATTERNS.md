# Dashboard Code Patterns & Templates

## 🎯 Quick Reference for Implementation

This document provides reusable code patterns and templates for building the dashboard components.

---

## 📦 Type Definitions Template

### Repository Types
```typescript
// frontend/src/types/repository.ts
export interface Repository {
  id: string;
  name: string;
  owner: string;
  url: string;
  description: string;
  stars: number;
  forks: number;
  language: string;
  size: number;
  lastUpdated: string;
  createdAt: string;
}

export interface RepositoryStats {
  totalFiles: number;
  totalLines: number;
  contributors: number;
  commits: number;
  branches: number;
  languages: Record<string, number>;
}
```

### Analysis Types
```typescript
// frontend/src/types/analysis.ts
export interface AnalysisResult {
  id: string;
  repositoryId: string;
  summary: string;
  insights: Insight[];
  metrics: AnalysisMetrics;
  completedAt: string;
}

export interface Insight {
  id: string;
  type: 'success' | 'warning' | 'info' | 'error';
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
}

export interface AnalysisMetrics {
  healthScore: number;
  codeQuality: number;
  maintainability: number;
  testCoverage: number;
}
```

### Architecture Types
```typescript
// frontend/src/types/architecture.ts
import { Node, Edge } from 'reactflow';

export interface ArchitectureData {
  nodes: ArchitectureNode[];
  edges: ArchitectureEdge[];
  layout: 'horizontal' | 'vertical';
}

export interface ArchitectureNode extends Node {
  data: {
    label: string;
    type: 'module' | 'class' | 'function' | 'file';
    files: number;
    lines: number;
    dependencies: string[];
    exports: string[];
  };
}

export interface ArchitectureEdge extends Edge {
  data: {
    type: 'import' | 'extends' | 'calls';
    weight: number;
  };
}
```

---

## 🎨 UI Component Patterns

### Animated Card Pattern
```typescript
// Pattern for creating animated stat cards
import { motion } from 'framer-motion';
import { Card, CardContent } from '@/components/ui/card';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  delay?: number;
}

export function StatCard({ title, value, icon: Icon, trend, delay = 0 }: StatCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay }}
    >
      <Card hover glow className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-primary opacity-10" />
        <CardContent className="relative p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-slate-400">{title}</p>
              <p className="text-3xl font-bold text-white mt-2">{value}</p>
              {trend && (
                <p className={`text-sm mt-1 ${trend.isPositive ? 'text-green-400' : 'text-red-400'}`}>
                  {trend.isPositive ? '↗' : '↘'} {Math.abs(trend.value)}%
                </p>
              )}
            </div>
            <div className="p-3 rounded-lg gradient-primary">
              <Icon className="w-6 h-6 text-white" />
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
```

### Collapsible Panel Pattern
```typescript
// Pattern for collapsible sections
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown } from 'lucide-react';

interface CollapsibleProps {
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

export function Collapsible({ title, children, defaultOpen = false }: CollapsibleProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="glass-card">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between p-4 text-left hover:bg-white/5 transition-colors"
      >
        <h3 className="text-lg font-semibold text-white">{title}</h3>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown className="w-5 h-5 text-slate-400" />
        </motion.div>
      </button>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="overflow-hidden"
          >
            <div className="p-4 pt-0">{children}</div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
```

### Tab Navigation Pattern
```typescript
// Pattern for tab navigation
import { motion } from 'framer-motion';

interface Tab {
  id: string;
  label: string;
  icon: LucideIcon;
}

interface TabNavigationProps {
  tabs: Tab[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
}

export function TabNavigation({ tabs, activeTab, onTabChange }: TabNavigationProps) {
  return (
    <div className="glass-card p-1 flex gap-1">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`
              relative flex items-center gap-2 px-4 py-2 rounded-lg
              transition-colors duration-200
              ${isActive ? 'text-white' : 'text-slate-400 hover:text-white'}
            `}
          >
            {isActive && (
              <motion.div
                layoutId="activeTab"
                className="absolute inset-0 gradient-primary rounded-lg"
                transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
              />
            )}
            <Icon className="w-4 h-4 relative z-10" />
            <span className="relative z-10 font-medium">{tab.label}</span>
          </button>
        );
      })}
    </div>
  );
}
```

---

## 🔄 Data Fetching Patterns

### Custom Hook Pattern
```typescript
// Pattern for data fetching hooks
import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api/client';

export function useRepository(repoId: string) {
  return useQuery({
    queryKey: ['repository', repoId],
    queryFn: () => api.getRepository(repoId),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 3,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
}

export function useAnalysis(repoId: string) {
  return useQuery({
    queryKey: ['analysis', repoId],
    queryFn: () => api.getAnalysis(repoId),
    staleTime: 10 * 60 * 1000, // 10 minutes
    enabled: !!repoId, // Only fetch if repoId exists
  });
}
```

### Loading State Pattern
```typescript
// Pattern for handling loading states
export function DataWrapper({ 
  isLoading, 
  error, 
  data, 
  children 
}: {
  isLoading: boolean;
  error: Error | null;
  data: any;
  children: (data: any) => React.ReactNode;
}) {
  if (isLoading) {
    return <LoadingSkeleton />;
  }

  if (error) {
    return (
      <ErrorState 
        message={error.message}
        onRetry={() => window.location.reload()}
      />
    );
  }

  if (!data) {
    return <EmptyState />;
  }

  return <>{children(data)}</>;
}
```

---

## 🎭 Animation Patterns

### Stagger Children Pattern
```typescript
// Pattern for staggered animations
import { motion } from 'framer-motion';

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

export function StaggeredList({ items }: { items: any[] }) {
  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      {items.map((item) => (
        <motion.div key={item.id} variants={item}>
          <ItemCard {...item} />
        </motion.div>
      ))}
    </motion.div>
  );
}
```

### Page Transition Pattern
```typescript
// Pattern for page/tab transitions
import { motion, AnimatePresence } from 'framer-motion';

export function TabContent({ activeTab, children }: { activeTab: string; children: React.ReactNode }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -20 }}
        transition={{ duration: 0.3 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

---

## 🎨 React Flow Patterns

### Basic Flow Setup
```typescript
// Pattern for React Flow setup
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap,
  useNodesState,
  useEdgesState,
} from 'reactflow';
import 'reactflow/dist/style.css';

export function ArchitectureFlow({ data }: { data: ArchitectureData }) {
  const [nodes, setNodes, onNodesChange] = useNodesState(data.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(data.edges);

  return (
    <div className="h-[600px] glass-card">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        className="bg-slate-900"
      >
        <Background color="#334155" gap={16} />
        <Controls className="glass-card" />
        <MiniMap 
          className="glass-card"
          nodeColor={(node) => {
            switch (node.data.type) {
              case 'module': return '#667eea';
              case 'class': return '#4facfe';
              case 'function': return '#43e97b';
              default: return '#94a3b8';
            }
          }}
        />
      </ReactFlow>
    </div>
  );
}
```

### Custom Node Pattern
```typescript
// Pattern for custom React Flow nodes
import { Handle, Position } from 'reactflow';

export function ModuleNode({ data }: { data: any }) {
  return (
    <div className="glass-card p-4 min-w-[200px]">
      <Handle type="target" position={Position.Top} />
      
      <div className="flex items-center gap-2 mb-2">
        <div className="w-8 h-8 rounded gradient-primary flex items-center justify-center">
          📦
        </div>
        <h4 className="font-semibold text-white">{data.label}</h4>
      </div>
      
      <div className="text-sm text-slate-400 space-y-1">
        <p>• {data.files} files</p>
        <p>• {data.lines.toLocaleString()} lines</p>
        <p>• {data.dependencies.length} dependencies</p>
      </div>
      
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}
```

---

## 📊 Chart Patterns

### Progress Bar Pattern
```typescript
// Pattern for animated progress bars
import { motion } from 'framer-motion';

interface ProgressBarProps {
  label: string;
  value: number;
  max?: number;
  color?: string;
}

export function ProgressBar({ label, value, max = 100, color = '#667eea' }: ProgressBarProps) {
  const percentage = (value / max) * 100;

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-slate-400">{label}</span>
        <span className="text-white font-medium">{percentage.toFixed(0)}%</span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${percentage}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className="h-full rounded-full"
          style={{ background: color }}
        />
      </div>
    </div>
  );
}
```

### Risk Matrix Pattern
```typescript
// Pattern for 2D risk matrix
interface RiskItem {
  id: string;
  title: string;
  impact: 'low' | 'high';
  probability: 'low' | 'high';
  severity: 'low' | 'medium' | 'high' | 'critical';
}

export function RiskMatrix({ risks }: { risks: RiskItem[] }) {
  const getQuadrant = (impact: string, probability: string) => {
    return risks.filter(r => r.impact === impact && r.probability === probability);
  };

  const severityColor = {
    low: 'bg-green-500',
    medium: 'bg-yellow-500',
    high: 'bg-orange-500',
    critical: 'bg-red-500',
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      {/* High Impact, Low Probability */}
      <div className="glass-card p-4">
        <h4 className="text-sm font-medium text-yellow-400 mb-2">Medium Risk</h4>
        {getQuadrant('high', 'low').map(risk => (
          <div key={risk.id} className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${severityColor[risk.severity]}`} />
            <span className="text-sm text-slate-300">{risk.title}</span>
          </div>
        ))}
      </div>

      {/* High Impact, High Probability */}
      <div className="glass-card p-4">
        <h4 className="text-sm font-medium text-red-400 mb-2">Critical Risk</h4>
        {getQuadrant('high', 'high').map(risk => (
          <div key={risk.id} className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${severityColor[risk.severity]}`} />
            <span className="text-sm text-slate-300">{risk.title}</span>
          </div>
        ))}
      </div>

      {/* Low Impact, Low Probability */}
      <div className="glass-card p-4">
        <h4 className="text-sm font-medium text-green-400 mb-2">Low Risk</h4>
        {getQuadrant('low', 'low').map(risk => (
          <div key={risk.id} className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${severityColor[risk.severity]}`} />
            <span className="text-sm text-slate-300">{risk.title}</span>
          </div>
        ))}
      </div>

      {/* Low Impact, High Probability */}
      <div className="glass-card p-4">
        <h4 className="text-sm font-medium text-yellow-400 mb-2">Medium Risk</h4>
        {getQuadrant('low', 'high').map(risk => (
          <div key={risk.id} className="flex items-center gap-2 mb-2">
            <div className={`w-2 h-2 rounded-full ${severityColor[risk.severity]}`} />
            <span className="text-sm text-slate-300">{risk.title}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 💬 Chat Patterns

### Message Component Pattern
```typescript
// Pattern for chat messages
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  codeSnippets?: CodeSnippet[];
}

export function ChatMessage({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`
        max-w-[80%] rounded-lg p-4
        ${isUser 
          ? 'gradient-primary text-white' 
          : 'glass-card text-slate-200'
        }
      `}>
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        
        {message.codeSnippets?.map((snippet, i) => (
          <CodeSnippet key={i} {...snippet} />
        ))}
        
        <p className="text-xs opacity-60 mt-2">
          {new Date(message.timestamp).toLocaleTimeString()}
        </p>
      </div>
    </motion.div>
  );
}
```

### Code Snippet Pattern
```typescript
// Pattern for syntax-highlighted code
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Copy, Check } from 'lucide-react';
import { useState } from 'react';

interface CodeSnippetProps {
  code: string;
  language: string;
  filename?: string;
}

export function CodeSnippet({ code, language, filename }: CodeSnippetProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-3 rounded-lg overflow-hidden glass-card">
      {filename && (
        <div className="flex items-center justify-between px-4 py-2 border-b border-slate-700">
          <span className="text-xs text-slate-400">{filename}</span>
          <button
            onClick={handleCopy}
            className="text-slate-400 hover:text-white transition-colors"
          >
            {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      )}
      <SyntaxHighlighter
        language={language}
        style={vscDarkPlus}
        customStyle={{
          margin: 0,
          padding: '1rem',
          background: 'transparent',
        }}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}
```

---

## 🎯 Utility Patterns

### Format Utilities
```typescript
// frontend/src/lib/utils/format.ts
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}

export function formatDate(date: string): string {
  const now = new Date();
  const then = new Date(date);
  const diffMs = now.getTime() - then.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 30) return `${diffDays}d ago`;
  return then.toLocaleDateString();
}

export function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(1)} ${sizes[i]}`;
}
```

### Validation Utilities
```typescript
// frontend/src/lib/utils/validation.ts
export function isValidGitHubUrl(url: string): boolean {
  const pattern = /^https?:\/\/(www\.)?github\.com\/[\w-]+\/[\w.-]+\/?$/;
  return pattern.test(url);
}

export function extractRepoInfo(url: string): { owner: string; repo: string } | null {
  const match = url.match(/github\.com\/([\w-]+)\/([\w.-]+)/);
  if (!match) return null;
  return { owner: match[1], repo: match[2] };
}
```

---

## 🔧 Configuration Patterns

### API Client Setup
```typescript
// frontend/src/lib/api/client.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const api = {
  getRepository: (id: string) => apiClient.get(`/repositories/${id}`),
  getAnalysis: (id: string) => apiClient.get(`/repositories/${id}/analysis`),
  getArchitecture: (id: string) => apiClient.get(`/repositories/${id}/architecture`),
  getDependencies: (id: string) => apiClient.get(`/repositories/${id}/dependencies`),
  getRisks: (id: string) => apiClient.get(`/repositories/${id}/risks`),
  getModernization: (id: string) => apiClient.get(`/repositories/${id}/modernization`),
  sendChatMessage: (id: string, message: string) => 
    apiClient.post(`/repositories/${id}/chat`, { message }),
};
```

---

## 📱 Responsive Patterns

### Responsive Grid Pattern
```typescript
// Pattern for responsive layouts
export function ResponsiveGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="
      grid gap-4
      grid-cols-1
      sm:grid-cols-2
      lg:grid-cols-3
      xl:grid-cols-4
    ">
      {children}
    </div>
  );
}
```

### Mobile Detection Pattern
```typescript
// Pattern for mobile-specific behavior
import { useEffect, useState } from 'react';

export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return isMobile;
}
```

---

*Use these patterns as templates during implementation*
*Customize as needed for specific requirements*