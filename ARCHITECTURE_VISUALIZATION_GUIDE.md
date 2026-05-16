# Architecture Visualization System - Complete Guide

## Overview

The Architecture Visualization System for LegacyMind AI provides interactive dependency graphs and architecture analysis for codebases. It parses code files, analyzes dependencies, and generates visual representations using React Flow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Architecture Page (/architecture)                    │  │
│  │  - User input for directory path                      │  │
│  │  - Graph controls and filters                         │  │
│  │  - Metrics display                                    │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  ArchitectureGraph Component (React Flow)            │  │
│  │  - Interactive node-edge visualization               │  │
│  │  - Node details on click                             │  │
│  │  - Minimap and controls                              │  │
│  └────────────────┬─────────────────────────────────────┘  │
│                   │                                          │
│  ┌────────────────▼─────────────────────────────────────┐  │
│  │  API Client (architecture.ts)                        │  │
│  │  - generateArchitectureGraph()                       │  │
│  │  - generateModuleGraph()                             │  │
│  │  - generateApiRelationships()                        │  │
│  │  - generateDependencyTree()                          │  │
│  └────────────────┬─────────────────────────────────────┘  │
└────────────────────┼─────────────────────────────────────────┘
                     │ HTTP/JSON
┌────────────────────▼─────────────────────────────────────────┐
│                    Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Endpoints (/architecture/*)                      │   │
│  │  - POST /architecture/graph                           │   │
│  │  - POST /architecture/module-graph                    │   │
│  │  - POST /architecture/api-relationships               │   │
│  │  - POST /architecture/dependency-tree                 │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│  ┌────────────────▼─────────────────────────────────────┐   │
│  │  GraphGenerator Service                               │   │
│  │  - generate_architecture_graph()                      │   │
│  │  - generate_module_graph()                            │   │
│  │  - generate_api_relationship_graph()                  │   │
│  │  - generate_dependency_tree()                         │   │
│  └────────────────┬─────────────────────────────────────┘   │
│                   │                                           │
│  ┌────────────────▼─────────────────────────────────────┐   │
│  │  DependencyParser Service                             │   │
│  │  - parse_python_file()                                │   │
│  │  - parse_javascript_file()                            │   │
│  │  - parse_directory()                                  │   │
│  │  - build_dependency_graph()                           │   │
│  └───────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

## Backend Components

### 1. DependencyParser (`backend/src/services/architecture/dependency_parser.py`)

**Purpose**: Parse code files and extract dependencies, imports, functions, and classes.

**Key Methods**:
- `parse_python_file(file_path)` - Parse Python files using AST
- `parse_javascript_file(file_path)` - Parse JS/TS files using regex
- `parse_directory(directory, file_patterns)` - Parse all files in directory
- `build_dependency_graph(parsed_files)` - Build node-edge graph from parsed data

**Supported Languages**:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts, .tsx)
- JSX (.jsx)

**Output Format**:
```python
{
    'file_path': 'path/to/file.py',
    'imports': [
        {'type': 'import', 'module': 'os', 'alias': None},
        {'type': 'from_import', 'module': 'pathlib', 'name': 'Path', 'alias': None}
    ],
    'functions': [
        {'name': 'my_function', 'line': 10, 'args': ['arg1', 'arg2']}
    ],
    'classes': [
        {'name': 'MyClass', 'line': 20, 'bases': ['BaseClass'], 'methods': ['method1']}
    ]
}
```

### 2. GraphGenerator (`backend/src/services/architecture/graph_generator.py`)

**Purpose**: Generate various types of architecture graphs.

**Key Methods**:

#### `generate_architecture_graph(directory, file_patterns, max_depth)`
Generates complete architecture graph with:
- All files as nodes
- Dependencies as edges
- Module groupings
- Architecture layers (API, Service, Data, Util)
- Metrics (total nodes, edges, avg dependencies)

#### `generate_module_graph(directory, module_path)`
Generates graph for specific module showing:
- Files within module
- Internal dependencies
- External connections

#### `generate_api_relationship_graph(directory)`
Generates graph showing:
- API endpoints as nodes
- Service dependencies
- Data layer connections

#### `generate_dependency_tree(directory, target_file)`
Generates dependency tree for specific file:
- Root file
- Direct dependencies
- Transitive dependencies (up to 5 levels)

### 3. API Endpoints (`backend/src/api/app.py`)

#### POST `/architecture/graph`
Generate full architecture graph.

**Request**:
```json
{
  "directory": "./backend/src",
  "file_patterns": ["*.py", "*.js"],
  "max_depth": 5
}
```

**Response**:
```json
{
  "nodes": [
    {
      "id": "backend_src_api_app_py",
      "label": "app.py",
      "type": "python",
      "path": "backend/src/api/app.py",
      "functions": 10,
      "classes": 2,
      "imports": 15
    }
  ],
  "edges": [
    {
      "id": "edge_1",
      "source": "node_1",
      "target": "node_2",
      "type": "import",
      "label": "models"
    }
  ],
  "modules": [...],
  "layers": [...],
  "metrics": {
    "total_nodes": 50,
    "total_edges": 120,
    "avg_dependencies": 2.4,
    "most_imported": [...],
    "most_importing": [...],
    "isolated_nodes": 3
  }
}
```

#### POST `/architecture/module-graph`
Generate module-specific graph.

**Query Parameters**:
- `directory`: Root directory
- `module_path`: Path to module

#### POST `/architecture/api-relationships`
Generate API relationship graph.

**Query Parameters**:
- `directory`: Root directory

#### POST `/architecture/dependency-tree`
Generate dependency tree for file.

**Request**:
```json
{
  "directory": "./backend/src",
  "target_file": "api/app.py"
}
```

## Frontend Components

### 1. ArchitectureGraph Component (`frontend/src/components/features/architecture/ArchitectureGraph.tsx`)

**Purpose**: Interactive React Flow visualization of architecture graph.

**Features**:
- **Node Visualization**: Color-coded by file type
- **Edge Visualization**: Animated for imports, labeled with module names
- **Interactive Controls**: Zoom, pan, fit view
- **Minimap**: Overview of entire graph
- **Node Details**: Click to see file details
- **Statistics Panel**: Real-time metrics
- **Legend**: File type color coding

**Props**:
```typescript
interface ArchitectureGraphProps {
  data: {
    nodes: GraphNode[];
    edges: GraphEdge[];
    metrics?: GraphMetrics;
  };
  onNodeClick?: (node: Node) => void;
}
```

**Node Colors**:
- Python: `#3776ab` (blue)
- JavaScript: `#f7df1e` (yellow)
- TypeScript: `#3178c6` (blue)
- TypeScript React: `#61dafb` (cyan)
- JavaScript React: `#61dafb` (cyan)
- Unknown: `#6b7280` (gray)

### 2. Architecture Page (`frontend/src/app/architecture/page.tsx`)

**Purpose**: Main page for architecture visualization.

**Features**:
- Directory input
- Generate graph button
- View selector (Full, Modules, Layers)
- Metrics overview cards
- Module and layer information
- Graph visualization
- Error handling
- Loading states

### 3. API Client (`frontend/src/lib/api/architecture.ts`)

**Purpose**: Frontend API client for architecture endpoints.

**Functions**:
- `generateArchitectureGraph(directory, filePatterns, maxDepth)`
- `generateModuleGraph(directory, modulePath)`
- `generateApiRelationships(directory)`
- `generateDependencyTree(directory, targetFile)`

## Usage Guide

### Backend Setup

1. **Install Dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Start Server**:
```bash
python start_server.py
```

Server runs on `http://localhost:8000`

### Frontend Setup

1. **Install Dependencies**:
```bash
cd frontend
npm install
```

2. **Configure API URL**:
Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Start Development Server**:
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

### Using the Visualization

1. **Navigate to Architecture Page**:
   - Go to `http://localhost:3000/architecture`

2. **Enter Directory Path**:
   - Input the path to analyze (e.g., `./backend/src`)
   - Path is relative to backend working directory

3. **Generate Graph**:
   - Click "Generate Graph" button
   - Wait for processing (may take a few seconds for large codebases)

4. **Explore Visualization**:
   - **Zoom**: Mouse wheel or controls
   - **Pan**: Click and drag background
   - **Select Node**: Click on any node to see details
   - **Fit View**: Use controls to fit entire graph

5. **View Metrics**:
   - Total files analyzed
   - Total dependencies found
   - Average dependencies per file
   - Isolated files (no connections)

6. **Explore Modules and Layers**:
   - View module breakdown
   - See architecture layers (API, Service, Data, Util)

## API Examples

### Generate Full Graph

```bash
curl -X POST http://localhost:8000/architecture/graph \
  -H "Content-Type: application/json" \
  -d '{
    "directory": "./backend/src",
    "file_patterns": ["*.py"],
    "max_depth": 5
  }'
```

### Generate Dependency Tree

```bash
curl -X POST http://localhost:8000/architecture/dependency-tree \
  -H "Content-Type: application/json" \
  -d '{
    "directory": "./backend/src",
    "target_file": "api/app.py"
  }'
```

## Customization

### Adding New File Types

Edit `DependencyParser` in `dependency_parser.py`:

```python
def parse_new_language_file(self, file_path: str) -> Dict:
    """Parse new language files."""
    # Implement parsing logic
    pass
```

### Custom Node Styling

Edit `ArchitectureGraph.tsx`:

```typescript
const nodeColors: Record<string, string> = {
  python: '#3776ab',
  // Add new colors
  rust: '#ce422b',
  go: '#00add8',
};
```

### Custom Layouts

Modify node positioning in `ArchitectureGraph.tsx`:

```typescript
// Current: Circular layout
const angle = (index / data.nodes.length) * 2 * Math.PI;
const radius = 300;

// Alternative: Grid layout
const x = (index % 10) * 200;
const y = Math.floor(index / 10) * 150;
```

## Performance Considerations

### Backend
- **Large Codebases**: Use `max_depth` to limit directory traversal
- **File Patterns**: Be specific to reduce parsing time
- **Caching**: Consider implementing caching for repeated requests

### Frontend
- **Node Limit**: React Flow performs well up to ~1000 nodes
- **Lazy Loading**: Consider pagination for very large graphs
- **Filtering**: Implement filters to show subsets of graph

## Troubleshooting

### Backend Issues

**Import Errors**:
```bash
# Ensure all dependencies installed
pip install -r requirements.txt
```

**Path Issues**:
- Use absolute paths or paths relative to backend working directory
- Check file permissions

### Frontend Issues

**API Connection Failed**:
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

**Graph Not Rendering**:
- Check browser console for errors
- Verify data format matches expected structure
- Ensure React Flow CSS is imported

## Future Enhancements

- [ ] Real-time updates as code changes
- [ ] Export graph as image/SVG
- [ ] Filter by file type, module, or layer
- [ ] Search functionality
- [ ] Dependency impact analysis
- [ ] Integration with Git history
- [ ] Performance metrics overlay
- [ ] Custom layout algorithms
- [ ] Collaborative annotations

## Made with Bob 🤖