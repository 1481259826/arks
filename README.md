# ArkUI 生命周期分析 RAG 系统

本项目基于 RAG（检索增强生成）技术，从 ArkUI 官方文档中检索相关片段，结合用户提供的 ArkTS 代码场景，自动生成结构化的生命周期函数调用顺序分析结果。系统包含 **Python RAG 后端**和 **TypeScript 调用图分析模块**两部分。

## 功能特性

### Python RAG 后端
- **RAG 生命周期分析**：从向量库检索 ArkUI 文档片段，结合输入场景输出严格 JSON 格式的分析结果
- **模块化架构**：代码结构清晰，配置、核心逻辑、工具函数分离
- **命令行工具**：支持索引和分析两种操作模式
- **灵活配置**：支持 YAML 配置文件和命令行参数

### TypeScript 调用图数据结构
- **简洁轻量**：仅提供核心图数据结构（节点 + 边）
- **类型安全**：完整的 TypeScript 类型定义
- **JSON 解析**：从 Python 后端生成的 JSON 构建图
- **基础接口**：访问节点、边和统计信息

## 目录

- [环境准备](#环境准备)
- [项目结构](#项目结构)
- [快速开始](#快速开始)
  - [Python RAG 分析](#python-rag-分析)
  - [TypeScript 使用](#typescript-使用)
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
├── src/                          # 源代码
│   ├── __init__.py               # Python 包初始化
│   ├── config.py                 # 配置管理和 Prompt 模板
│   ├── rag_engine.py             # RAG 核心引擎
│   ├── vectorstore.py            # 向量库管理
│   ├── utils.py                  # 工具函数
│   └── callgraph.ts              # TypeScript 调用图数据结构 ⭐
│
├── data/
│   ├── docs/                     # PDF 文档
│   │   └── arkUI自定义组件生命周期.pdf
│   ├── inputs/                   # ArkTS 代码输入
│   │   └── input.txt
│   └── outputs/                  # 分析结果
│       ├── .gitignore            # 输出目录 Git 配置
│       └── json/                 # JSON 输出文件
│           └── output1.json      # 示例输出
│
├── node_modules/                 # NPM 依赖包（自动生成，26MB）
├── vector_store/                 # Chroma 向量库（自动生成）
├── dist/                         # TypeScript 编译输出（自动生成）
│   ├── callgraph.js              # 编译后的 JS
│   ├── callgraph.d.ts            # 类型声明文件
│   └── callgraph.js.map          # Source Map
│
├── main.py                       # Python 主入口
├── example.js                    # TypeScript 使用示例
├── config.yaml                   # RAG 配置文件
├── package.json                  # Node.js 项目配置
├── package-lock.json             # NPM 依赖锁定
├── tsconfig.json                 # TypeScript 配置
├── requirements.txt              # Python 依赖
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git 忽略配置
├── CLAUDE.md                     # Claude Code 项目指南
└── README.md                     # 本文档
```

---

## 快速开始

### Python RAG 分析

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

### TypeScript 使用

#### 构建项目

```bash
# 编译 TypeScript
npm run build

# 监听模式（开发时使用）
npm run build:watch

# 仅类型检查
npm run type-check
```

#### 编程式使用

```typescript
import { CallGraph } from './dist/callgraph.js';
import { readFileSync } from 'fs';

// 从文件读取 JSON
const jsonContent = readFileSync('data/outputs/json/output1.json', 'utf-8');

// 解析调用图
const graph = CallGraph.fromJSON(jsonContent);

// 访问节点和边
const nodes = graph.getNodes();
const edges = graph.getEdges();

// 打印基本信息
console.log(`节点数: ${graph.getNodeCount()}`);
console.log(`边数: ${graph.getEdgeCount()}`);

// 遍历调用关系
for (const edge of edges) {
  console.log(`${edge.pred} -> ${edge.succ}`);
}

// 查看动态行为描述
console.log(graph.getDynamicBehavior());
```

#### NPM 脚本

| 脚本 | 说明 |
|------|------|
| `npm run build` | 编译 TypeScript 到 `dist/` |
| `npm run build:watch` | 监听模式编译 |
| `npm run type-check` | 类型检查（不生成文件） |
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

#### CallGraph 类

**静态方法**：
- `static fromJSON(jsonStr: string): CallGraph` - 从 JSON 字符串构建图

**访问方法**：
- `getNodes(): FunctionNode[]` - 获取所有节点
- `getEdges(): Edge[]` - 获取所有边
- `getDynamicBehavior(): string | undefined` - 获取动态行为描述
- `getNodeCount(): number` - 获取节点数量
- `getEdgeCount(): number` - 获取边数量

#### 类型定义

```typescript
interface FunctionNode {
  name: string;        // 函数名
  scope: string;       // 作用域（page/component）
  description: string; // 描述
}

interface Edge {
  pred: string;  // 前驱函数（调用者）
  succ: string;  // 后继函数（被调用者）
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

**Q: 如何处理 JSON 解析错误？**

```typescript
import { CallGraph } from './dist/callgraph.js';

try {
  const graph = CallGraph.fromJSON(invalidJsonString);
} catch (error) {
  console.error('解析失败:', error.message);
}
```

**Q: 如何在 JavaScript 项目中使用？**

```javascript
// 确保 package.json 中有 "type": "module"
import { CallGraph } from './dist/callgraph.js';
import { readFileSync } from 'fs';

const json = readFileSync('data/outputs/json/output1.json', 'utf-8');
const graph = CallGraph.fromJSON(json);

console.log(`节点数: ${graph.getNodeCount()}`);
console.log(`边数: ${graph.getEdgeCount()}`);
```

**Q: CallGraph 是否包含复杂的图算法？**

A: 不包含。CallGraph 是一个简单的数据结构，只提供基本的节点和边访问接口。如需拓扑排序、路径查找等算法，请在外部实现或使用其他图算法库。

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

### TypeScript 调用图模块

**设计理念**：
- **简洁优先**：只提供核心数据结构，不包含复杂算法
- **类型安全**：使用 TypeScript 严格类型系统
- **易于集成**：可与 ArkAnalyzer 等框架无缝集成

**核心功能**：
- 从 JSON 解析构建图结构
- 访问节点（函数）和边（调用关系）
- 获取基本统计信息

---

## 测试和验证

### 验证系统配置

在首次使用前，运行验证脚本检查配置：

```bash
conda activate 你的虚拟环境名
python scripts/verify_setup.py
```

### 运行测试

```bash
# Python 分析测试
conda activate 你的虚拟环境名
python main.py analyze --output test.json

# TypeScript 编译测试
npm run build
npm run type-check
```

---

## 更多资源

### 项目文档
- **🔧 Claude Code 指南**：[CLAUDE.md](CLAUDE.md) - 项目架构和开发指南

### 外部资源
- **LangChain 文档**：https://python.langchain.com/
- **HarmonyOS 开发文档**：https://developer.harmonyos.com/

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

---

**祝你用 RAG 快速梳理 ArkUI 自定义组件的生命周期！**
