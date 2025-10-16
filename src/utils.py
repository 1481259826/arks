"""
工具函数模块
"""

from pathlib import Path
from typing import List
from datetime import datetime


def read_input_file(filepath: Path) -> str:
    """
    读取输入文件

    Args:
        filepath: 文件路径

    Returns:
        文件内容

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件为空
    """
    if not filepath.exists():
        raise FileNotFoundError(f"未找到输入文件：{filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    if not content:
        raise ValueError(f"输入文件为空：{filepath}")

    print(f"✅ 已读取输入文件: {filepath}")
    print(f"📝 内容预览:\n{content[:200]}{'...' if len(content) > 200 else ''}\n")
    return content


def save_output(content: str, output_dir: Path, filename: str = None) -> Path:
    """
    保存输出结果

    Args:
        content: 输出内容
        output_dir: 输出目录
        filename: 文件名，如果为 None 则自动生成

    Returns:
        输出文件路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lifecycle_analysis_{timestamp}.txt"

    output_file = output_dir / filename

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"💾 结果已保存到: {output_file}")
    return output_file


def format_docs(docs: List) -> str:
    """
    格式化文档为字符串

    Args:
        docs: 文档列表

    Returns:
        格式化后的文档内容
    """
    formatted = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get('source', '未知')
        page = doc.metadata.get('page', '?')
        formatted.append(f"[片段 {i} - 来源: {source}, 页: {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(formatted)


def print_banner(title: str, width: int = 60):
    """
    打印横幅

    Args:
        title: 标题
        width: 宽度
    """
    print("=" * width)
    print(f"🚀 {title}")
    print("=" * width)
