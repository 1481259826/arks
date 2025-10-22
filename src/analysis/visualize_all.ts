/**
 * Visualize all JSON files in data/outputs
 */

import { readdir, writeFile } from 'fs/promises';
import { join } from 'path';
import { LifecycleParser } from './index.js';

async function visualizeAllFiles() {
  console.log('🎨 Visualizing All Lifecycle JSON Files\n');

  const jsonDir = 'data/outputs/json';
  const vizDir = 'data/outputs/visualizations';

  try {
    const files = await readdir(jsonDir);
    const jsonFiles = files.filter(f => f.endsWith('.json') && !f.includes('export'));

    if (jsonFiles.length === 0) {
      console.log('⚠ No JSON files found');
      return;
    }

    console.log(`Found ${jsonFiles.length} JSON file(s):\n`);

    for (const jsonFile of jsonFiles) {
      const inputPath = join(jsonDir, jsonFile);
      const baseName = jsonFile.replace('.json', '');
      const dotPath = join(vizDir, `${baseName}.dot`);

      console.log(`📄 ${jsonFile}`);
      console.log('─'.repeat(60));

      try {
        // Load the graph
        const graph = await LifecycleParser.fromFile(inputPath);

        // Get statistics
        const stats = graph.getStats();
        console.log(`  Nodes: ${stats.nodeCount}, Edges: ${stats.edgeCount}`);
        console.log(`  Cycles: ${stats.hasCycles ? 'Yes ⚠' : 'No ✓'}`);

        // Export to DOT
        const dotContent = graph.toDot();
        await writeFile(dotPath, dotContent, 'utf-8');
        console.log(`  ✓ Exported DOT: ${baseName}.dot`);

        // Show topological order if possible
        if (!stats.hasCycles) {
          const order = graph.topologicalSort();
          console.log(`  Order: ${order.slice(0, 3).join(' → ')}${order.length > 3 ? ' ...' : ''}`);
        }

        console.log();

      } catch (error) {
        console.error(`  ✗ Failed:`, (error as Error).message);
        console.log();
      }
    }

    console.log('✅ Visualization complete!\n');
    console.log('💡 Generate images with:');
    console.log('   dot -Tpng data/outputs/visualizations/*.dot -O');
    console.log('   or for a specific file:');
    console.log('   dot -Tpng data/outputs/visualizations/filename.dot -o filename.png\n');

  } catch (error) {
    console.error('❌ Error:', error);
    process.exit(1);
  }
}

visualizeAllFiles().catch(console.error);
