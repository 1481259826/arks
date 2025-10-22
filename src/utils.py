"""
工具函数模块
"""

import json
import re
import sys
from pathlib import Path
from typing import List
from datetime import datetime


def safe_print(text: str):
    """
    安全地打印文本，处理 Windows 终端编码问题

    Args:
        text: 要打印的文本
    """
    try:
        print(text)
    except (UnicodeEncodeError, UnicodeError):
        # 尝试使用 UTF-8 编码输出到 stdout
        try:
            sys.stdout.buffer.write(text.encode('utf-8'))
            sys.stdout.buffer.write(b'\n')
            sys.stdout.buffer.flush()
        except:
            # 最后的备选方案：移除所有非 ASCII 字符
            safe_text = text.encode('ascii', 'ignore').decode('ascii')
            print(safe_text)


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

    safe_print(f"✅ 已读取输入文件: {filepath}")
    safe_print(f"📝 内容预览:\n{content[:200]}{'...' if len(content) > 200 else ''}\n")
    return content


def extract_json_from_markdown(content: str) -> str:
    """
    从 markdown 代码块中提取 JSON 内容

    Args:
        content: 可能包含 markdown 代码块的内容

    Returns:
        提取的 JSON 字符串
    """
    # 尝试匹配 ```json ... ``` 或 ``` ... ``` 代码块
    pattern = r'```(?:json)?\s*\n([\s\S]*?)\n```'
    match = re.search(pattern, content)

    if match:
        return match.group(1).strip()

    # 如果没有代码块，返回原内容
    return content.strip()


def extract_function_instances(order: list) -> set:
    """
    从 order 数组中提取所有唯一的函数实例名

    Args:
        order: 调用顺序列表

    Returns:
        函数实例名集合
    """
    instances = set()
    for edge in order:
        if isinstance(edge, dict):
            if "pred" in edge:
                instances.add(edge["pred"])
            if "succ" in edge:
                instances.add(edge["succ"])
    return instances


def parse_function_name(full_name: str) -> str:
    """
    解析函数实例名，提取基础函数名
    例如: "SimpleDemo.aboutToAppear" -> "aboutToAppear"

    Args:
        full_name: 完整的函数实例名

    Returns:
        基础函数名
    """
    parts = full_name.split('.')
    return parts[-1] if parts else full_name


def normalize_json_format(json_data: dict) -> dict:
    """
    标准化 JSON 格式，移除额外字段，确保兼容性

    functions 数组只包含基础函数名（不带组件前缀）
    order 数组保留完整的实例名（带组件前缀）

    Args:
        json_data: 原始 JSON 数据

    Returns:
        标准化后的 JSON 数据
    """
    if "lifecycle" not in json_data:
        return json_data

    lifecycle = json_data["lifecycle"]

    # 标准化 functions - 只保留唯一的基础函数
    if "functions" in lifecycle:
        # 使用字典去重，保留第一次出现的函数定义
        unique_functions = {}

        for func in lifecycle["functions"]:
            # 获取基础函数名（去掉组件前缀）
            full_name = func.get("name", "")
            base_name = parse_function_name(full_name)

            # 如果这个基础函数还没有记录，添加它
            if base_name not in unique_functions:
                scope = func.get("scope", "component")
                # 确保 scope 是有效值
                if scope not in ["page", "component"]:
                    scope = "component" if scope == "both" else "component"

                unique_functions[base_name] = {
                    "name": base_name,  # 只使用基础名称
                    "scope": scope,
                    "description": func.get("description", "")
                }

        # 转换为列表，按名称排序
        lifecycle["functions"] = [
            unique_functions[name] for name in sorted(unique_functions.keys())
        ]

    # order 数组保持不变（保留完整的实例名）
    # 不需要修改 lifecycle["order"]

    return json_data


def save_output(content: str, output_dir: Path, filename: str = None) -> Path:
    """
    保存输出结果为 JSON 格式

    Args:
        content: 输出内容（可能包含 markdown 代码块的 JSON）
        output_dir: 输出目录
        filename: 文件名，如果为 None 则自动生成

    Returns:
        输出文件路径
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 生成文件名
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"lifecycle_analysis_{timestamp}.json"

    # 确保文件扩展名是 .json
    if not filename.endswith('.json'):
        filename = filename.rsplit('.', 1)[0] + '.json'

    output_file = output_dir / filename

    try:
        # 提取 JSON 内容
        json_str = extract_json_from_markdown(content)

        # 解析 JSON
        json_data = json.loads(json_str)

        # 标准化格式
        normalized_data = normalize_json_format(json_data)

        # 保存为格式化的 JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(normalized_data, f, ensure_ascii=False, indent=2)

        safe_print(f"💾 结果已保存到: {output_file} (JSON 格式)")

    except json.JSONDecodeError as e:
        # 如果 JSON 解析失败，回退到保存原始内容
        safe_print(f"⚠️  警告: JSON 解析失败 ({e})，保存原始内容")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        safe_print(f"💾 结果已保存到: {output_file} (原始格式)")

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
    safe_print("=" * width)
    safe_print(f"🚀 {title}")
    safe_print("=" * width)
