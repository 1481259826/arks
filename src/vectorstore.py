"""
向量库管理模块
"""

import os
from pathlib import Path
from typing import Optional

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from .utils import safe_print


class VectorStoreManager:
    """向量库管理器"""

    def __init__(self, persist_directory: Path, embedding_function: Optional[OpenAIEmbeddings] = None):
        """
        初始化向量库管理器

        Args:
            persist_directory: 向量库持久化目录
            embedding_function: 嵌入函数，默认使用 OpenAIEmbeddings
        """
        self.persist_directory = Path(persist_directory)
        self.embedding_function = embedding_function or OpenAIEmbeddings()
        self.vectorstore: Optional[Chroma] = None

    def load_and_index_pdf(
        self,
        pdf_path: Path,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        force_reindex: bool = False
    ) -> Chroma:
        """
        加载 PDF 并创建向量索引

        Args:
            pdf_path: PDF 文件路径
            chunk_size: 文档分块大小
            chunk_overlap: 分块重叠长度
            force_reindex: 是否强制重新索引

        Returns:
            Chroma 向量库实例
        """
        # 检查是否需要重新索引
        if self.persist_directory.exists() and not force_reindex:
            safe_print(f"⚠️  向量库已存在于 {self.persist_directory}")
            response = input("是否重新索引？(y/n): ")
            if response.lower() != 'y':
                safe_print("❌ 取消索引操作")
                return self.load_vectorstore()

        safe_print(f"📚 正在加载 PDF: {pdf_path}")
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        safe_print(f"✅ 已加载 {len(docs)} 页文档")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        splits = text_splitter.split_documents(docs)
        safe_print(f"✅ 已分割为 {len(splits)} 个文本块")

        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=self.embedding_function,
            persist_directory=str(self.persist_directory)
        )
        safe_print(f"✅ 向量索引已保存到: {self.persist_directory}")

        return self.vectorstore

    def load_vectorstore(self) -> Chroma:
        """
        加载现有向量库

        Returns:
            Chroma 向量库实例

        Raises:
            FileNotFoundError: 向量库不存在
            ValueError: 向量库为空
        """
        if not self.persist_directory.exists():
            raise FileNotFoundError(
                f"❌ 向量数据库不存在: {self.persist_directory}\n"
                "请先运行索引命令创建向量库。"
            )

        self.vectorstore = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=self.embedding_function
        )

        # 检查是否有数据
        try:
            count = self.vectorstore._collection.count()
            if count == 0:
                raise ValueError("向量数据库为空，请重新索引文档")
            safe_print(f"✅ 向量数据库已加载，包含 {count} 个文档块")
        except Exception as e:
            safe_print(f"⚠️  无法检查向量库状态: {e}")

        return self.vectorstore

    def get_retriever(self, k: int = 4):
        """
        获取检索器

        Args:
            k: 返回的文档数量

        Returns:
            检索器实例
        """
        if self.vectorstore is None:
            self.load_vectorstore()

        return self.vectorstore.as_retriever(search_kwargs={"k": k})
