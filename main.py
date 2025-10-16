"""
ArkUI 生命周期分析 RAG 系统 - 主入口
"""

import argparse
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.config import Config
from src.vectorstore import VectorStoreManager
from src.rag_engine import RAGEngine
from src.utils import read_input_file, save_output, print_banner


def index_documents(config: Config, force: bool = False):
    """
    索引 PDF 文档

    Args:
        config: 配置对象
        force: 是否强制重新索引
    """
    print_banner("PDF 文档索引")

    vectorstore_manager = VectorStoreManager(
        persist_directory=config.vector_store_path
    )

    vectorstore_manager.load_and_index_pdf(
        pdf_path=config.pdf_path,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        force_reindex=force
    )

    print("✅ 索引创建完成！")


def analyze_lifecycle(config: Config, input_file: Path = None, output_file: str = None):
    """
    执行生命周期分析

    Args:
        config: 配置对象
        input_file: 输入文件路径（可选）
        output_file: 输出文件名（可选）
    """
    print_banner("ArkUI 生命周期分析 RAG 系统")

    try:
        # 1. 读取输入
        input_path = input_file or config.input_file
        scene_text = read_input_file(input_path)

        # 2. 初始化向量库管理器
        vectorstore_manager = VectorStoreManager(
            persist_directory=config.vector_store_path
        )
        vectorstore_manager.load_vectorstore()

        # 3. 创建 RAG 引擎
        rag_engine = RAGEngine(
            vectorstore_manager=vectorstore_manager,
            model_name=config.model_name,
            temperature=config.temperature,
            retriever_k=config.retriever_k
        )

        # 4. 执行分析
        result = rag_engine.analyze(
            scene_text,
            api_key=config.api_key,
            api_base=config.api_base
        )

        # 5. 输出结果
        print("=" * 60)
        print("📜 生命周期调用顺序分析结果")
        print("=" * 60)
        print(result)
        print()

        # 6. 保存结果
        save_output(result, config.output_dir, output_file)

    except FileNotFoundError as e:
        print(f"\n❌ 文件错误: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ 数据错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 执行失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 命令行参数解析
    parser = argparse.ArgumentParser(
        description="ArkUI 生命周期分析 RAG 系统",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # 索引命令
    index_parser = subparsers.add_parser("index", help="索引 PDF 文档")
    index_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="强制重新索引"
    )
    index_parser.add_argument(
        "--config", "-c",
        type=str,
        help="配置文件路径"
    )

    # 分析命令
    analyze_parser = subparsers.add_parser("analyze", help="执行生命周期分析")
    analyze_parser.add_argument(
        "--input", "-i",
        type=str,
        help="输入文件路径"
    )
    analyze_parser.add_argument(
        "--output", "-o",
        type=str,
        help="输出文件名"
    )
    analyze_parser.add_argument(
        "--config", "-c",
        type=str,
        help="配置文件路径"
    )

    args = parser.parse_args()

    # 如果没有指定命令，默认执行分析
    if args.command is None:
        args.command = "analyze"
        # 为默认命令添加默认属性
        args.input = None
        args.output = None
        args.config = None

    # 加载配置
    config_file = getattr(args, 'config', None)
    config = Config(config_file=config_file)

    # 执行命令
    if args.command == "index":
        index_documents(config, force=args.force)
    elif args.command == "analyze":
        input_file = Path(args.input) if args.input else None
        analyze_lifecycle(config, input_file=input_file, output_file=args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
