# ArkUI 生命周期分析 RAG 系统

本项目基于 RAG（检索增强生成）技术，从 ArkUI 官方文档中检索相关片段，结合用户提供的 ArkTS 代码场景，自动生成结构化的生命周期函数调用顺序分析结果。系统包含 **Python RAG 后端**和 **TypeScript 调用图分析模块**两部分。

## 功能特性

### Python RAG 后端
- **RAG 生命周期分析**：从向量库检索 ArkUI 文档片段，结合输入场景输出严格 JSON 格式的分析结果
- **模块化架构**：代码结构清晰，配置、核心逻辑、工具函数分离
- **命令行工具**：支持索引和分析两种操作模式
- **灵活配置**：支持 YAML 配置文件和命令行参数

### TypeScript 调用图分析模块
- **类型安全解析**：完整的 TypeScript 类型定义
- **图算法**：拓扑排序、路径查找、环检测
- **多种输入格式**：支持 JSON 字符串、对象、文件
- **导出能力**：导出为 Graphviz DOT 格式或 JSON
- **图统计分析**：获取根节点、叶节点、图统计信息

## 目录

- [环境准备](#环境准备)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
  - [Part 1: Python RAG 分析](#part-1-python-rag-分析)
  - [Part 2: TypeScript 调用图分析](#part-2-typescript-调用图分析)
- [完整工作流程](#完整工作流程)
- [配置说明](#配置说明)
- [API 参考](#api-参考)
- [常见问题](#常见问题)

---

## 环境准备

### Python 环境
- **版本要求**：Python 3.9+
- **依赖安装**：
  ```bash
  pip install -r requirements.txt
  ```
- **环境变量配置**：
  ```bash
  cp .env.example .env
  # 编辑 .env 文件，填写 OPENAI_API_KEY
  ```

### TypeScript/Node.js 环境
- **版本要求**：Node.js 18+
- **依赖安装**：
  ```bash
  npm install
  ```
- **构建项目**：
  ```bash
  npm run build
  ```

---

## 项目结构

```
arkUI/
├── src/                          # Python 源代码
│   ├── __init__.py
│   ├── config.py                 # 配置管理和 Prompt 模板
│   ├── rag_engine.py            # RAG 核心引擎
│   ├── vectorstore.py           # 向量库管理
│   ├── utils.py                 # 工具函数
│   └── analysis/                # TypeScript 分析模块
│       ├── types/
│       │   └── lifecycle.ts     # 类型定义
│       ├── graph/
│       │   └── CallGraph.ts     # 调用图数据结构
│       ├── parser/
│       │   └── LifecycleParser.ts # JSON 解析器
│       ├── index.ts             # 统一导出
│       ├── example.ts           # 示例代码
│       ├── integration_example.ts
│       └── visualize_all.ts     # 批量可视化
├── data/
│   ├── docs/                    # PDF 文档
│   │   └── arkUI自定义组件生命周期.pdf
│   ├── inputs/                  # ArkTS 代码输入
│   │   ├── input.txt
│   │   └── input1.txt
│   └── outputs/                 # 分析结果
│       ├── json/                # JSON 输出
│       ├── visualizations/      # DOT 可视化文件
│       ├── legacy/              # 旧版 .txt 文件
│       └── archives/            # 归档文件
├── notebooks/
│   └── arkUI.ipynb              # Jupyter 探索笔记
├── scripts/                     # 🔧 辅助脚本
│   ├── README.md                # 脚本说明
│   ├── organize_outputs.py      # 整理输出目录
│   └── verify_setup.py          # 验证系统配置
├── docs/                        # 📚 项目文档
│   ├── README.md                # 文档索引
│   ├── API_REFERENCE.md         # TypeScript API 参考
│   ├── TEST_RESULTS.md          # 测试报告
│   ├── CHANGELOG.md             # 版本变更记录
│   └── TYPESCRIPT_USAGE.md      # TypeScript 使用指南（已合并）
├── vector_store/                # Chroma 向量库（自动生成）
├── dist/                        # TypeScript 编译输出
├── main.py                      # Python 主入口
├── config.yaml                  # 配置文件
├── package.json                 # Node.js 项目配置
├── tsconfig.json                # TypeScript 配置
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例
├── CLAUDE.md                    # Claude Code 项目指南（必须在根目录）
└── README.md                    # 本文档（项目主文档）
```

---

## 快速开始

### Part 1: Python RAG 分析

#### 1. 首次索引（仅第一次需要）

```bash
# 激活虚拟环境（如果使用 conda）
conda activate CreatPPT

# 索引 PDF 文档
python main.py index
```

这将在 `vector_store/` 目录下生成向量索引。

#### 2. 执行生命周期分析

准备 ArkTS 代码场景，保存到 `data/inputs/input.txt`：

```typescript
@Entry
@Component
struct SimpleDemo {
  @State showChild: boolean = true

  aboutToAppear() {
    console.info('SimpleDemo aboutToAppear')
  }

  build() {
    Column() {
      if (this.showChild) {
        SimpleChild()
      }
    }
  }
}
```

运行分析：

```bash
# 使用默认配置
python main.py analyze

# 或指定输入/输出文件
python main.py analyze --input data/inputs/custom.txt --output result.json

# 强制重新索引
python main.py index --force
```

生成的 JSON 会保存到 `data/outputs/json/` 目录。

#### 3. 输出格式示例

```json
{
  "lifecycle": {
    "functions": [
      {
        "name": "aboutToAppear",
        "scope": "component",
        "description": "组件即将出现时触发，用于初始化操作"
      },
      {
        "name": "build",
        "scope": "component",
        "description": "UI构建方法，声明式描述UI结构，状态变化时重新执行"
      }
    ],
    "order": [
      {
        "pred": "SimpleDemo.aboutToAppear",
        "succ": "SimpleDemo.build"
      },
      {
        "pred": "SimpleDemo.build",
        "succ": "SimpleChild.aboutToAppear"
      }
    ],
    "dynamicBehavior": "当showChild状态从true变为false时，触发SimpleChild.aboutToDisappear..."
  }
}
```

**关键点**：
- `functions` 数组：包含唯一的基础函数名（不带组件前缀）
- `order` 数组：包含完整的实例名（如 `SimpleDemo.aboutToAppear`）
- TypeScript 模块会自动将基础函数映射到实例节点

---

### Part 2: TypeScript 调用图分析

#### 1. 解析 JSON 并分析调用图

```bash
# 运行示例
npm run example

# 运行集成示例
npm run integration

# 批量可视化所有 JSON 文件
npm run visualize
```

#### 2. 编程式使用

```typescript
import { LifecycleParser } from './dist/index.js';

// 从 Python 生成的 JSON 文件加载
const graph = await LifecycleParser.fromFile('data/outputs/json/output1.json');

// 获取统计信息
const stats = graph.getStats();
console.log(`节点数: ${stats.nodeCount}`);
console.log(`边数: ${stats.edgeCount}`);
console.log(`是否有环: ${stats.hasCycles}`);

// 拓扑排序（执行顺序）
const order = graph.topologicalSort();
console.log('执行顺序:', order.join(' → '));

// 查找路径
const path = graph.findPath('SimpleDemo.aboutToAppear', 'SimpleChild.aboutToDisappear');
if (path) {
  console.log('路径:', path.join(' → '));
}

// 导出为 Graphviz DOT 格式
const dotContent = graph.toDot();
await writeFile('data/outputs/visualizations/graph.dot', dotContent);
```

#### 3. 生成可视化图片

**方法 1：在线可视化（无需安装，推荐）**

1. 访问 https://dreampuf.github.io/GraphvizOnline/
2. 打开 `data/outputs/visualizations/output1.dot` 文件
3. 复制全部内容，粘贴到网页左侧编辑器
4. 右侧自动显示可视化调用图
5. 下载 PNG 或 SVG 图片

**方法 2：使用 Graphviz（本地生成）**

安装 Graphviz：
```bash
# Windows
choco install graphviz

# macOS
brew install graphviz

# Linux
sudo apt-get install graphviz
```

生成图片：
```bash
cd data/outputs/visualizations

# 生成 SVG（矢量图，推荐）
dot -Tsvg output1.dot -o output1.svg

# 生成 PNG（位图）
dot -Tpng output1.dot -o output1.png
```

📖 **详细指南**：查看 [docs/DOT_VISUALIZATION_GUIDE.md](docs/DOT_VISUALIZATION_GUIDE.md) 了解更多选项

---

## 完整工作流程

### 端到端示例

```bash
# 1. Python: 索引文档（首次运行）
conda activate CreatPPT
python main.py index

# 2. Python: 分析 ArkTS 代码
python main.py analyze --output my_analysis.json

# 3. TypeScript: 解析调用图并生成统计
npm run build
node -e "
import('./dist/index.js').then(async ({ LifecycleParser }) => {
  const graph = await LifecycleParser.fromFile('data/outputs/json/my_analysis.json');
  console.log('执行顺序:', graph.topologicalSort().join(' → '));
  const stats = graph.getStats();
  console.log('节点数:', stats.nodeCount);
  console.log('边数:', stats.edgeCount);
});
"

# 4. TypeScript: 导出可视化
npm run visualize

# 5. Graphviz: 生成图片
dot -Tpng data/outputs/visualizations/my_analysis.dot -o my_analysis.png
```

### NPM 脚本参考

| 脚本 | 说明 |
|------|------|
| `npm run build` | 编译 TypeScript 到 `dist/` |
| `npm run build:watch` | 监听模式编译 |
| `npm run type-check` | 类型检查（不生成文件） |
| `npm run example` | 运行所有功能示例 |
| `npm run integration` | 运行集成示例 |
| `npm run visualize` | 为所有 JSON 生成 DOT 文件 |
| `npm run convert` | 转换旧 .txt 为 .json |
| `npm run clean` | 清理编译输出 |

---

## 配置说明

### config.yaml

```yaml
# 路径配置
vector_store_path: "./vector_store"
input_file: "./data/inputs/input.txt"
output_dir: "./data/outputs"
pdf_path: "./data/docs/arkUI自定义组件生命周期.pdf"

# LLM 配置
model_name: "deepseek-chat"  # 或 "gpt-4o-mini"
temperature: 0               # 0 表示确定性输出

# 文档处理配置
chunk_size: 1500            # 文档分块大小
chunk_overlap: 300          # 分块重叠长度
retriever_k: 4              # 检索返回的文档片段数量
```

### 调参建议

| 场景 | 建议 |
|------|------|
| **初学者** | 使用默认配置 |
| **答案缺少上下文** | 增加 `retriever_k` 或 `chunk_size` |
| **结果冗余** | 减小 `retriever_k` 或 `chunk_overlap` |
| **输出不稳定** | 确保 `temperature=0` |
| **aboutToDisappear 顺序错误** | `retriever_k=4` 是最佳值 |

**重要发现**：
- `retriever_k=4`：✅ 检索到关键文档，正确输出 Parent → Child
- `retriever_k=6`：❌ 可能检索到干扰性文档，导致错误顺序

---

## API 参考

### Python API

#### Config 类
```python
from src.config import Config

# 使用默认配置
config = Config()

# 使用自定义 YAML 配置
config = Config(config_file="custom_config.yaml")

# 访问配置
print(config.model_name)
print(config.chunk_size)
```

#### VectorStoreManager 类
```python
from src.vectorstore import VectorStoreManager

manager = VectorStoreManager(config)

# 加载并索引 PDF
manager.load_and_index_pdf()

# 加载现有向量库
vectorstore = manager.load_vectorstore()

# 获取检索器
retriever = manager.get_retriever()
```

#### RAGEngine 类
```python
from src.rag_engine import RAGEngine

engine = RAGEngine(config, retriever)

# 分析 ArkTS 代码
result = engine.analyze(arkts_code)
```

### TypeScript API

#### LifecycleParser 类

| 方法 | 说明 |
|------|------|
| `fromJSON(jsonString: string): CallGraph` | 从 JSON 字符串解析 |
| `fromObject(data: unknown): CallGraph` | 从 JavaScript 对象解析 |
| `fromFile(filePath: string): Promise<CallGraph>` | 从文件读取并解析 |
| `validate(graph: CallGraph): boolean` | 验证图的完整性 |

#### CallGraph 类

**节点操作**：
- `addNode(func: LifecycleFunction): void`
- `getNode(name: string): CallGraphNode | undefined`
- `getAllNodes(): CallGraphNode[]`
- `hasNode(name: string): boolean`

**边操作**：
- `addEdge(pred: string, succ: string): void`
- `hasEdge(pred: string, succ: string): boolean`
- `getSuccessors(name: string): string[]`
- `getPredecessors(name: string): string[]`

**图分析**：
- `topologicalSort(): string[]` - Kahn 算法，O(V+E)
- `findPath(start: string, end: string): string[] | null` - BFS，O(V+E)
- `detectCycles(): boolean` - 环检测
- `getStats()` - 获取图统计（节点数、边数、根节点、叶节点）

**导入导出**：
- `toDot(): string` - 导出为 Graphviz DOT 格式
- `toJSON(): LifecycleResult` - 导出为 JSON
- `getDynamicBehavior(): string`
- `setDynamicBehavior(behavior: string): void`

#### 类型定义

```typescript
interface LifecycleFunction {
  name: string;
  scope: 'page' | 'component';
  description: string;
}

interface CallOrder {
  pred: string;  // 前驱函数
  succ: string;  // 后继函数
}

interface LifecycleAnalysis {
  functions: LifecycleFunction[];
  order: CallOrder[];
  dynamicBehavior: string;
}
```

---

## 常见问题

### Python 相关

**Q: 向量库不存在错误**

A: 运行 `python main.py index` 创建索引。

**Q: API 密钥错误**

A: 检查 `.env` 文件中的 `OPENAI_API_KEY` 配置。

**Q: 输出不是有效 JSON**

A:
- 确保 `temperature=0`
- 调整 `retriever_k` 改善检索质量
- 优化 `chunk_size` 和 `chunk_overlap`

**Q: aboutToDisappear 执行顺序错误**

A:
- 使用 `retriever_k=4`（最佳值）
- Prompt 模板已优化，包含明确的顺序说明
- 正确顺序：Parent.aboutToDisappear → Child.aboutToDisappear

### TypeScript 相关

**Q: 如何处理解析错误？**

```typescript
import { ParseError } from './dist/index.js';

try {
  const graph = await LifecycleParser.fromFile('invalid.json');
} catch (error) {
  if (error instanceof ParseError) {
    console.error('解析失败:', error.message);
  }
}
```

**Q: 图包含循环依赖怎么办？**

```typescript
if (graph.detectCycles()) {
  console.log('图包含环，无法拓扑排序');
  // 但其他操作仍可用
  const stats = graph.getStats();
  console.log('根节点:', stats.rootNodes);
}
```

**Q: 如何在 JavaScript 项目中使用？**

```javascript
// 确保 package.json 中有 "type": "module"
import { LifecycleParser } from './dist/index.js';

const graph = await LifecycleParser.fromFile('data.json');
console.log(graph.getStats());
```

**Q: 如何处理大型调用图？**

A: CallGraph 使用邻接表，算法复杂度：
- 添加节点/边: O(1)
- 拓扑排序: O(V + E)
- 路径查找: O(V + E)

可高效处理数千节点的图。

---

## 架构说明

### Python RAG 系统

**数据流**：

1. **索引阶段**（一次性）：
   ```
   PDF → PyPDFLoader → RecursiveCharacterTextSplitter
       → OpenAIEmbeddings → Chroma 向量库
   ```

2. **分析阶段**（重复使用）：
   ```
   ArkTS 代码 → Retriever (Top-k 搜索) → 格式化上下文
              → Prompt 模板 → LLM → JSON 输出
   ```

### TypeScript 分析模块

**组件架构**：
- `types/lifecycle.ts`：类型定义
- `graph/CallGraph.ts`：图数据结构和算法
- `parser/LifecycleParser.ts`：JSON 解析和验证
- `index.ts`：统一导出

**算法**：
- **拓扑排序**：Kahn 算法（O(V+E)）
- **路径查找**：广度优先搜索（O(V+E)）
- **环检测**：基于拓扑排序

### 实例映射机制

**关键设计**：
- `functions` 数组：只包含基础函数名（如 `aboutToAppear`）
- `order` 数组：包含完整实例名（如 `SimpleDemo.aboutToAppear`）
- TypeScript 解析器自动创建实例节点：
  1. 从 `functions` 构建基础函数映射
  2. 从 `order` 提取所有实例名
  3. 为每个实例创建独立节点，继承基础函数的元数据

---

## 测试和验证

### 验证系统配置

在首次使用前，运行验证脚本检查配置：

```bash
conda activate CreatPPT
python scripts/verify_setup.py
```

### 运行完整测试

```bash
# Python 分析
conda activate CreatPPT
python main.py analyze --output test.json

# TypeScript 解析
npm run build
node dist/example.js

# 可视化
npm run visualize
```

查看测试报告：
- [docs/TEST_RESULTS.md](docs/TEST_RESULTS.md)：完整测试结果
- [docs/CHANGELOG.md](docs/CHANGELOG.md)：版本变更记录

---

## 更多资源

### 项目文档
- **📚 文档索引**：[docs/README.md](docs/README.md) - 所有文档的导航中心
- **🔧 Claude Code 指南**：[CLAUDE.md](CLAUDE.md) - 项目架构和开发指南（AI 助手必读）
- **📖 TypeScript API 参考**：[docs/API_REFERENCE.md](docs/API_REFERENCE.md) - 完整 API 文档
- **✅ 测试报告**：[docs/TEST_RESULTS.md](docs/TEST_RESULTS.md) - 功能验证和性能统计
- **📝 变更记录**：[docs/CHANGELOG.md](docs/CHANGELOG.md) - 版本历史

### 外部资源
- **Graphviz 文档**：https://graphviz.org/documentation/
- **LangChain 文档**：https://python.langchain.com/
- **HarmonyOS 开发文档**：https://developer.harmonyos.com/

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

---

**祝你用 RAG 快速梳理 ArkUI 自定义组件的生命周期！**
