"""
RAG 检索器实现
"""

from .vector_store import ChromaVectorStore
from typing import List, Dict


class RAGRetriever:
    """RAG 检索器 - 从向量库检索相关文档"""
    
    def __init__(self, persist_dir: str = "chroma_db", collection_name: str = "fitmeal_documents"):
        """初始化检索器"""
        self.vector_store = ChromaVectorStore(persist_dir, collection_name)
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """检索相关文档"""
        results = self.vector_store.search(query, top_k=top_k)
        return results
    
    def retrieve_with_context(self, query: str, top_k: int = 3) -> Dict:
        """带上下文的检索"""
        results = self.vector_store.search(query, top_k=top_k)
        
        context = {
            "query": query,
            "results": results,
            "sources": list(set([
                r["metadata"].get("source", "Unknown")
                for r in results
            ])),
            "total_results": len(results)
        }
        
        return context
    
    def add_documents(self, documents: List[Dict]):
        """添加文档到向量库"""
        self.vector_store.add_documents(documents)
    
    def get_collection_stats(self) -> dict:
        """获取向量库统计信息"""
        return self.vector_store.get_collection_info()
