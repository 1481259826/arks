# 文档索引

欢迎查看 ArkUI 生命周期分析 RAG 系统的文档。本目录包含项目的所有技术文档。

## 📚 文档结构

### 用户文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [../README.md](../README.md) | **项目主文档** - 快速开始、完整工作流程、API 参考 | 所有用户 ⭐ |
| [DOT_VISUALIZATION_GUIDE.md](DOT_VISUALIZATION_GUIDE.md) | **可视化指南** - 使用 DOT 文件生成调用图图片 | 所有用户 |
| [TYPESCRIPT_USAGE.md](TYPESCRIPT_USAGE.md) | TypeScript 模块详细使用指南（已合并到主 README） | TypeScript 用户 |

### 开发者文档

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [../CLAUDE.md](../CLAUDE.md) | **Claude Code 开发指南** - 项目架构、模块说明、开发规范（必须在根目录） | 贡献者、AI 助手 |
| [API_REFERENCE.md](API_REFERENCE.md) | **TypeScript API 完整参考** - 类型定义、方法签名、示例 | 高级开发者 |

### 测试与变更

| 文档 | 说明 | 适合人群 |
|------|------|----------|
| [TEST_RESULTS.md](TEST_RESULTS.md) | **完整测试报告** - 功能验证、性能统计、已修复问题 | 测试人员、用户 |
| [CHANGELOG.md](CHANGELOG.md) | **版本变更记录** - 新功能、Bug 修复、重大变更 | 所有用户 |

---

## 🚀 快速导航

### 我想...

**开始使用项目**
→ 阅读 [主 README](../README.md) 的"快速开始"部分

**生成可视化图片**
→ 阅读 [DOT_VISUALIZATION_GUIDE.md](DOT_VISUALIZATION_GUIDE.md) 了解如何使用 `.dot` 文件

**了解项目架构**
→ 阅读 [../CLAUDE.md](../CLAUDE.md) 的"架构"部分

**查看 TypeScript API**
→ 阅读 [API_REFERENCE.md](API_REFERENCE.md)

**了解最新变更**
→ 阅读 [CHANGELOG.md](CHANGELOG.md)

**查看测试结果**
→ 阅读 [TEST_RESULTS.md](TEST_RESULTS.md)

**使用 TypeScript 模块**
→ 阅读 [主 README](../README.md) 的"Part 2: TypeScript 调用图分析"部分

---

## 📖 文档详细说明

### 主 README（../README.md）

**主要内容**：
- 环境准备（Python + TypeScript）
- 项目结构
- 快速开始
  - Part 1: Python RAG 分析
  - Part 2: TypeScript 调用图分析
- 完整工作流程
- 配置说明
- API 参考（Python + TypeScript）
- 常见问题
- 架构说明

**何时阅读**：首次使用项目时必读

---

### CLAUDE.md - Claude Code 开发指南

**位置**：`../CLAUDE.md`（必须在项目根目录）

**主要内容**：
- 项目概述
- 关键命令
- 模块化架构详解
  - `src/config.py` - 配置管理
  - `src/vectorstore.py` - 向量库操作
  - `src/rag_engine.py` - RAG 核心逻辑
  - `src/utils.py` - 工具函数
  - `main.py` - CLI 接口
- 数据流说明
- 配置系统
- 输出格式
- 参数调优建议
- 遗留代码说明

**何时阅读**：
- 需要修改或扩展 Python 后端时
- 想深入理解 RAG 系统架构时
- 作为 AI 助手（如 Claude Code）协作时

**重要说明**：此文件必须保持在项目根目录，Claude Code 会自动读取它作为项目指南

---

### API_REFERENCE.md - TypeScript API 参考

**主要内容**：
- 完整的 TypeScript API 文档
- 类型定义详解
  - `LifecycleFunction`
  - `CallOrder`
  - `LifecycleAnalysis`
  - `LifecycleResult`
- `LifecycleParser` 类方法
- `CallGraph` 类方法
  - 节点操作
  - 边操作
  - 图分析算法
  - 导入导出
- 使用示例
- 错误处理
- 算法说明（Kahn、BFS）

**何时阅读**：
- 需要使用 TypeScript 模块的所有方法时
- 想了解算法实现细节时
- 需要类型定义参考时

---

### TYPESCRIPT_USAGE.md - TypeScript 使用指南

**主要内容**：
- 快速开始
- 使用场景（5 个典型场景）
- 与 Python RAG 系统集成
- NPM 脚本参考
- API 快速参考表
- 常见问题

**何时阅读**：
- 专注于 TypeScript 模块的使用
- 需要场景化的示例代码

**注意**：此文档的内容已合并到主 README.md，保留此文件供参考。

---

### TEST_RESULTS.md - 测试报告

**主要内容**：
- 测试时间和目的
- 测试用例（5 个）
  1. Python 分析生成 JSON
  2. TypeScript 解析 JSON
  3. TypeScript 可视化生成 DOT
  4. 目录结构验证
  5. 完整工作流验证
- JSON 格式验证
- 性能统计
- 已修复的问题
  1. 函数名重复
  2. 目录混乱
  3. Windows 编码错误
- 功能验证清单

**何时阅读**：
- 想了解系统测试覆盖率时
- 验证功能是否正常时
- 查看已知问题的修复方案时

---

### CHANGELOG.md - 版本变更记录

**主要内容**：
- 按版本组织的变更日志
- 新功能
- Bug 修复
- 重大变更（Breaking Changes）
- 性能优化
- 文档更新

**何时阅读**：
- 升级版本前
- 想了解项目演进历史时
- 查找特定功能何时引入时

---

## 🔧 文档维护

### 更新文档时

1. **主 README** (`../README.md`) - 更新用户可见的功能、API、使用方法
2. **CLAUDE.md** - 更新架构说明、模块实现细节
3. **API_REFERENCE.md** - 更新 TypeScript API 变更
4. **TEST_RESULTS.md** - 添加新的测试结果
5. **CHANGELOG.md** - 记录版本变更

### 文档规范

- 使用 Markdown 格式
- 包含目录导航（长文档）
- 代码示例使用语法高亮
- 重要信息使用表格或列表
- 保持中文文档的一致性

---

## 📝 反馈

如有文档问题或改进建议，欢迎提交 Issue！
