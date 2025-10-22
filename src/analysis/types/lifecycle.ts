/**
 * Type definitions for ArkUI lifecycle analysis
 */

/**
 * Represents a lifecycle function in ArkUI
 */
export interface LifecycleFunction {
  /** Function name (e.g., "aboutToAppear", "onPageShow") */
  name: string;

  /** Scope where the function is defined */
  scope: 'page' | 'component';

  /** Description of the function's purpose */
  description: string;
}

/**
 * Represents a directed edge in the call graph
 * Indicates that pred is called before succ
 */
export interface CallOrder {
  /** Predecessor function name (called first) */
  pred: string;

  /** Successor function name (called after) */
  succ: string;
}

/**
 * Complete lifecycle analysis data
 */
export interface LifecycleAnalysis {
  /** List of all lifecycle functions identified */
  functions: LifecycleFunction[];

  /** Call order relationships between functions */
  order: CallOrder[];

  /** Description of dynamic behavior patterns */
  dynamicBehavior: string;
}

/**
 * Root object returned by the RAG API
 */
export interface LifecycleResult {
  /** Lifecycle analysis data */
  lifecycle: LifecycleAnalysis;
}

/**
 * Represents a node in the call graph
 */
export interface CallGraphNode {
  /** Function information */
  func: LifecycleFunction;

  /** Set of successor function names */
  successors: Set<string>;

  /** Set of predecessor function names */
  predecessors: Set<string>;
}
