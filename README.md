# ArkUI 生命周期分析 RAG 系统

本项目基于 RAG（检索增强生成）技术，从 ArkUI 官方文档中检索相关片段，结合用户提供的 ArkTS 代码场景，自动生成结构化的生命周期函数调用顺序分析结果。

## 功能特性

- **RAG 生命周期分析**：从向量库检索 ArkUI 文档片段，结合输入场景输出严格 JSON 格式的分析结果
- **模块化架构**：代码结构清晰，配置、核心逻辑、工具函数分离
- **命令行工具**：支持索引和分析两种操作模式
- **灵活配置**：支持 YAML 配置文件和命令行参数

## 环境准备

### Python 版本
- 建议：Python 3.9+

### 依赖安装
```bash
pip install -r requirements.txt
```

### 环境变量配置
复制 `.env.example` 为 `.env`，并填写你的 API 密钥：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```
OPENAI_API_KEY=你的密钥
OPENAI_API_BASE=你的自定义网关地址（可选）
```

## 项目结构

```
arkUI/
├── src/                          # 源代码目录
│   ├── __init__.py
│   ├── config.py                 # 配置管理
│   ├── rag_engine.py            # RAG 核心引擎
│   ├── vectorstore.py           # 向量库管理
│   └── utils.py                 # 工具函数
├── data/                         # 数据目录
│   ├── docs/                     # 文档资源
│   │   └── arkUI自定义组件生命周期.pdf
│   ├── inputs/                   # 输入示例
│   │   ├── input.txt
│   │   └── input1.txt
│   └── outputs/                  # 输出结果
├── notebooks/                    # Jupyter notebooks
│   └── arkUI.ipynb
├── vector_store/                 # 向量库（自动生成）
├── main.py                       # 主入口文件
├── config.yaml                   # 配置文件
├── requirements.txt              # 依赖管理
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git 忽略文件
├── README.md                     # 项目说明
└── CLAUDE.md                     # Claude Code 指南
```

## 快速开始

### 1. 首次索引（仅第一次需要）

将 PDF 文档放在 `data/docs/` 目录下，然后运行：

```bash
python main.py index
```

这将在 `vector_store/` 目录下生成向量索引。

### 2. 执行生命周期分析

准备你的 ArkTS 代码场景，保存到 `data/inputs/input.txt`，然后运行：

```bash
python main.py analyze
```

或者使用默认命令（不指定子命令时默认执行分析）：

```bash
python main.py
```

结果将保存到 `data/outputs/` 目录。

### 3. 高级用法

指定自定义输入文件：
```bash
python main.py analyze --input data/inputs/custom_input.txt
```

指定输出文件名：
```bash
python main.py analyze --output my_analysis.txt
```

强制重新索引：
```bash
python main.py index --force
```

使用自定义配置文件：
```bash
python main.py analyze --config custom_config.yaml
```

## 配置说明

编辑 `config.yaml` 文件可以调整以下参数：

### 路径配置
- `vector_store_path`: 向量库存储路径
- `input_file`: 默认输入文件路径
- `output_dir`: 输出目录
- `pdf_path`: PDF 文档路径

### LLM 配置
- `model_name`: 大模型名称（如 "deepseek-chat", "gpt-4o-mini"）
- `temperature`: 生成温度（0 表示确定性输出）

### 文档处理配置
- `chunk_size`: 文档分块大小（默认 1000）
- `chunk_overlap`: 分块重叠长度（默认 200）
- `retriever_k`: 检索返回的文档片段数量（默认 4）

## 输出格式

系统生成的 JSON 格式包含：

```json
{
  "lifecycle": {
    "functions": [
      {
        "name": "函数名",
        "scope": "page 或 component",
        "description": "触发时机和作用说明"
      }
    ],
    "order": [
      {
        "pred": "前驱函数",
        "succ": "后继函数"
      }
    ],
    "dynamicBehavior": "动态场景下的生命周期变化说明"
  }
}
```

## 示例输入

在 `data/inputs/input.txt` 中编写 ArkTS 代码示例：

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

## 调参建议

- **初学者**：使用默认配置即可
- **答案缺少上下文**：增加 `retriever_k` 或 `chunk_size`
- **结果冗余**：减小 `retriever_k` 或 `chunk_overlap`
- **输出不稳定**：确保 `temperature=0`

## Jupyter Notebook

如需交互式探索，可以使用：

```bash
jupyter notebook notebooks/arkUI.ipynb
```

## 常见问题

### 向量库不存在
运行 `python main.py index` 创建索引。

### API 密钥错误
检查 `.env` 文件中的 `OPENAI_API_KEY` 配置。

### 输出不是有效 JSON
- 确保 `temperature=0`
- 提高 `retriever_k` 改善检索质量
- 优化 `chunk_size` 和 `chunk_overlap`

## 旧版本兼容

旧版本的 `arkui_lifecycle_rag.py` 仍然可用，但建议使用新的模块化版本（`main.py`）。

---

祝你用 RAG 快速梳理 ArkUI 自定义组件的生命周期！