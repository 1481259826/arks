/**
 * Example usage of the ArkUI Lifecycle Call Graph Analyzer
 */

import { readdir } from 'fs/promises';
import { join } from 'path';
import { LifecycleParser } from './index.js';

/**
 * Print a section header
 */
function printHeader(title: string): void {
  console.log('\n' + '='.repeat(60));
  console.log(`  ${title}`);
  console.log('='.repeat(60) + '\n');
}

/**
 * Print a subsection
 */
function printSubsection(title: string): void {
  console.log(`\n${title}`);
  console.log('-'.repeat(title.length));
}

/**
 * Example 1: Parse from JSON string
 */
function example1_ParseFromString(): void {
  printHeader('Example 1: Parse from JSON String');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "aboutToAppear", "scope": "page", "description": "页面即将出现"},
        {"name": "onPageShow", "scope": "page", "description": "页面显示"},
        {"name": "aboutToDisappear", "scope": "page", "description": "页面即将消失"},
        {"name": "onBackPress", "scope": "page", "description": "返回按钮按下"}
      ],
      "order": [
        {"pred": "aboutToAppear", "succ": "onPageShow"},
        {"pred": "onBackPress", "succ": "aboutToDisappear"}
      ],
      "dynamicBehavior": "标准页面生命周期"
    }
  }`;

  try {
    const graph = LifecycleParser.fromJSON(jsonData);
    console.log('✓ Successfully parsed JSON string');
    console.log(`  Nodes: ${graph.getStats().nodeCount}`);
    console.log(`  Edges: ${graph.getStats().edgeCount}`);
  } catch (error) {
    console.error('✗ Failed to parse:', error);
  }
}

/**
 * Example 2: Query node information
 */
function example2_QueryNodes(): void {
  printHeader('Example 2: Query Node Information');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "aboutToAppear", "scope": "component", "description": "组件即将出现"},
        {"name": "onDidBuild", "scope": "component", "description": "组件构建完成"},
        {"name": "aboutToDisappear", "scope": "component", "description": "组件即将消失"}
      ],
      "order": [
        {"pred": "aboutToAppear", "succ": "onDidBuild"},
        {"pred": "onDidBuild", "succ": "aboutToDisappear"}
      ],
      "dynamicBehavior": "组件生命周期"
    }
  }`;

  const graph = LifecycleParser.fromJSON(jsonData);

  printSubsection('All Nodes:');
  for (const node of graph.getAllNodes()) {
    console.log(`  - ${node.func.name} [${node.func.scope}]`);
    console.log(`    ${node.func.description}`);
  }

  printSubsection('Node Details for "aboutToAppear":');
  const node = graph.getNode('aboutToAppear');
  if (node) {
    console.log(`  Predecessors: ${graph.getPredecessors('aboutToAppear').join(', ') || 'none'}`);
    console.log(`  Successors: ${graph.getSuccessors('aboutToAppear').join(', ') || 'none'}`);
  }
}

/**
 * Example 3: Topological sort
 */
function example3_TopologicalSort(): void {
  printHeader('Example 3: Topological Sort');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "onCreate", "scope": "page", "description": "创建"},
        {"name": "onShow", "scope": "page", "description": "显示"},
        {"name": "onReady", "scope": "page", "description": "就绪"},
        {"name": "onHide", "scope": "page", "description": "隐藏"}
      ],
      "order": [
        {"pred": "onCreate", "succ": "onShow"},
        {"pred": "onShow", "succ": "onReady"},
        {"pred": "onReady", "succ": "onHide"}
      ],
      "dynamicBehavior": "线性生命周期"
    }
  }`;

  const graph = LifecycleParser.fromJSON(jsonData);

  try {
    const sorted = graph.topologicalSort();
    console.log('✓ Topological order:');
    sorted.forEach((name, index) => {
      console.log(`  ${index + 1}. ${name}`);
    });
  } catch (error) {
    console.error('✗ Failed to sort:', error);
  }
}

/**
 * Example 4: Path finding
 */
function example4_PathFinding(): void {
  printHeader('Example 4: Path Finding');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "A", "scope": "page", "description": "节点A"},
        {"name": "B", "scope": "page", "description": "节点B"},
        {"name": "C", "scope": "page", "description": "节点C"},
        {"name": "D", "scope": "page", "description": "节点D"}
      ],
      "order": [
        {"pred": "A", "succ": "B"},
        {"pred": "B", "succ": "C"},
        {"pred": "A", "succ": "D"},
        {"pred": "D", "succ": "C"}
      ],
      "dynamicBehavior": "多路径图"
    }
  }`;

  const graph = LifecycleParser.fromJSON(jsonData);

  const path = graph.findPath('A', 'C');
  if (path) {
    console.log('✓ Path from A to C:');
    console.log(`  ${path.join(' → ')}`);
  } else {
    console.log('✗ No path found from A to C');
  }
}

/**
 * Example 5: Export to DOT format
 */
function example5_ExportDot(): void {
  printHeader('Example 5: Export to Graphviz DOT Format');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "init", "scope": "component", "description": "初始化"},
        {"name": "mount", "scope": "component", "description": "挂载"},
        {"name": "unmount", "scope": "component", "description": "卸载"}
      ],
      "order": [
        {"pred": "init", "succ": "mount"},
        {"pred": "mount", "succ": "unmount"}
      ],
      "dynamicBehavior": "简单组件生命周期"
    }
  }`;

  const graph = LifecycleParser.fromJSON(jsonData);
  const dot = graph.toDot();

  console.log('DOT format output:');
  console.log(dot);
  console.log('\n💡 Tip: Save this to a .dot file and visualize with:');
  console.log('   dot -Tpng output.dot -o output.png');
}

/**
 * Example 6: Cycle detection
 */
function example6_CycleDetection(): void {
  printHeader('Example 6: Cycle Detection');

  printSubsection('Graph without cycles:');
  const acyclicData = `{
    "lifecycle": {
      "functions": [
        {"name": "A", "scope": "page", "description": "节点A"},
        {"name": "B", "scope": "page", "description": "节点B"}
      ],
      "order": [
        {"pred": "A", "succ": "B"}
      ],
      "dynamicBehavior": "无环图"
    }
  }`;

  const acyclicGraph = LifecycleParser.fromJSON(acyclicData);
  console.log(`  Has cycles: ${acyclicGraph.detectCycles()}`);

  printSubsection('Graph with cycles:');
  const cyclicData = `{
    "lifecycle": {
      "functions": [
        {"name": "A", "scope": "page", "description": "节点A"},
        {"name": "B", "scope": "page", "description": "节点B"},
        {"name": "C", "scope": "page", "description": "节点C"}
      ],
      "order": [
        {"pred": "A", "succ": "B"},
        {"pred": "B", "succ": "C"},
        {"pred": "C", "succ": "A"}
      ],
      "dynamicBehavior": "环形图"
    }
  }`;

  const cyclicGraph = LifecycleParser.fromJSON(cyclicData);
  console.log(`  Has cycles: ${cyclicGraph.detectCycles()}`);

  try {
    cyclicGraph.topologicalSort();
    console.log('  ✓ Topological sort succeeded (unexpected!)');
  } catch (error) {
    console.log('  ✗ Topological sort failed as expected:', (error as Error).message);
  }
}

/**
 * Example 7: Graph statistics
 */
function example7_Statistics(): void {
  printHeader('Example 7: Graph Statistics');

  const jsonData = `{
    "lifecycle": {
      "functions": [
        {"name": "root1", "scope": "page", "description": "根节点1"},
        {"name": "root2", "scope": "page", "description": "根节点2"},
        {"name": "middle", "scope": "page", "description": "中间节点"},
        {"name": "leaf", "scope": "page", "description": "叶节点"}
      ],
      "order": [
        {"pred": "root1", "succ": "middle"},
        {"pred": "root2", "succ": "middle"},
        {"pred": "middle", "succ": "leaf"}
      ],
      "dynamicBehavior": "多根节点图"
    }
  }`;

  const graph = LifecycleParser.fromJSON(jsonData);
  const stats = graph.getStats();

  console.log(`Nodes: ${stats.nodeCount}`);
  console.log(`Edges: ${stats.edgeCount}`);
  console.log(`Has cycles: ${stats.hasCycles}`);
  console.log(`Root nodes (no predecessors): ${stats.rootNodes.join(', ')}`);
  console.log(`Leaf nodes (no successors): ${stats.leafNodes.join(', ')}`);
}

/**
 * Example 8: Read from file
 */
async function example8_ReadFromFile(): Promise<void> {
  printHeader('Example 8: Read from File');

  const outputDir = 'data/outputs/json';

  try {
    const files = await readdir(outputDir);
    const jsonFiles = files.filter(f => f.endsWith('.json'));

    if (jsonFiles.length === 0) {
      console.log('⚠ No JSON files found in data/outputs/json/');
      console.log('  Run the Python analyzer first to generate output files.');
      return;
    }

    console.log(`Found ${jsonFiles.length} JSON file(s):`);
    jsonFiles.forEach(f => console.log(`  - ${f}`));

    // Try to load the first file
    const firstFile = join(outputDir, jsonFiles[0]!);
    console.log(`\nLoading: ${firstFile}`);

    const graph = await LifecycleParser.fromFile(firstFile);
    console.log('✓ Successfully loaded file');

    const stats = graph.getStats();
    console.log(`  Nodes: ${stats.nodeCount}`);
    console.log(`  Edges: ${stats.edgeCount}`);
    console.log(`  Dynamic behavior: ${graph.getDynamicBehavior()}`);

    if (stats.nodeCount > 0) {
      console.log('\nFirst few functions:');
      const nodes = graph.getAllNodes().slice(0, 3);
      for (const node of nodes) {
        console.log(`  - ${node.func.name} [${node.func.scope}]`);
      }
    }
  } catch (error) {
    console.error('✗ Error:', error);
  }
}

/**
 * Example 9: Error handling
 */
function example9_ErrorHandling(): void {
  printHeader('Example 9: Error Handling');

  printSubsection('Invalid JSON:');
  try {
    LifecycleParser.fromJSON('not valid json');
  } catch (error) {
    console.log(`  ✓ Caught error: ${(error as Error).message}`);
  }

  printSubsection('Missing required field:');
  try {
    LifecycleParser.fromJSON('{"lifecycle": {}}');
  } catch (error) {
    console.log(`  ✓ Caught error: ${(error as Error).message}`);
  }

  printSubsection('Invalid edge reference:');
  try {
    const invalidData = `{
      "lifecycle": {
        "functions": [
          {"name": "A", "scope": "page", "description": "节点A"}
        ],
        "order": [
          {"pred": "A", "succ": "B"}
        ],
        "dynamicBehavior": "无效边"
      }
    }`;
    LifecycleParser.fromJSON(invalidData);
  } catch (error) {
    console.log(`  ✓ Caught error: ${(error as Error).message}`);
  }
}

/**
 * Main function to run all examples
 */
async function main(): Promise<void> {
  console.log('\n🚀 ArkUI Lifecycle Call Graph Analyzer - Examples\n');

  example1_ParseFromString();
  example2_QueryNodes();
  example3_TopologicalSort();
  example4_PathFinding();
  example5_ExportDot();
  example6_CycleDetection();
  example7_Statistics();
  await example8_ReadFromFile();
  example9_ErrorHandling();

  console.log('\n' + '='.repeat(60));
  console.log('✓ All examples completed!');
  console.log('='.repeat(60) + '\n');
}

// Run examples
main().catch(console.error);
