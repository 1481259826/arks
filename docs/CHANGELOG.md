# 更新日志

## 2025-10-22 - 目录结构优化

### 🗂️ Outputs 目录重组

**问题**：`data/outputs/` 目录混乱，包含多种文件类型
**解决方案**：创建分类子目录结构

**新的目录结构**：
```
data/outputs/
├── json/              # Python 生成的 JSON 文件
├── visualizations/    # TypeScript 生成的 DOT 文件
├── legacy/           # 旧的 .txt 文件
└── archives/         # 归档和临时文件
```

**工具**：
- 新增 `scripts/organize_outputs.py` - 自动整理文件脚本
- 支持预览模式 (`--dry-run`)
- 智能分类文件到对应目录

**配置更新**：
- Python 默认输出到 `data/outputs/json/`
- TypeScript 默认输出到 `data/outputs/visualizations/`
- 添加 `.gitignore` 和 `.gitkeep` 保持目录结构

---

## 2025-10-22 - 修复函数名重复问题

### 🐛 问题修复

**问题**：`functions` 数组中的函数名包含组件实例前缀（如 `SimpleDemo.aboutToAppear`），导致相同基础函数重复出现。

**解决方案**：
- `functions` 数组只保留**唯一的基础函数名**（如 `aboutToAppear`）
- `order` 数组保留**完整的实例名**（如 `SimpleDemo.aboutToAppear`）
- TypeScript 解析器自动映射实例名到基础函数

**示例格式**：
```json
{
  "lifecycle": {
    "functions": [
      {"name": "aboutToAppear", "scope": "component", "description": "..."},
      {"name": "build", "scope": "component", "description": "..."}
    ],
    "order": [
      {"pred": "SimpleDemo.aboutToAppear", "succ": "SimpleDemo.build"},
      {"pred": "SimpleDemo.build", "succ": "SimpleChild.aboutToAppear"}
    ]
  }
}
```

---

## 2025-10-22 - JSON 输出格式改进

### 🎯 主要变更

**Python 后端现在直接输出 .json 文件**
- 之前：输出 `.txt` 文件，包含 markdown 代码块包裹的 JSON
- 现在：直接输出格式化的 `.json` 文件

### ✨ 新功能

1. **自动 JSON 提取和格式化** (`src/utils.py`)
   - `extract_json_from_markdown()`: 从 markdown 代码块中提取 JSON
   - `normalize_json_format()`: 标准化 JSON 格式
   - `extract_function_instances()`: 处理实例化的函数名
   - `parse_function_name()`: 解析函数基础名称

2. **智能格式转换**
   - 自动将 `scope: "both"` 转换为 `scope: "component"`
   - 移除额外的 `type` 字段（如果存在）
   - 处理实例化函数名（如 `Component.method`）

3. **Windows 终端编码修复** (`src/utils.py`)
   - 新增 `safe_print()` 函数
   - 优雅处理 Unicode 字符（emoji、中文）
   - 避免 Windows cmd 的 cp1252 编码错误

### 🔧 技术细节

**实例化函数名处理**：
- LLM 输出包含实例名（如 `SimpleDemo.aboutToAppear`）
- 标准化函数自动展开为每个实例创建独立节点
- 保持元数据（scope、description）一致性

**文件命名约定**：
- 默认文件名：`lifecycle_analysis_YYYYMMDD_HHMMSS.json`
- 自动添加 `.json` 扩展名（即使用户指定了其他扩展名）

### 📦 兼容性

**向后兼容**：
- 旧的 `.txt` 文件仍然可以通过 TypeScript 转换器处理
- 使用 `npm run convert` 批量转换旧格式

**TypeScript 集成**：
- Python 输出的 JSON 可直接被 TypeScript 解析器加载
- 无需额外转换步骤

### 🚀 使用示例

```bash
# Python 分析（直接输出 JSON）
conda activate CreatPPT
python main.py analyze

# 指定输出文件名
python main.py analyze --output my_analysis.json

# TypeScript 可视化
npm run visualize
```

### 📝 文件结构变化

**生成的文件**：
```
data/outputs/
├── lifecycle_analysis_20251022_123456.json  # 新格式（JSON）
├── lifecycle_analysis_20251016_183649.txt   # 旧格式（保留）
└── lifecycle_analysis_20251016_183649.json  # 转换后（可选）
```

### 🐛 修复的问题

1. Windows 终端 Unicode 编码错误
2. JSON 解析失败时的错误处理
3. 实例化函数名与函数定义不匹配的问题

### 🔄 迁移指南

**从旧版本迁移**：
1. 旧的 `.txt` 文件仍然有效
2. 运行 `npm run convert` 转换为新格式
3. 新的分析将自动使用 JSON 格式

**代码更改**：
- 无需修改现有代码
- 所有模块已更新使用 `safe_print()`
- JSON 格式自动标准化
