/**
 * Test the converted JSON files
 */

import { LifecycleParser } from './index.js';

async function testConvertedFiles() {
  console.log('🧪 Testing Converted JSON Files\n');

  const files = [
    'data/outputs/lifecycle_analysis_20251016_183649.json',
    'data/outputs/lifecycle_analysis_20251016_184425.json'
  ];

  for (const file of files) {
    console.log(`📄 Testing: ${file}`);
    console.log('─'.repeat(60));

    try {
      const graph = await LifecycleParser.fromFile(file);

      // Display statistics
      const stats = graph.getStats();
      console.log(`✓ Successfully loaded`);
      console.log(`  Nodes: ${stats.nodeCount}`);
      console.log(`  Edges: ${stats.edgeCount}`);
      console.log(`  Has cycles: ${stats.hasCycles}`);

      // Display functions
      console.log(`\n  Functions:`);
      for (const node of graph.getAllNodes()) {
        console.log(`    - ${node.func.name} [${node.func.scope}]`);
      }

      // Try topological sort
      try {
        const sorted = graph.topologicalSort();
        console.log(`\n  Topological order:`);
        console.log(`    ${sorted.join(' → ')}`);
      } catch (error) {
        console.log(`\n  ⚠ Cannot sort (contains cycles)`);
      }

      console.log();

    } catch (error) {
      console.error(`✗ Failed to load:`, error);
    }
  }

  console.log('✅ All tests completed!\n');
}

testConvertedFiles().catch(console.error);
