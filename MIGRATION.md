# 迁移指南

## 从旧版本迁移到新的模块化结构

本文档帮助你从旧的 `arkui_lifecycle_rag.py` 迁移到新的模块化结构。

## 主要变化

### 1. 目录结构变化

**旧结构**：
```
arkUI/
├── arkui_lifecycle_rag.py
├── arkUI自定义组件生命周期.pdf
├── input.txt
├── lifecycle_analysis_output.txt
└── vector_store/
```

**新结构**：
```
arkUI/
├── src/                    # 新增：源代码模块
│   ├── config.py
│   ├── rag_engine.py
│   ├── vectorstore.py
│   └── utils.py
├── data/                   # 新增：数据目录
│   ├── docs/              # PDF 文档
│   ├── inputs/            # 输入文件
│   └── outputs/           # 输出结果
├── main.py                # 新增：主入口
├── config.yaml            # 新增：配置文件
├── requirements.txt       # 新增：依赖管理
├── .env.example           # 新增：环境变量示例
├── .gitignore             # 新增：Git 忽略文件
└── arkui_lifecycle_rag.py # 保留：向后兼容
```

### 2. 使用方式变化

**旧方式**：
```bash
# 首次索引（需要编辑代码取消注释）
python arkui_lifecycle_rag.py

# 正常运行（需要编辑代码恢复注释）
python arkui_lifecycle_rag.py
```

**新方式**：
```bash
# 首次索引（无需编辑代码）
python main.py index

# 正常运行
python main.py analyze
# 或
python main.py
```

### 3. 配置方式变化

**旧方式** - 在代码中硬编码：
```python
CONFIG = {
    "vector_store_path": "./vector_store",
    "input_file": "input.txt",
    "model_name": "deepseek-chat",
    ...
}
```

**新方式** - 使用 YAML 配置文件：
```yaml
# config.yaml
vector_store_path: "./vector_store"
input_file: "./data/inputs/input.txt"
model_name: "deepseek-chat"
...
```

## 迁移步骤

### 步骤 1：检查现有数据

确认你现有的文件位置：
- PDF 文档在哪里？
- 输入文件在哪里？
- 是否已经创建了 vector_store？

### 步骤 2：文件已自动迁移

如果你运行了优化脚本，文件已经自动移动到新位置：
- PDF → `data/docs/`
- 输入文件 → `data/inputs/`
- 输出文件 → `data/outputs/`
- Notebook → `notebooks/`

### 步骤 3：安装依赖（如果还没有）

```bash
pip install -r requirements.txt
```

### 步骤 4：配置环境变量

```bash
cp .env.example .env
# 编辑 .env，添加你的 OPENAI_API_KEY
```

### 步骤 5：测试新系统

如果向量库已存在，直接测试分析：
```bash
python main.py analyze
```

如果需要重新索引：
```bash
python main.py index --force
```

## 功能对照表

| 功能 | 旧方式 | 新方式 |
|------|--------|--------|
| 首次索引 | 编辑代码取消注释 `index_pdf_documents()` | `python main.py index` |
| 正常分析 | 编辑代码确保调用 `main()` | `python main.py` 或 `python main.py analyze` |
| 修改配置 | 编辑 `CONFIG` 字典 | 编辑 `config.yaml` |
| 自定义输入 | 修改 `CONFIG["input_file"]` | `python main.py analyze --input path/to/file` |
| 自定义输出 | 修改代码中的文件名 | `python main.py analyze --output filename.txt` |

## 优势

新的模块化结构提供了以下优势：

1. **更清晰的代码组织**：配置、核心逻辑、工具函数分离
2. **更好的可维护性**：每个模块职责单一
3. **更灵活的配置**：YAML 文件 + 命令行参数
4. **更友好的使用**：无需编辑代码，使用命令行即可
5. **更好的项目管理**：.gitignore、requirements.txt、目录分离

## 向后兼容

旧的 `arkui_lifecycle_rag.py` 仍然保留，可以继续使用：

```bash
python arkui_lifecycle_rag.py
```

但建议尽快迁移到新的模块化结构以享受更好的开发体验。

## 常见问题

### Q: 我的 vector_store 还能用吗？
A: 可以！向量库位置没有变化，新系统会自动使用现有的向量库。

### Q: 我需要重新索引吗？
A: 不需要。如果 `vector_store/` 目录存在且有数据，可以直接运行分析。

### Q: 旧的输入文件还能用吗？
A: 可以。文件已经移动到 `data/inputs/`，新系统会自动找到。你也可以用 `--input` 参数指定任意路径。

### Q: 我可以继续使用旧脚本吗？
A: 可以，但不推荐。新系统功能更强大，使用更方便。

### Q: 如何自定义配置？
A: 编辑 `config.yaml` 文件，或者创建新的 YAML 文件并用 `--config` 参数指定。

## 需要帮助？

如果迁移过程中遇到问题，请查看：
- `README.md` - 完整的使用说明
- `CLAUDE.md` - 架构和实现细节
- 或提交 Issue 反馈问题
