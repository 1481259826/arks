/**
 * Parser for lifecycle analysis JSON data
 */

import { readFile } from 'fs/promises';
import { CallGraph } from '../graph/CallGraph.js';
import type { LifecycleFunction } from '../types/lifecycle.js';

/**
 * Error thrown when parsing fails
 */
export class ParseError extends Error {
  constructor(message: string, public cause?: unknown) {
    super(message);
    this.name = 'ParseError';
  }
}

/**
 * Parser for converting lifecycle JSON data to CallGraph
 */
export class LifecycleParser {
  /**
   * Parse a JSON string into a CallGraph
   * @throws {ParseError} If JSON is invalid or format is incorrect
   */
  static fromJSON(jsonString: string): CallGraph {
    try {
      const data = JSON.parse(jsonString);
      return this.fromObject(data);
    } catch (error) {
      if (error instanceof ParseError) {
        throw error;
      }
      throw new ParseError('Failed to parse JSON string', error);
    }
  }

  /**
   * Parse a LifecycleResult object into a CallGraph
   * @throws {ParseError} If data format is invalid
   */
  static fromObject(data: unknown): CallGraph {
    // Validate root structure
    if (!this.isObject(data)) {
      throw new ParseError('Data must be an object');
    }

    if (!('lifecycle' in data)) {
      throw new ParseError('Missing required field: lifecycle');
    }

    const lifecycle = data.lifecycle;
    if (!this.isObject(lifecycle)) {
      throw new ParseError('lifecycle must be an object');
    }

    // Validate required fields
    if (!('functions' in lifecycle)) {
      throw new ParseError('Missing required field: lifecycle.functions');
    }
    if (!('order' in lifecycle)) {
      throw new ParseError('Missing required field: lifecycle.order');
    }

    const { functions, order, dynamicBehavior } = lifecycle;

    // Validate functions array
    if (!Array.isArray(functions)) {
      throw new ParseError('lifecycle.functions must be an array');
    }

    // Validate order array
    if (!Array.isArray(order)) {
      throw new ParseError('lifecycle.order must be an array');
    }

    // Validate dynamic behavior
    const behavior = typeof dynamicBehavior === 'string' ? dynamicBehavior : '';

    // Create graph
    const graph = new CallGraph(behavior);

    // Build a map of base function names to their metadata
    const functionMap = new Map<string, LifecycleFunction>();

    for (let i = 0; i < functions.length; i++) {
      const func = functions[i];

      if (!this.isObject(func)) {
        throw new ParseError(`functions[${i}] must be an object`);
      }

      if (!('name' in func) || typeof func.name !== 'string') {
        throw new ParseError(`functions[${i}].name must be a string`);
      }

      if (!('scope' in func) || (func.scope !== 'page' && func.scope !== 'component')) {
        throw new ParseError(`functions[${i}].scope must be "page" or "component"`);
      }

      if (!('description' in func) || typeof func.description !== 'string') {
        throw new ParseError(`functions[${i}].description must be a string`);
      }

      const lifecycleFunc: LifecycleFunction = {
        name: func.name,
        scope: func.scope as 'page' | 'component',
        description: func.description
      };

      functionMap.set(func.name, lifecycleFunc);
    }

    // Collect all unique instance names from order array
    const instanceNames = new Set<string>();
    for (const edge of order) {
      if (this.isObject(edge)) {
        if ('pred' in edge && typeof edge.pred === 'string') {
          instanceNames.add(edge.pred);
        }
        if ('succ' in edge && typeof edge.succ === 'string') {
          instanceNames.add(edge.succ);
        }
      }
    }

    // Create nodes for all instances, mapping them to base functions
    for (const instanceName of instanceNames) {
      const baseName = this.parseBaseName(instanceName);
      const baseFunc = functionMap.get(baseName);

      if (!baseFunc) {
        throw new ParseError(
          `Instance "${instanceName}" references unknown base function: ${baseName}`
        );
      }

      // Create a node for this instance with the base function's metadata
      const instanceFunc: LifecycleFunction = {
        name: instanceName,
        scope: baseFunc.scope,
        description: baseFunc.description
      };

      graph.addNode(instanceFunc);
    }

    // Add all edges
    for (let i = 0; i < order.length; i++) {
      const edge = order[i];

      if (!this.isObject(edge)) {
        throw new ParseError(`order[${i}] must be an object`);
      }

      if (!('pred' in edge) || typeof edge.pred !== 'string') {
        throw new ParseError(`order[${i}].pred must be a string`);
      }

      if (!('succ' in edge) || typeof edge.succ !== 'string') {
        throw new ParseError(`order[${i}].succ must be a string`);
      }

      graph.addEdge(edge.pred, edge.succ);
    }

    return graph;
  }

  /**
   * Read and parse a JSON file into a CallGraph
   * @throws {ParseError} If file cannot be read or parsed
   */
  static async fromFile(filePath: string): Promise<CallGraph> {
    try {
      const content = await readFile(filePath, 'utf-8');
      return this.fromJSON(content);
    } catch (error) {
      if (error instanceof ParseError) {
        throw error;
      }
      throw new ParseError(`Failed to read file: ${filePath}`, error);
    }
  }

  /**
   * Type guard to check if value is an object
   */
  private static isObject(value: unknown): value is Record<string, unknown> {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
  }

  /**
   * Parse base function name from instance name
   * e.g., "Component.method" -> "method", "method" -> "method"
   */
  private static parseBaseName(instanceName: string): string {
    const parts = instanceName.split('.');
    return parts[parts.length - 1] || instanceName;
  }

  /**
   * Validate that a CallGraph can be serialized back to valid JSON
   */
  static validate(graph: CallGraph): boolean {
    try {
      const json = graph.toJSON();
      const reparsed = this.fromObject(json);

      // Check that the graphs are equivalent
      const originalStats = graph.getStats();
      const reparsedStats = reparsed.getStats();

      return (
        originalStats.nodeCount === reparsedStats.nodeCount &&
        originalStats.edgeCount === reparsedStats.edgeCount
      );
    } catch {
      return false;
    }
  }
}
