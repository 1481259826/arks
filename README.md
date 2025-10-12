# ArkUI 生命周期分析与智能代理示例

本项目围绕 ArkUI 自定义组件生命周期的理解与分析，提供基于 RAG（检索增强生成）的推理脚本，以及两类智能体示例（ReAct、Plan-and-Execute）。你可以用本项目从官方文档或 PDF 中检索相关片段，结合你提供的场景，自动生成结构化的生命周期调用顺序分析结果。

## 功能概览
- RAG 生命周期分析：从向量库检索 ArkUI 文档片段，结合输入场景输出严格 JSON 的分析结果。
- ReAct 代理示例：可调用检索工具按步骤思考并回答 ArkUI 相关问题。
- Plan-and-Execute 代理示例：先规划再执行，适合多步骤需求。

## 环境准备
- 建议 Python 版本：`3.9+`
- 依赖安装（按需）：
  - `pip install langchain langchain-openai langchain-community langchain-chroma chromadb python-dotenv pypdf`
  - 如需运行 Notebook：`pip install jupyter ipykernel`

## 配置密钥
在项目根目录创建或编辑 `.env` 文件：
- `OPENAI_API_KEY=你的密钥`
- `SERPAPI_API_KEY=你的密钥`（仅 ReAct/Plan-and-Execute 示例需要）
- 可选：`OPENAI_API_BASE=你的自定义网关地址`

## 项目结构
```
c:\code\arkUI
├── Rag.py                      # RAG 生命周期分析主脚本
├── ReAct.py                    # ReAct 智能体示例
├── Plan_n_Execute.py           # 计划-执行智能体示例
├── arkUI.ipynb                 # Notebook 演示（加载 PDF、构建 RAG）
├── arkUI自定义组件生命周期.pdf   # ArkUI 生命周期官方文档 PDF（示例）
├── input.txt                   # 输入场景文本（RAG 的 question）
├── lifecycle_analysis_output*.txt # RAG 输出的 JSON 结果
└── vector_store/               # Chroma 向量库持久化目录
```

## 快速开始（RAG 生命周期分析）
1. 准备数据索引：将 `arkUI自定义组件生命周期.pdf` 放在项目根目录。
2. 首次索引（仅第一次需要）：
   - 打开 `Rag.py`，在文件末尾的入口处取消注释 `index_pdf_documents()`，运行一次：
     - `python Rag.py`
   - 完成后会在 `vector_store/` 生成向量索引。
3. 正常运行分析：恢复注释 `index_pdf_documents()`，确保入口调用的是 `main()`，然后执行：
   - `python Rag.py`
   - 结果会保存到 `lifecycle_analysis_output.txt`（或你自己命名的文件）。

## 使用说明（Rag.py）
- 配置项（见 `CONFIG`）：
  - `vector_store_path`：向量库持久化目录。
  - `input_file`：作为用户场景与问题的输入文件（用作 `question`）。
  - `model_name`：大模型名称（按你的服务商可用模型填写）。
  - `temperature`：生成温度，`0` 更稳定可控。
  - `chunk_size`：文档分块大小。
  - `chunk_overlap`：相邻分块的重叠长度，常用 100–250（中文字符）。
  - `retriever_k`：每次检索返回的片段数（Top‑k）。

- 提示模板（`PROMPT_TEMPLATE`）占位符：
  - `context`：从向量库检索到的参考片段集合。
  - `question`：你的输入场景（来自 `input.txt` 的全文）。
  - 输出字段包含：
    - `analysis`：逐步的生命周期调用序列（含组件名、方法名、触发原因）。
    - `component_tree`：组件层级关系的字符串描述，例如 `Parent → Child1, Child2`。
    - `summary`：简短总结。

- 运行流程：
  - 读取 `input.txt` 到字符串 `scene_text`。
  - 检索向量库，格式化片段为 `context`。
  - 用 `PromptTemplate` 组合 `context` 与 `question`，交给 LLM 生成 JSON。

## 示例输入（input.txt）
你可以在 `input.txt` 编写组件与交互场景，例如首次加载父子组件、按钮切换子组件显隐等。脚本会基于检索到的 ArkUI 文档片段，输出调用顺序与原因说明。

## 其他脚本
- `ReAct.py`
  - 作用：演示 ReAct 代理如何用工具（如 `serpapi`）获取网页内容并回答问题。
  - 运行：`python ReAct.py`
- `Plan_n_Execute.py`
  - 作用：演示先规划后执行的智能体，适合多步骤需求。
  - 运行：`python Plan_n_Execute.py`
- `arkUI.ipynb`
  - 作用：Notebook 形式的 RAG 演示，便于交互式探索与可视化。

## 常见问题
- 向量库不存在或为空：
  - 先执行一次 `index_pdf_documents()` 进行索引；确保 PDF 路径正确。
- 报错未设置密钥：
  - 检查 `.env` 中的 `OPENAI_API_KEY` 与（可选）`SERPAPI_API_KEY`。
- 输出不是有效 JSON：
  - 设定 `temperature=0`，保证模板约束；或提高 `retriever_k` 与优化 `chunk_size/chunk_overlap`，提升检索质量。
- 检索速度慢或噪声多：
  - 减小 `retriever_k` 或 `chunk_overlap`；适当调小 `chunk_size`。

## 调参与建议
- 初学者建议：`chunk_size=1000`、`chunk_overlap=200`、`retriever_k=4`、`temperature=0`。
- 若答案缺上下文：增加 `retriever_k`，或增大 `chunk_size/overlap`。
- 若结果冗余：减小 `retriever_k/overlap`。

—— 祝你用 RAG 快速梳理 ArkUI 自定义组件的生命周期！