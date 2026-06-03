"""
Chroma 向量存储实现
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict


class ChromaVectorStore:
    """Chroma 向量存储"""
    
    def __init__(self, persist_dir: str = "chroma_db", collection_name: str = "fitmeal_documents"):
        """初始化 Chroma 向量存储"""
        self.settings = Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
        
        self.client = chromadb.Client(self.settings)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: List[Dict]):
        """添加文档到向量库"""
        ids = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            ids.append(f"doc_{i}_{hash(doc['content']) % 10000}")
            texts.append(doc["content"])
            metadatas.append(doc.get("metadata", {}))
        
        self.collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """搜索相似文档"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        documents = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                documents.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else 0
                })
        
        return documents
    
    def delete_collection(self):
        """删除集合"""
        self.client.delete_collection(name="fitmeal_documents")
    
    def persist(self):
        """持久化数据"""
        self.client.persist()
    
    def get_collection_info(self) -> dict:
        """获取集合信息"""
        return {
            "name": self.collection.name,
            "count": self.collection.count(),
            "metadata": self.collection.metadata
        }
