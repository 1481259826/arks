# TypeScript 调用图分析模块使用指南

本文档介绍如何使用 TypeScript 模块分析 Python RAG 系统生成的 ArkUI 生命周期函数调用图。

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 构建项目

```bash
npm run build
```

### 3. 转换旧格式文件（如果需要）

如果你有旧的 `.txt` 格式的生命周期分析文件：

```bash
# 自动转换 data/outputs/ 下所有 .txt 文件为 .json
npm run convert
```

转换器会自动处理：
- 提取 markdown 代码块中的 JSON
- 将 `scope: "both"` 转换为 `scope: "component"`
- 移除额外的 `type` 字段
- 处理实例化的函数名（如 `Component.method`）

### 4. 运行示例

```bash
# 运行所有示例
npm run example

# 运行集成示例
npm run integration

# 可视化所有 JSON 文件并导出 DOT 格式
npm run visualize
```

## 使用场景

### 场景 1：解析 Python 生成的 JSON 文件

```typescript
import { LifecycleParser } from './dist/index.js';

// 从 Python RAG 系统的输出文件加载
const graph = await LifecycleParser.fromFile('data/outputs/result.json');

// 查看基本信息
const stats = graph.getStats();
console.log(`节点数: ${stats.nodeCount}`);
console.log(`边数: ${stats.edgeCount}`);
```

### 场景 2：分析调用顺序

```typescript
// 获取拓扑排序（执行顺序）
const executionOrder = graph.topologicalSort();
console.log('执行顺序:', executionOrder.join(' → '));

// 查找特定路径
const path = graph.findPath('aboutToAppear', 'aboutToDisappear');
if (path) {
  console.log('路径:', path.join(' → '));
}
```

### 场景 3：导出可视化

```typescript
import { writeFile } from 'fs/promises';

// 导出为 Graphviz DOT 格式
const dotContent = graph.toDot();
await writeFile('output.dot', dotContent);

// 使用 Graphviz 生成图片
// dot -Tpng output.dot -o output.png
```

### 场景 4：查询节点信息

```typescript
// 获取某个节点的信息
const node = graph.getNode('aboutToAppear');
if (node) {
  console.log(`函数: ${node.func.name}`);
  console.log(`作用域: ${node.func.scope}`);
  console.log(`描述: ${node.func.description}`);
}

// 获取后继节点
const successors = graph.getSuccessors('aboutToAppear');
console.log('后继:', successors);

// 获取前驱节点
const predecessors = graph.getPredecessors('onPageShow');
console.log('前驱:', predecessors);
```

### 场景 5：检测循环依赖

```typescript
if (graph.detectCycles()) {
  console.log('⚠️ 警告: 调用图包含循环依赖');
  // 无法进行拓扑排序
} else {
  console.log('✓ 调用图无环');
  const sorted = graph.topologicalSort();
}
```

## 与 Python RAG 系统集成

### 完整工作流程

1. **使用 Python 生成分析结果**

```bash
# 准备 ArkTS 代码场景
echo "你的 ArkTS 代码" > data/inputs/scenario.txt

# 运行 RAG 分析
python main.py analyze --input data/inputs/scenario.txt --output result.json
```

2. **使用 TypeScript 分析调用图**

```typescript
import { LifecycleParser } from './dist/index.js';

// 加载 Python 生成的结果
const graph = await LifecycleParser.fromFile('data/outputs/result.json');

// 执行图分析
const order = graph.topologicalSort();
console.log('生命周期执行顺序:', order);

// 导出可视化
const dot = graph.toDot();
await writeFile('data/outputs/visualization.dot', dot);
```

3. **生成可视化图表（可选）**

```bash
# 安装 Graphviz (如果还没有)
# Windows: choco install graphviz
# macOS: brew install graphviz
# Linux: sudo apt-get install graphviz

# 生成 PNG 图片
dot -Tpng data/outputs/visualization.dot -o data/outputs/lifecycle.png

# 或生成 SVG
dot -Tsvg data/outputs/visualization.dot -o data/outputs/lifecycle.svg
```

## NPM 脚本参考

| 脚本 | 说明 |
|------|------|
| `npm run build` | 编译 TypeScript 代码到 `dist/` 目录 |
| `npm run build:watch` | 监听模式编译，文件改变时自动重新编译 |
| `npm run type-check` | 类型检查（不生成文件） |
| `npm run example` | 运行所有功能示例 |
| `npm run integration` | 运行与 Python 集成的示例 |
| `npm run convert` | 转换 `.txt` 文件为 `.json` 格式 |
| `npm run visualize` | 为所有 JSON 文件生成 DOT 可视化 |
| `npm run clean` | 清理编译输出 |

## API 快速参考

### LifecycleParser 类

| 方法 | 说明 |
|------|------|
| `fromJSON(jsonString)` | 从 JSON 字符串解析 |
| `fromObject(data)` | 从 JavaScript 对象解析 |
| `fromFile(filePath)` | 从文件读取并解析 |
| `validate(graph)` | 验证图的完整性 |

### CallGraph 类

**节点操作**
| 方法 | 说明 |
|------|------|
| `addNode(func)` | 添加节点 |
| `getNode(name)` | 获取节点 |
| `getAllNodes()` | 获取所有节点 |
| `hasNode(name)` | 检查节点是否存在 |

**边操作**
| 方法 | 说明 |
|------|------|
| `addEdge(pred, succ)` | 添加有向边 |
| `hasEdge(pred, succ)` | 检查边是否存在 |
| `getSuccessors(name)` | 获取后继节点列表 |
| `getPredecessors(name)` | 获取前驱节点列表 |

**图分析**
| 方法 | 说明 |
|------|------|
| `topologicalSort()` | 拓扑排序（Kahn 算法） |
| `findPath(start, end)` | 查找路径（BFS） |
| `detectCycles()` | 检测是否有环 |
| `getStats()` | 获取图统计信息 |

**导入导出**
| 方法 | 说明 |
|------|------|
| `toDot()` | 导出为 Graphviz DOT 格式 |
| `toJSON()` | 导出为 JSON 格式 |
| `getDynamicBehavior()` | 获取动态行为描述 |
| `setDynamicBehavior(text)` | 设置动态行为描述 |

## 常见问题

### Q: 如何处理大型调用图？

A: CallGraph 使用高效的数据结构（邻接表），所有核心操作的时间复杂度：
- 添加节点/边: O(1)
- 拓扑排序: O(V + E)
- 路径查找: O(V + E)

对于数千个节点的图也能高效处理。

### Q: 如何处理解析错误？

A: 使用 try-catch 捕获 `ParseError`：

```typescript
import { ParseError } from './dist/index.js';

try {
  const graph = await LifecycleParser.fromFile('invalid.json');
} catch (error) {
  if (error instanceof ParseError) {
    console.error('解析失败:', error.message);
    // error.cause 包含原始错误
  }
}
```

### Q: 如何在 JavaScript 项目中使用？

A: 生成的代码是 ES Modules，可以直接在 Node.js 18+ 中使用：

```javascript
// 确保 package.json 中有 "type": "module"
import { LifecycleParser } from './dist/index.js';

const graph = await LifecycleParser.fromFile('data.json');
console.log(graph.getStats());
```

### Q: 图包含循环依赖怎么办？

A: 使用 `detectCycles()` 检测，然后分析问题：

```typescript
if (graph.detectCycles()) {
  // 循环存在，无法拓扑排序
  // 但其他操作（路径查找、统计等）仍然可用
  const stats = graph.getStats();
  console.log('根节点:', stats.rootNodes);
  console.log('叶节点:', stats.leafNodes);
}
```

## 项目结构

```
src/analysis/
├── types/
│   └── lifecycle.ts           # TypeScript 类型定义
├── graph/
│   └── CallGraph.ts           # 调用图数据结构
├── parser/
│   └── LifecycleParser.ts     # JSON 解析器
├── index.ts                   # 统一导出
├── example.ts                 # 综合示例
├── integration_example.ts     # 集成示例
└── README.md                  # API 文档

dist/                          # 编译输出（自动生成）
data/
├── inputs/                    # ArkTS 代码输入
└── outputs/                   # JSON 输出和可视化文件
```

## 更多资源

- [TypeScript 模块 API 文档](src/analysis/README.md)
- [Python RAG 系统文档](CLAUDE.md)
- [Graphviz 文档](https://graphviz.org/documentation/)

## 贡献

欢迎提交 Issue 和 Pull Request！
