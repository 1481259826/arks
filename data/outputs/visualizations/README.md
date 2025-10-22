# Visualizations 目录

本目录包含 TypeScript 生成的 Graphviz DOT 可视化文件。

## 📁 文件说明

- **`.dot` 文件**：Graphviz 图形描述文件，描述 ArkUI 生命周期调用图结构
- **`.png` / `.svg` 文件**：由 DOT 文件生成的可视化图片（需要 Graphviz）

## 🚀 快速使用

### 方法 1：在线可视化（无需安装）

1. 打开 https://dreampuf.github.io/GraphvizOnline/
2. 复制 `.dot` 文件内容
3. 粘贴到网页左侧编辑器
4. 右侧自动显示可视化结果
5. 点击下载按钮保存图片

### 方法 2：使用 Graphviz（推荐）

**安装 Graphviz**：
```bash
# Windows (使用 Chocolatey)
choco install graphviz

# macOS
brew install graphviz

# Linux (Ubuntu/Debian)
sudo apt-get install graphviz
```

**生成图片**：
```bash
# 进入此目录
cd data/outputs/visualizations

# 生成 PNG 图片
dot -Tpng output1.dot -o output1.png

# 生成 SVG 图片（矢量，推荐）
dot -Tsvg output1.dot -o output1.svg

# 生成高分辨率 PNG
dot -Tpng -Gdpi=300 output1.dot -o output1_hires.png
```

**批量生成所有 DOT 文件**：
```bash
# Windows (PowerShell)
Get-ChildItem *.dot | ForEach-Object { dot -Tsvg $_.Name -o ($_.BaseName + ".svg") }

# Linux/macOS
for file in *.dot; do dot -Tsvg "$file" -o "${file%.dot}.svg"; done
```

## 📖 详细指南

查看完整的可视化使用指南：[../../docs/DOT_VISUALIZATION_GUIDE.md](../../docs/DOT_VISUALIZATION_GUIDE.md)

包含：
- DOT 文件格式说明
- Graphviz 详细安装指南
- 多种输出格式选项
- 自定义样式方法
- 常见问题解答

## 🎨 示例

假设你有 `output1.dot` 文件，可以这样使用：

**查看 DOT 文件内容**：
```bash
cat output1.dot
```

**生成可视化**：
```bash
# 生成 SVG（矢量图，可缩放）
dot -Tsvg output1.dot -o output1.svg

# 生成 PNG（位图）
dot -Tpng output1.dot -o output1.png

# 生成 PDF（适合打印）
dot -Tpdf output1.dot -o output1.pdf
```

**查看图片**：
```bash
# Windows
start output1.png

# macOS
open output1.svg

# Linux
xdg-open output1.png
```

## 🔍 理解调用图

生成的可视化图展示了：

- **节点**：ArkUI 生命周期函数（如 `aboutToAppear`、`build`、`onDidBuild`）
- **边（箭头）**：调用顺序（A → B 表示 A 执行后触发 B）
- **颜色**：
  - 浅绿色：`component` 作用域
  - 浅蓝色：`page` 作用域（如果有）
- **说明框**：动态行为描述

## 💡 提示

- **SVG 格式**优于 PNG：矢量图可无限缩放，文件更小
- **在线工具**适合快速查看，无需安装软件
- **本地 Graphviz** 适合批量处理和自定义样式
- 图片可以嵌入到文档、PPT、技术博客中

## 🔗 相关命令

```bash
# 从项目根目录生成 DOT 文件
npm run visualize

# 查看所有 DOT 文件
ls *.dot

# 查看 DOT 文件内容
cat output1.dot
```

---

**Happy Visualizing! 🎨**
