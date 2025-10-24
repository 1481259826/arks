/**
 * 简单使用示例：演示如何使用 CallGraph 类
 */
import { CallGraph } from './dist/callgraph.js';
import { readFileSync } from 'fs';

console.log('=== CallGraph 使用示例 ===\n');

// 1. 从文件读取 JSON
const jsonPath = 'data/outputs/json/output1.json';
const jsonContent = readFileSync(jsonPath, 'utf-8');

// 2. 解析为 CallGraph
const graph = CallGraph.fromJSON(jsonContent);

// 3. 获取节点信息
console.log(`节点数量: ${graph.getNodeCount()}`);
const nodes = graph.getNodes();
console.log('\n函数节点:');
nodes.forEach(node => {
  console.log(`  - ${node.name} (${node.scope})`);
});

// 4. 获取边信息
console.log(`\n边数量: ${graph.getEdgeCount()}`);
const edges = graph.getEdges();
console.log('\n调用关系:');
edges.forEach(edge => {
  console.log(`  ${edge.pred} → ${edge.succ}`);
});

// 5. 获取动态行为描述
const behavior = graph.getDynamicBehavior();
if (behavior) {
  console.log(`\n动态行为:\n  ${behavior}`);
}

console.log('\n✓ 示例执行完成');
