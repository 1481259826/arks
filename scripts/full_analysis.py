#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端分析脚本：从 input.txt 直接生成 DOT 可视化文件

工作流程：
1. 运行 Python RAG 分析生成 JSON
2. 自动调用 TypeScript 生成 DOT 文件
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# 设置 UTF-8 编码（Windows 兼容性）
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from src.config import Config
from src.vectorstore import VectorStoreManager
from src.rag_engine import RAGEngine
from src.utils import read_input_file, save_output, print_banner, safe_print


def run_python_analysis(config: Config, input_file: Path = None, output_file: str = None):
    """
    步骤 1: 运行 Python RAG 分析生成 JSON

    Returns:
        生成的 JSON 文件路径
    """
    print_banner("步骤 1/2: Python RAG 分析")

    # 读取输入文件
    input_path = input_file or config.input_file
    safe_print(f"📖 读取输入文件: {input_path}")
    scenario = read_input_file(input_path)

    # 初始化 RAG 引擎
    safe_print("🔧 初始化 RAG 引擎...")
    vectorstore_manager = VectorStoreManager(
        persist_directory=config.vector_store_path
    )

    vectorstore = vectorstore_manager.load_vectorstore()

    rag_engine = RAGEngine(
        vectorstore_manager=vectorstore_manager,
        model_name=config.model_name,
        temperature=config.temperature,
        retriever_k=config.retriever_k
    )

    # 构建 RAG 链
    rag_engine.build_chain()

    # 执行分析
    safe_print("🚀 开始分析...")
    result = rag_engine.analyze(scenario)

    # 保存输出
    from pathlib import Path as PathLib
    output_dir = PathLib(config.output_dir)
    json_path = save_output(result, output_dir, output_file)
    safe_print(f"✅ JSON 文件已保存: {json_path}")

    return json_path


def run_typescript_visualization(json_path: Path):
    """
    步骤 2: 调用 TypeScript 生成 DOT 文件

    Args:
        json_path: JSON 文件路径
    """
    print_banner("步骤 2/2: TypeScript 可视化")

    safe_print(f"📄 输入 JSON: {json_path}")
    safe_print("🎨 生成 DOT 可视化文件...")

    try:
        # Windows 上需要使用 npm.cmd
        npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

        # 运行 npm run visualize
        result = subprocess.run(
            [npm_cmd, "run", "visualize"],
            check=True,
            capture_output=True,
            text=True,
            shell=(sys.platform == "win32")  # Windows 需要 shell=True
        )

        # 显示输出
        if result.stdout:
            print(result.stdout)

        safe_print("✅ DOT 文件生成完成！")

        # 推导 DOT 文件路径
        json_basename = json_path.stem  # 不带扩展名的文件名
        dot_path = Path("data/outputs/visualizations") / f"{json_basename}.dot"

        if dot_path.exists():
            safe_print(f"📊 DOT 文件位置: {dot_path}")
            safe_print("\n💡 生成图片命令:")
            safe_print(f"   dot -Tpng {dot_path} -o {dot_path.with_suffix('.png')}")

    except subprocess.CalledProcessError as e:
        safe_print(f"❌ TypeScript 可视化失败: {e}")
        if e.stderr:
            safe_print(f"错误信息: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        safe_print("❌ npm 命令未找到，请确保已安装 Node.js 和 npm")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="端到端分析：从 input.txt 直接生成 DOT 可视化文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 使用默认输入文件 (data/inputs/input.txt)
  python scripts/full_analysis.py

  # 指定输入文件
  python scripts/full_analysis.py --input data/inputs/input1.txt

  # 指定输出文件名
  python scripts/full_analysis.py --output my_test

  # 使用自定义配置
  python scripts/full_analysis.py --config custom_config.yaml
        """
    )

    parser.add_argument(
        "--input",
        type=Path,
        help="输入文件路径 (默认: data/inputs/input.txt)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="输出文件名（不含扩展名，默认: lifecycle_analysis_时间戳）"
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="配置文件路径 (默认: config.yaml)"
    )

    args = parser.parse_args()

    # 加载环境变量
    load_dotenv()

    # 加载配置
    config = Config()
    if args.config:
        config.load_from_yaml(args.config)

    print_banner("ArkUI 端到端生命周期分析")
    safe_print("从 ArkTS 代码生成调用图可视化\n")

    # 步骤 1: Python 分析生成 JSON
    json_path = run_python_analysis(config, args.input, args.output)

    # 步骤 2: TypeScript 生成 DOT
    run_typescript_visualization(json_path)

    # 完成
    print_banner("分析完成")
    safe_print("🎉 成功生成 JSON 和 DOT 文件！")
    safe_print("\n📁 输出位置:")
    safe_print(f"   JSON: {json_path}")
    safe_print(f"   DOT:  data/outputs/visualizations/{json_path.stem}.dot")


if __name__ == "__main__":
    main()
