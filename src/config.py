"""
配置管理模块
"""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """RAG 系统配置类"""

    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置

        Args:
            config_file: YAML 配置文件路径，如果为 None 则使用默认配置
        """
        # 项目根目录
        self.project_root = Path(__file__).parent.parent

        # 默认配置
        self.vector_store_path = self.project_root / "vector_store"
        self.input_file = self.project_root / "data" / "inputs" / "input.txt"
        self.output_dir = self.project_root / "data" / "outputs" / "json"
        self.visualization_dir = self.project_root / "data" / "outputs" / "visualizations"
        self.pdf_path = self.project_root / "data" / "docs" / "arkUI自定义组件生命周期.pdf"

        # LLM 配置
        self.model_name = "deepseek-chat"
        self.temperature = 0

        # API 配置 - 支持从环境变量读取
        self.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("DEEPSEEK_BASE_URL") or os.getenv("OPENAI_BASE_URL")

        # 文档处理配置
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.retriever_k = 4

        # 如果提供了配置文件，加载并覆盖默认配置
        if config_file and os.path.exists(config_file):
            self.load_from_yaml(config_file)

    def load_from_yaml(self, config_file: str):
        """从 YAML 文件加载配置"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)

        # 更新配置
        for key, value in config_data.items():
            if hasattr(self, key):
                # 路径类型转换
                if 'path' in key or 'file' in key or 'dir' in key:
                    setattr(self, key, Path(value))
                else:
                    setattr(self, key, value)

    def to_dict(self):
        """转换为字典"""
        return {
            "vector_store_path": str(self.vector_store_path),
            "input_file": str(self.input_file),
            "output_dir": str(self.output_dir),
            "pdf_path": str(self.pdf_path),
            "model_name": self.model_name,
            "temperature": self.temperature,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "retriever_k": self.retriever_k,
        }


# 提示词模板
PROMPT_TEMPLATE = """你是一位精通 HarmonyOS ArkTS 生命周期机制的专家，现需要从 ArkTS 示例代码中解析并提取所有相关生命周期函数。

请参阅以下参考文档和代码示例：
- 参考文档片段提供于下方，标记为 {context}。
- ArkTS 示例代码提供于下方，标记为 {question}。

任务要求如下：
1. 严格输出 JSON 格式，不包含任何附加文字。

2. **需要提取的函数包括但不限于**：
   - 生命周期回调函数：aboutToAppear、aboutToDisappear、onPageShow、onPageHide 等
   - UI 构建方法：build（必须包含）
   - 其他状态管理相关方法

3. 参考以下 JSON 结构格式：
```
{{
  "lifecycle": {{
    "functions": [
      {{
        "name": "函数名（如 aboutToAppear、build）",
        "scope": "page 或 component 或 both",
        "description": "简要说明触发时机和作用"
      }}
    ],
    "order": [
      {{
        "pred": "组件名.函数名",
        "succ": "组件名.函数名"
      }}
    ],
    "dynamicBehavior": "说明动态情况下（如条件渲染、状态切换）生命周期的调用变化"
  }}
}}
```

4. **关于 functions 列表**：
   - 只列出**出现过的函数类型**，无需区分具体组件
   - 例如：代码中有 Parent.aboutToAppear 和 Child.aboutToAppear，functions 中只需列出一个 aboutToAppear
   - 如果某个函数在 page 和 component 中都出现，scope 填写 "both"

5. **关于 order 列表（重要）**：
   - 使用**有向边**表示函数调用的先后关系
   - 每个对象包含两个字段：pred（前驱函数）和 succ（后继函数）
   - 必须使用 "组件名.函数名" 格式（如 Parent.aboutToAppear）
   - 按照实际执行顺序，将相邻的两个函数调用组成一对
   - 例如：执行顺序是 A → B → C，则 order 为 [{{pred: A, succ: B}}, {{pred: B, succ: C}}]
   - 默认情况下，列出应用正常启动到关闭的顺序

  **关键规则 - aboutToDisappear 执行顺序**：
   - ⚠️ 组件删除顺序：严格按照"从父到子"的顺序执行
   - ⚠️ 正确顺序：Parent.aboutToDisappear → Child.aboutToDisappear
   - ❌ 错误顺序：Child.aboutToDisappear → Parent.aboutToDisappear（这是错误的！）
   - 示例：应用退出时，父组件 Parent 的 aboutToDisappear 必须先于子组件 Child 的 aboutToDisappear 执行

6. 关于 build 函数的说明：
   - build 是 UI 声明式构建的核心方法，每次状态变化都可能触发重新执行
   - 必须在输出中体现其首次执行和后续更新的时机

7. 输出时仅提供 JSON 结果。
"""
