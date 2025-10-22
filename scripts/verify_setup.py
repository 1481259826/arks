"""
测试新系统的脚本
"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("🧪 ArkUI RAG 系统测试")
print("=" * 60)

# 测试 1: 导入模块
print("\n[1/5] 测试模块导入...")
try:
    from src.config import Config
    from src.vectorstore import VectorStoreManager
    from src.rag_engine import RAGEngine
    from src.utils import read_input_file, print_banner
    print("✅ 所有模块导入成功")
except Exception as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

# 测试 2: 配置加载
print("\n[2/5] 测试配置加载...")
try:
    config = Config()
    print(f"✅ 配置加载成功")
    print(f"   - 模型: {config.model_name}")
    print(f"   - 向量库路径: {config.vector_store_path}")
    print(f"   - API Key: {'已设置' if config.api_key else '未设置'}")
    print(f"   - API Base: {config.api_base if config.api_base else '默认'}")
except Exception as e:
    print(f"❌ 配置加载失败: {e}")
    sys.exit(1)

# 测试 3: 向量库加载
print("\n[3/5] 测试向量库加载...")
try:
    vectorstore_manager = VectorStoreManager(
        persist_directory=config.vector_store_path
    )
    vectorstore = vectorstore_manager.load_vectorstore()
    print("✅ 向量库加载成功")
except FileNotFoundError as e:
    print(f"⚠️  向量库不存在: {e}")
    print("   请先运行: python main.py index")
    sys.exit(1)
except Exception as e:
    print(f"❌ 向量库加载失败: {e}")
    sys.exit(1)

# 测试 4: 输入文件读取
print("\n[4/5] 测试输入文件读取...")
try:
    scene_text = read_input_file(config.input_file)
    print(f"✅ 输入文件读取成功")
    print(f"   - 文件: {config.input_file}")
    print(f"   - 长度: {len(scene_text)} 字符")
except Exception as e:
    print(f"❌ 输入文件读取失败: {e}")
    sys.exit(1)

# 测试 5: RAG 引擎初始化
print("\n[5/5] 测试 RAG 引擎初始化...")
try:
    rag_engine = RAGEngine(
        vectorstore_manager=vectorstore_manager,
        model_name=config.model_name,
        temperature=config.temperature,
        retriever_k=config.retriever_k
    )
    print("✅ RAG 引擎初始化成功")
except Exception as e:
    print(f"❌ RAG 引擎初始化失败: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 所有测试通过！系统已准备就绪。")
print("=" * 60)
print("\n💡 运行分析:")
print("   python main.py analyze")
print("\n💡 或使用简化命令:")
print("   python main.py")
