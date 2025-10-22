# Outputs 目录结构

本目录包含 ArkUI 生命周期分析系统的所有输出文件，已按类型分类整理。

## 📁 目录结构

```
data/outputs/
├── json/              # Python RAG 系统生成的 JSON 分析结果
│   └── lifecycle_analysis_YYYYMMDD_HHMMSS.json
├── visualizations/    # TypeScript 生成的 Graphviz DOT 可视化文件
│   └── lifecycle_analysis_YYYYMMDD_HHMMSS.dot
├── legacy/           # 旧版本的 .txt 格式文件（已弃用）
│   └── *.txt
└── archives/         # 归档和临时导出文件
    └── *_export.json
```

## 🔄 文件流程

### 1. Python 分析 → JSON 输出

```bash
conda activate CreatPPT
python main.py analyze --output my_analysis.json
# 输出: data/outputs/json/my_analysis.json
```

### 2. TypeScript 可视化 → DOT 文件

```bash
npm run visualize
# 读取: data/outputs/json/*.json
# 输出: data/outputs/visualizations/*.dot
```

### 3. 生成图片（可选）

```bash
# 生成所有可视化图片
cd data/outputs/visualizations
dot -Tpng *.dot -O

# 或单个文件
dot -Tpng my_analysis.dot -o my_analysis.png
```

## 🗂️ 整理现有文件

如果 `data/outputs/` 根目录有混乱的文件，运行整理脚本：

```bash
# 预览整理操作（不实际移动）
python scripts/organize_outputs.py --dry-run

# 实际整理
python scripts/organize_outputs.py
```

**整理规则**：
- `*.json` → `json/` 目录（或 `archives/` 如果是临时导出文件）
- `*.dot` → `visualizations/` 目录
- `*.txt` → `legacy/` 目录
- 其他文件保持不动

## 📝 文件命名规范

### Python 输出
- 默认：`lifecycle_analysis_YYYYMMDD_HHMMSS.json`
- 自定义：`python main.py analyze --output custom_name.json`

### TypeScript 可视化
- 自动命名：与源 JSON 文件同名，扩展名改为 `.dot`
- 示例：`my_analysis.json` → `my_analysis.dot`

## 🚫 Git 忽略规则

所有生成的文件都被 `.gitignore` 忽略，但保留目录结构：

```gitignore
json/*.json
visualizations/*.dot
legacy/*.txt
archives/*
```

## 🔧 维护建议

### 定期清理

```bash
# 删除 30 天前的文件
find data/outputs/json -name "*.json" -mtime +30 -delete
find data/outputs/visualizations -name "*.dot" -mtime +30 -delete
```

### 备份重要文件

```bash
# 备份到 archives 目录
cp data/outputs/json/important_analysis.json data/outputs/archives/
```

## 📊 统计信息

查看各目录的文件数量：

```bash
# Linux/macOS
find data/outputs -mindepth 1 -maxdepth 1 -type d -exec sh -c 'echo "$(basename {}): $(find {} -type f | wc -l) files"' \;

# Windows PowerShell
Get-ChildItem data/outputs -Directory | ForEach-Object { "$($_.Name): $((Get-ChildItem $_.FullName -File).Count) files" }
```

## ❓ 常见问题

### Q: 为什么要分离目录？
A: 保持文件类型清晰分离，便于管理和版本控制，避免根目录混乱。

### Q: 旧的 .txt 文件还能用吗？
A: 可以。使用 `npm run convert` 将 `legacy/*.txt` 转换为 `json/*.json`。

### Q: 如何恢复到单一目录结构？
A: 运行 `mv data/outputs/*/* data/outputs/` 将所有文件移回根目录（不推荐）。

## 🔗 相关命令

| 命令 | 说明 |
|------|------|
| `python main.py analyze` | 生成 JSON 到 `json/` |
| `npm run visualize` | 从 `json/` 生成 DOT 到 `visualizations/` |
| `npm run convert` | 转换 `legacy/*.txt` 到 `json/*.json` |
| `python scripts/organize_outputs.py` | 整理根目录文件 |
