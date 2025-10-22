# ArkUI Lifecycle Call Graph Analyzer

TypeScript module for parsing and analyzing ArkUI lifecycle function call graphs from RAG-generated JSON data.

## Features

- **Type-safe parsing**: Full TypeScript type definitions for lifecycle data
- **Graph operations**: Topological sort, path finding, cycle detection
- **Multiple input formats**: Parse from JSON strings, objects, or files
- **Export capabilities**: Export to Graphviz DOT format or back to JSON
- **Comprehensive error handling**: Detailed validation and error messages
- **Graph analysis**: Get statistics, find root/leaf nodes, analyze relationships

## Installation

```bash
npm install
npm run build
```

## Quick Start

### Parse from JSON String

```typescript
import { LifecycleParser } from './analysis/index.js';

const jsonData = `{
  "lifecycle": {
    "functions": [
      {"name": "aboutToAppear", "scope": "page", "description": "页面即将出现"},
      {"name": "onPageShow", "scope": "page", "description": "页面显示"}
    ],
    "order": [
      {"pred": "aboutToAppear", "succ": "onPageShow"}
    ],
    "dynamicBehavior": "标准页面生命周期"
  }
}`;

const graph = LifecycleParser.fromJSON(jsonData);
```

### Parse from File

```typescript
const graph = await LifecycleParser.fromFile('data/outputs/result.json');
```

### Query Graph Information

```typescript
// Get all nodes
const nodes = graph.getAllNodes();
for (const node of nodes) {
  console.log(`${node.func.name} [${node.func.scope}]: ${node.func.description}`);
}

// Get successors and predecessors
const successors = graph.getSuccessors('aboutToAppear');
const predecessors = graph.getPredecessors('onPageShow');

// Check if node or edge exists
if (graph.hasNode('aboutToAppear')) {
  console.log('Node exists');
}
if (graph.hasEdge('aboutToAppear', 'onPageShow')) {
  console.log('Edge exists');
}
```

### Perform Topological Sort

```typescript
try {
  const sorted = graph.topologicalSort();
  console.log('Execution order:', sorted.join(' → '));
} catch (error) {
  console.error('Graph contains cycles!');
}
```

### Find Path Between Nodes

```typescript
const path = graph.findPath('aboutToAppear', 'aboutToDisappear');
if (path) {
  console.log('Path found:', path.join(' → '));
} else {
  console.log('No path exists');
}
```

### Detect Cycles

```typescript
if (graph.detectCycles()) {
  console.log('Graph contains cycles');
} else {
  console.log('Graph is acyclic');
}
```

### Export to Graphviz DOT

```typescript
const dotContent = graph.toDot();
// Save to file and visualize:
// dot -Tpng output.dot -o output.png
```

### Get Graph Statistics

```typescript
const stats = graph.getStats();
console.log(`Nodes: ${stats.nodeCount}`);
console.log(`Edges: ${stats.edgeCount}`);
console.log(`Has cycles: ${stats.hasCycles}`);
console.log(`Root nodes: ${stats.rootNodes.join(', ')}`);
console.log(`Leaf nodes: ${stats.leafNodes.join(', ')}`);
```

## API Reference

### LifecycleParser

Static methods for parsing lifecycle data:

- `fromJSON(jsonString: string): CallGraph` - Parse from JSON string
- `fromObject(data: unknown): CallGraph` - Parse from JavaScript object
- `fromFile(filePath: string): Promise<CallGraph>` - Parse from file
- `validate(graph: CallGraph): boolean` - Validate graph integrity

### CallGraph

Graph data structure and operations:

**Node Operations:**
- `addNode(func: LifecycleFunction): void` - Add a node
- `getNode(name: string): CallGraphNode | undefined` - Get node by name
- `getAllNodes(): CallGraphNode[]` - Get all nodes
- `hasNode(name: string): boolean` - Check if node exists

**Edge Operations:**
- `addEdge(pred: string, succ: string): void` - Add directed edge
- `hasEdge(pred: string, succ: string): boolean` - Check if edge exists
- `getSuccessors(name: string): string[]` - Get successor nodes
- `getPredecessors(name: string): string[]` - Get predecessor nodes

**Graph Analysis:**
- `topologicalSort(): string[]` - Perform topological sort (Kahn's algorithm)
- `findPath(start: string, end: string): string[] | null` - Find path (BFS)
- `detectCycles(): boolean` - Check for cycles
- `getStats()` - Get graph statistics

**Import/Export:**
- `toDot(): string` - Export to Graphviz DOT format
- `toJSON(): LifecycleResult` - Export to JSON
- `getDynamicBehavior(): string` - Get behavior description
- `setDynamicBehavior(behavior: string): void` - Set behavior description

## Type Definitions

### LifecycleFunction

```typescript
interface LifecycleFunction {
  name: string;
  scope: 'page' | 'component';
  description: string;
}
```

### CallOrder

```typescript
interface CallOrder {
  pred: string;  // Predecessor function
  succ: string;  // Successor function
}
```

### LifecycleAnalysis

```typescript
interface LifecycleAnalysis {
  functions: LifecycleFunction[];
  order: CallOrder[];
  dynamicBehavior: string;
}
```

### LifecycleResult

```typescript
interface LifecycleResult {
  lifecycle: LifecycleAnalysis;
}
```

## Examples

Run the comprehensive example suite:

```bash
npm run example
```

This demonstrates:
1. Parsing from JSON strings
2. Querying node information
3. Topological sorting
4. Path finding
5. DOT format export
6. Cycle detection
7. Graph statistics
8. Reading from files
9. Error handling

## Error Handling

The parser throws `ParseError` for invalid data:

```typescript
try {
  const graph = LifecycleParser.fromJSON(invalidJson);
} catch (error) {
  if (error instanceof ParseError) {
    console.error('Parse failed:', error.message);
    console.error('Cause:', error.cause);
  }
}
```

Common errors:
- Invalid JSON syntax
- Missing required fields
- Invalid scope values (must be 'page' or 'component')
- Edge references to non-existent nodes

## Integration with Python RAG System

This TypeScript module is designed to work with the Python RAG system:

1. **Python generates JSON**: Run `python main.py analyze` to generate lifecycle analysis
2. **TypeScript processes graph**: Load the JSON output and perform graph operations
3. **Visualize results**: Export to DOT format for visualization

Example workflow:

```bash
# Generate analysis with Python
python main.py analyze --input data/inputs/scenario.txt

# Process with TypeScript
node -e "
import('./dist/index.js').then(async ({ LifecycleParser }) => {
  const graph = await LifecycleParser.fromFile('data/outputs/result.json');
  console.log('Execution order:', graph.topologicalSort().join(' → '));
});
"
```

## Architecture

```
types/lifecycle.ts      - Type definitions
graph/CallGraph.ts      - Graph data structure and algorithms
parser/LifecycleParser.ts - JSON parsing and validation
index.ts                - Public API exports
example.ts              - Usage examples
```

## Algorithms

- **Topological Sort**: Kahn's algorithm (O(V + E))
- **Path Finding**: Breadth-First Search (O(V + E))
- **Cycle Detection**: Based on topological sort

## License

MIT
