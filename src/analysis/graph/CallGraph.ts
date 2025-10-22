/**
 * Call graph data structure for lifecycle analysis
 */

import type {
  LifecycleFunction,
  CallOrder,
  LifecycleResult,
  CallGraphNode as ICallGraphNode
} from '../types/lifecycle.js';

/**
 * Node in the call graph
 */
class CallGraphNode implements ICallGraphNode {
  func: LifecycleFunction;
  successors: Set<string>;
  predecessors: Set<string>;

  constructor(func: LifecycleFunction) {
    this.func = func;
    this.successors = new Set();
    this.predecessors = new Set();
  }
}

/**
 * Directed graph representing lifecycle function call relationships
 */
export class CallGraph {
  private nodes: Map<string, CallGraphNode>;
  private dynamicBehavior: string;

  constructor(dynamicBehavior: string = '') {
    this.nodes = new Map();
    this.dynamicBehavior = dynamicBehavior;
  }

  /**
   * Add a lifecycle function node to the graph
   */
  addNode(func: LifecycleFunction): void {
    if (!this.nodes.has(func.name)) {
      this.nodes.set(func.name, new CallGraphNode(func));
    }
  }

  /**
   * Add a directed edge from pred to succ
   */
  addEdge(pred: string, succ: string): void {
    const predNode = this.nodes.get(pred);
    const succNode = this.nodes.get(succ);

    if (!predNode) {
      throw new Error(`Predecessor node "${pred}" not found in graph`);
    }
    if (!succNode) {
      throw new Error(`Successor node "${succ}" not found in graph`);
    }

    predNode.successors.add(succ);
    succNode.predecessors.add(pred);
  }

  /**
   * Get a node by function name
   */
  getNode(name: string): CallGraphNode | undefined {
    return this.nodes.get(name);
  }

  /**
   * Get all successor function names for a given node
   */
  getSuccessors(name: string): string[] {
    const node = this.nodes.get(name);
    return node ? Array.from(node.successors) : [];
  }

  /**
   * Get all predecessor function names for a given node
   */
  getPredecessors(name: string): string[] {
    const node = this.nodes.get(name);
    return node ? Array.from(node.predecessors) : [];
  }

  /**
   * Get all nodes in the graph
   */
  getAllNodes(): CallGraphNode[] {
    return Array.from(this.nodes.values());
  }

  /**
   * Check if a node exists in the graph
   */
  hasNode(name: string): boolean {
    return this.nodes.has(name);
  }

  /**
   * Check if an edge exists between two nodes
   */
  hasEdge(pred: string, succ: string): boolean {
    const node = this.nodes.get(pred);
    return node ? node.successors.has(succ) : false;
  }

  /**
   * Get the dynamic behavior description
   */
  getDynamicBehavior(): string {
    return this.dynamicBehavior;
  }

  /**
   * Set the dynamic behavior description
   */
  setDynamicBehavior(behavior: string): void {
    this.dynamicBehavior = behavior;
  }

  /**
   * Perform topological sort using Kahn's algorithm
   * Returns sorted function names, or throws if cycle detected
   */
  topologicalSort(): string[] {
    // Create copy of in-degree map
    const inDegree = new Map<string, number>();
    for (const [name, node] of this.nodes) {
      inDegree.set(name, node.predecessors.size);
    }

    // Find all nodes with no incoming edges
    const queue: string[] = [];
    for (const [name, degree] of inDegree) {
      if (degree === 0) {
        queue.push(name);
      }
    }

    const result: string[] = [];

    while (queue.length > 0) {
      const current = queue.shift()!;
      result.push(current);

      const node = this.nodes.get(current)!;
      for (const succ of node.successors) {
        const degree = inDegree.get(succ)! - 1;
        inDegree.set(succ, degree);
        if (degree === 0) {
          queue.push(succ);
        }
      }
    }

    // If result doesn't contain all nodes, there's a cycle
    if (result.length !== this.nodes.size) {
      throw new Error('Graph contains a cycle - cannot perform topological sort');
    }

    return result;
  }

  /**
   * Find a path from start to end using BFS
   * Returns the path as an array of function names, or null if no path exists
   */
  findPath(start: string, end: string): string[] | null {
    if (!this.hasNode(start) || !this.hasNode(end)) {
      return null;
    }

    if (start === end) {
      return [start];
    }

    const visited = new Set<string>();
    const queue: Array<{ node: string; path: string[] }> = [{ node: start, path: [start] }];
    visited.add(start);

    while (queue.length > 0) {
      const { node, path } = queue.shift()!;

      for (const succ of this.getSuccessors(node)) {
        if (succ === end) {
          return [...path, succ];
        }

        if (!visited.has(succ)) {
          visited.add(succ);
          queue.push({ node: succ, path: [...path, succ] });
        }
      }
    }

    return null;
  }

  /**
   * Detect if the graph contains any cycles
   */
  detectCycles(): boolean {
    try {
      this.topologicalSort();
      return false;
    } catch {
      return true;
    }
  }

  /**
   * Export the graph in Graphviz DOT format
   */
  toDot(): string {
    const lines: string[] = ['digraph LifecycleCallGraph {'];
    lines.push('  rankdir=TB;');
    lines.push('  node [shape=box, style=rounded];');
    lines.push('');

    // Add nodes with labels
    for (const [name, node] of this.nodes) {
      const scope = node.func.scope;
      const color = scope === 'page' ? 'lightblue' : 'lightgreen';
      const label = `${name}\\n[${scope}]\\n${node.func.description}`;
      lines.push(`  "${name}" [label="${label}", fillcolor="${color}", style="rounded,filled"];`);
    }

    lines.push('');

    // Add edges
    for (const [name, node] of this.nodes) {
      for (const succ of node.successors) {
        lines.push(`  "${name}" -> "${succ}";`);
      }
    }

    // Add dynamic behavior as a note
    if (this.dynamicBehavior) {
      lines.push('');
      lines.push('  note [shape=note, label="' + this.dynamicBehavior.replace(/"/g, '\\"') + '"];');
    }

    lines.push('}');
    return lines.join('\n');
  }

  /**
   * Export the graph as the original JSON format
   */
  toJSON(): LifecycleResult {
    const functions: LifecycleFunction[] = [];
    const order: CallOrder[] = [];

    // Collect all functions
    for (const node of this.nodes.values()) {
      functions.push({
        name: node.func.name,
        scope: node.func.scope,
        description: node.func.description
      });
    }

    // Collect all edges
    for (const [pred, node] of this.nodes) {
      for (const succ of node.successors) {
        order.push({ pred, succ });
      }
    }

    return {
      lifecycle: {
        functions,
        order,
        dynamicBehavior: this.dynamicBehavior
      }
    };
  }

  /**
   * Get statistics about the graph
   */
  getStats(): {
    nodeCount: number;
    edgeCount: number;
    hasCycles: boolean;
    rootNodes: string[];
    leafNodes: string[];
  } {
    let edgeCount = 0;
    const rootNodes: string[] = [];
    const leafNodes: string[] = [];

    for (const [name, node] of this.nodes) {
      edgeCount += node.successors.size;

      if (node.predecessors.size === 0) {
        rootNodes.push(name);
      }
      if (node.successors.size === 0) {
        leafNodes.push(name);
      }
    }

    return {
      nodeCount: this.nodes.size,
      edgeCount,
      hasCycles: this.detectCycles(),
      rootNodes,
      leafNodes
    };
  }
}
