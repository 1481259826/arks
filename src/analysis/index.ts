/**
 * ArkUI Lifecycle Call Graph Analyzer
 *
 * A TypeScript module for parsing and analyzing ArkUI lifecycle function call graphs
 * from RAG-generated JSON data.
 *
 * @example
 * ```typescript
 * import { LifecycleParser, CallGraph } from './analysis/index.js';
 *
 * const graph = await LifecycleParser.fromFile('data/outputs/result.json');
 * console.log(graph.topologicalSort());
 * ```
 */

// Type definitions
export type {
  LifecycleFunction,
  CallOrder,
  LifecycleAnalysis,
  LifecycleResult,
  CallGraphNode
} from './types/lifecycle.js';

// Core classes
export { CallGraph } from './graph/CallGraph.js';
export { LifecycleParser, ParseError } from './parser/LifecycleParser.js';
