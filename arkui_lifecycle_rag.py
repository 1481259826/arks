"""
ArkUI 自定义组件生命周期分析 RAG 系统
"""

from dotenv import load_dotenv
load_dotenv()

import os
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from typing import List

# ==================== 配置部分 ====================
CONFIG = {
    "vector_store_path": "./vector_store",
    "input_file": "input.txt",
    "model_name": "deepseek-chat", 
    "temperature": 0,
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "retriever_k": 4  # 检索的文档数量
}

# ==================== 提示词模板 ====================
PROMPT_TEMPLATE = """你是一位精通 HarmonyOS ArkTS 生命周期机制的专家，现需要从 ArkTS 示例代码中解析并提取所有相关生命周期函数。

请参阅以下参考文档和代码示例：
- 参考文档片段提供于下方，标记为 {context}。
- ArkTS 示例代码提供于下方，标记为 {question}。

任务要求如下：
1. 严格输出 JSON 格式，不包含任何附加文字。
2. 参考以下 JSON 结构格式：
```
{{
  "lifecycle": {{
    "functions": [
      {{
        "name": "函数名",
        "scope": "page 或 component",
        "description": "简要说明触发时机和作用"
      }}
    ],
    "order": [
      "函数调用顺序，按时间先后排列，例如 Parent.aboutToAppear → Child.aboutToAppear ..."
    ],
    "dynamicBehavior": "说明动态情况下（如条件渲染、状态切换）生命周期的调用变化"
  }}
}}

说明：
1. 一个functions列表：包含所有的生命周期函数方法，不用区分组件。
2. 一个order列表：包含所有的生命周期函数先后顺序，两个为一组，用pred和succ表示。
例如：共有三个生命周期函数，onCreate, onResume, onDestory
functions: [onCreate, onResume, onDestory]
order: [{{pred: onCreate, succ: onResume}}, {{pred: onResume, succ: onDestory}}]
```
3. 合并多个组件的生命周期：
- 将 Parent、Child 或其他组件中的生命周期函数统一输出。
- 使用 Parent.xxx 或 Child.xxx 区分函数所属组件。
- 请依据实际执行顺序整理调用链条，从组件出现到组件消失。

4. 提炼并简述每个函数的说明与调用时机。

5. 输出时仅提供 JSON 结果。
"""


# ==================== 数据加载函数 ====================
def load_and_index_pdf(pdf_path: str, persist_dir: str) -> Chroma:
    """加载 PDF 并创建向量索引"""
    print(f"📚 正在加载 PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"✅ 已加载 {len(docs)} 页文档")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CONFIG["chunk_size"],
        chunk_overlap=CONFIG["chunk_overlap"]
    )
    splits = text_splitter.split_documents(docs)
    print(f"✅ 已分割为 {len(splits)} 个文本块")
    
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_dir
    )
    print(f"✅ 向量索引已保存到: {persist_dir}")
    return vectorstore


# ==================== 初始化向量库 ====================
def init_vectorstore(persist_dir: str) -> Chroma:
    """初始化或加载向量数据库"""
    embedding = OpenAIEmbeddings()
    
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(
            f"❌ 向量数据库不存在: {persist_dir}\n"
            "请先取消注释数据加载代码，运行一次以创建索引。"
        )
    
    vectorstore = Chroma(
        persist_directory=persist_dir,
        embedding_function=embedding
    )
    
    # 检查是否有数据
    try:
        count = vectorstore._collection.count()
        if count == 0:
            raise ValueError("向量数据库为空，请重新索引文档")
        print(f"✅ 向量数据库已加载，包含 {count} 个文档块")
    except Exception as e:
        print(f"⚠️  无法检查向量库状态: {e}")
    
    return vectorstore


# ==================== 构建 RAG 链 ====================
def create_rag_chain(vectorstore: Chroma, model_name: str, temperature: float):
    """创建 RAG 推理链"""
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": CONFIG["retriever_k"]}
    )
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE
    )
    
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature
    )
    
    def format_docs(docs):
        # 添加来源信息
        formatted = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', '未知')
            page = doc.metadata.get('page', '?')
            formatted.append(f"[片段 {i} - 来源: {source}, 页: {page}]\n{doc.page_content}")
        return "\n\n---\n\n".join(formatted)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain


# ==================== 读取输入文件 ====================
def read_input_file(filepath: str) -> str:
    """读取输入文件"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"未找到输入文件：{filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        raise ValueError(f"输入文件为空：{filepath}")
    
    print(f"✅ 已读取输入文件: {filepath}")
    print(f"📝 内容预览:\n{content[:200]}{'...' if len(content) > 200 else ''}\n")
    return content


# ==================== 主函数 ====================
def main():
    """主执行流程"""
    print("=" * 60)
    print("🚀 ArkUI 生命周期分析 RAG 系统")
    print("=" * 60)
    
    try:
        # 1. 初始化向量库
        vectorstore = init_vectorstore(CONFIG["vector_store_path"])
        
        # 2. 读取输入
        scene_text = read_input_file(CONFIG["input_file"])
        
        # 3. 创建 RAG 链
        print("\n🔗 正在构建 RAG 推理链...")
        rag_chain = create_rag_chain(
            vectorstore,
            CONFIG["model_name"],
            CONFIG["temperature"]
        )
        
        # 4. 执行推理
        print("🤔 正在分析生命周期调用顺序...\n")
        result = rag_chain.invoke(scene_text)
        
        # 5. 输出结果
        print("=" * 60)
        print("📜 生命周期调用顺序分析结果")
        print("=" * 60)
        print(result)
        
        # 6. 保存结果（可选）
        output_file = "lifecycle_analysis_output.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n💾 结果已保存到: {output_file}")
        
    except FileNotFoundError as e:
        print(f"\n❌ 文件错误: {e}")
    except ValueError as e:
        print(f"\n❌ 数据错误: {e}")
    except Exception as e:
        print(f"\n❌ 执行失败: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


# ==================== 可选：数据索引脚本 ====================
def index_pdf_documents():
    """
    首次运行时使用此函数创建向量索引
    取消注释并调用此函数来索引你的 PDF 文档
    """
    pdf_path = "arkUI自定义组件生命周期.pdf"
    persist_dir = CONFIG["vector_store_path"]
    
    if os.path.exists(persist_dir):
        response = input(f"⚠️  向量库已存在于 {persist_dir}，是否重新索引？(y/n): ")
        if response.lower() != 'y':
            print("❌ 取消索引操作")
            return
    
    vectorstore = load_and_index_pdf(pdf_path, persist_dir)
    print("✅ 索引创建完成！")


# ==================== 入口点 ====================
if __name__ == "__main__":
    # 首次运行时取消注释以下行来创建索引：
    # index_pdf_documents()
    
    # 正常运行分析：
    main()