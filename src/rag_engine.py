"""
RAG 引擎核心模块
"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from .config import PROMPT_TEMPLATE
from .vectorstore import VectorStoreManager
from .utils import format_docs


class RAGEngine:
    """RAG 推理引擎"""

    def __init__(
        self,
        vectorstore_manager: VectorStoreManager,
        model_name: str = "deepseek-chat",
        temperature: float = 0,
        retriever_k: int = 4
    ):
        """
        初始化 RAG 引擎

        Args:
            vectorstore_manager: 向量库管理器
            model_name: LLM 模型名称
            temperature: 生成温度
            retriever_k: 检索的文档数量
        """
        self.vectorstore_manager = vectorstore_manager
        self.model_name = model_name
        self.temperature = temperature
        self.retriever_k = retriever_k
        self.rag_chain = None

    def build_chain(self, api_key=None, api_base=None):
        """
        构建 RAG 推理链

        Args:
            api_key: API 密钥（可选）
            api_base: API 基础 URL（可选）
        """
        retriever = self.vectorstore_manager.get_retriever(k=self.retriever_k)

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=PROMPT_TEMPLATE
        )

        # 构建 LLM 参数
        llm_kwargs = {
            "model_name": self.model_name,
            "temperature": self.temperature
        }

        if api_key:
            llm_kwargs["api_key"] = api_key
        if api_base:
            llm_kwargs["base_url"] = api_base

        llm = ChatOpenAI(**llm_kwargs)

        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return self.rag_chain

    def analyze(self, query: str, api_key=None, api_base=None) -> str:
        """
        执行生命周期分析

        Args:
            query: 用户查询（ArkTS 代码场景）
            api_key: API 密钥（可选）
            api_base: API 基础 URL（可选）

        Returns:
            分析结果（JSON 格式）
        """
        if self.rag_chain is None:
            print("🔗 正在构建 RAG 推理链...")
            self.build_chain(api_key=api_key, api_base=api_base)

        print("🤔 正在分析生命周期调用顺序...\n")
        result = self.rag_chain.invoke(query)

        return result
