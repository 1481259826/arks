/**
 * Converter tool to transform .txt files to .json format
 * Handles legacy format with "both" scope and "type" fields
 */

import { readFile, writeFile, readdir } from 'fs/promises';
import { join, basename } from 'path';

interface LegacyFunction {
  name: string;
  scope: string;
  type?: string;
  description: string;
}

interface LegacyLifecycle {
  functions: LegacyFunction[];
  order: Array<{ pred: string; succ: string }>;
  dynamicBehavior: string;
}

interface LegacyResult {
  lifecycle: LegacyLifecycle;
}

/**
 * Extract JSON from markdown code block
 */
function extractJsonFromMarkdown(content: string): string {
  // Remove markdown code fences
  const match = content.match(/```json\s*\n([\s\S]*?)\n```/);
  if (match && match[1]) {
    return match[1];
  }
  // If no markdown fences, return as-is
  return content;
}

/**
 * Normalize scope value
 */
function normalizeScope(scope: string): 'page' | 'component' {
  const lowerScope = scope.toLowerCase();

  // Map "both" to "component" by default
  if (lowerScope === 'both') {
    return 'component';
  }

  if (lowerScope === 'page') {
    return 'page';
  }

  if (lowerScope === 'component') {
    return 'component';
  }

  // Default to component
  return 'component';
}

/**
 * Extract unique function instances from order array
 */
function extractFunctionInstances(order: Array<{ pred: string; succ: string }>): Set<string> {
  const instances = new Set<string>();

  for (const edge of order) {
    instances.add(edge.pred);
    instances.add(edge.succ);
  }

  return instances;
}

/**
 * Parse function instance name (e.g., "SimpleDemo.aboutToAppear" -> "aboutToAppear")
 */
function parseFunctionName(fullName: string): string {
  const parts = fullName.split('.');
  return parts[parts.length - 1] || fullName;
}

/**
 * Convert legacy format to standard format
 * Handles both simple and instance-based naming
 */
function convertToStandardFormat(legacy: LegacyResult): any {
  // Extract all function instances from the order array
  const instances = extractFunctionInstances(legacy.lifecycle.order);

  // Check if we're dealing with instance-based naming (e.g., "Component.method")
  const hasInstanceNames = Array.from(instances).some(name => name.includes('.'));

  if (hasInstanceNames) {
    // Build a map of base function names to their metadata
    const functionMap = new Map<string, LegacyFunction>();
    for (const func of legacy.lifecycle.functions) {
      functionMap.set(func.name, func);
    }

    // Extract unique base function names
    const baseFunctions = new Map<string, any>();
    for (const fullName of instances) {
      const baseName = parseFunctionName(fullName);

      if (!baseFunctions.has(baseName)) {
        const metadata = functionMap.get(baseName);
        baseFunctions.set(baseName, {
          name: baseName,  // Only use base name
          scope: metadata ? normalizeScope(metadata.scope) : 'component' as const,
          description: metadata ? metadata.description : `Function ${baseName}`
        });
      }
    }

    // Convert to array and sort
    const standardFunctions = Array.from(baseFunctions.values()).sort((a, b) =>
      a.name.localeCompare(b.name)
    );

    return {
      lifecycle: {
        functions: standardFunctions,  // Only base functions
        order: legacy.lifecycle.order,  // Keep full instance names in order
        dynamicBehavior: legacy.lifecycle.dynamicBehavior
      }
    };
  } else {
    // Simple naming without instances
    const standardFunctions = legacy.lifecycle.functions.map(func => ({
      name: func.name,
      scope: normalizeScope(func.scope),
      description: func.description
    }));

    return {
      lifecycle: {
        functions: standardFunctions,
        order: legacy.lifecycle.order,
        dynamicBehavior: legacy.lifecycle.dynamicBehavior
      }
    };
  }
}

/**
 * Convert a single .txt file to .json
 */
async function convertFile(inputPath: string, outputPath: string): Promise<void> {
  try {
    // Read the .txt file
    const content = await readFile(inputPath, 'utf-8');

    // Extract JSON from markdown
    const jsonString = extractJsonFromMarkdown(content);

    // Parse the JSON
    const legacyData = JSON.parse(jsonString) as LegacyResult;

    // Convert to standard format
    const standardData = convertToStandardFormat(legacyData);

    // Write to .json file
    await writeFile(outputPath, JSON.stringify(standardData, null, 2), 'utf-8');

    console.log(`✓ Converted: ${basename(inputPath)} → ${basename(outputPath)}`);
  } catch (error) {
    console.error(`✗ Failed to convert ${basename(inputPath)}:`, error);
    throw error;
  }
}

/**
 * Convert all .txt files in a directory
 */
async function convertDirectory(dirPath: string): Promise<void> {
  console.log('🔄 Converting .txt files to .json format...\n');

  try {
    const files = await readdir(dirPath);
    const txtFiles = files.filter(f => f.endsWith('.txt'));

    if (txtFiles.length === 0) {
      console.log('⚠ No .txt files found in', dirPath);
      return;
    }

    console.log(`Found ${txtFiles.length} .txt file(s):\n`);

    let successCount = 0;
    let failCount = 0;

    for (const txtFile of txtFiles) {
      const inputPath = join(dirPath, txtFile);
      const outputFile = txtFile.replace('.txt', '.json');
      const outputPath = join(dirPath, outputFile);

      try {
        await convertFile(inputPath, outputPath);
        successCount++;
      } catch (error) {
        failCount++;
      }
    }

    console.log(`\n📊 Summary:`);
    console.log(`   Successful: ${successCount}`);
    console.log(`   Failed: ${failCount}`);
    console.log(`   Total: ${txtFiles.length}`);

    if (successCount > 0) {
      console.log('\n✅ Conversion complete!');
    }
  } catch (error) {
    console.error('❌ Error reading directory:', error);
    throw error;
  }
}

/**
 * Main function
 */
async function main() {
  // Convert from legacy directory to json directory
  const legacyDir = 'data/outputs/legacy';
  const outputDir = 'data/outputs/json';

  console.log('🔄 Converting legacy .txt files to JSON format...\n');
  console.log(`   Source: ${legacyDir}`);
  console.log(`   Target: ${outputDir}\n`);

  await convertDirectory(legacyDir);
}

// Run the converter
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
