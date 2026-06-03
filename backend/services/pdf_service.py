"""
PDF 处理服务
"""

from rag.document_processor import DocumentManager
from rag.retriever import RAGRetriever
from typing import List, Dict


class PDFService:
    """PDF 处理服务"""
    
    def __init__(self):
        self.doc_manager = DocumentManager()
        self.retriever = RAGRetriever()
    
    def upload_and_index_pdf(self, file_path: str) -> Dict:
        """上传 PDF 并索引"""
        try:
            documents = self.doc_manager.upload_pdf(file_path)
            self.retriever.add_documents(documents)
            
            return {
                "status": "success",
                "document_count": len(documents),
                "message": f"成功处理了 {len(documents)} 个文档块"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def batch_index_pdfs(self) -> Dict:
        """批量索引 PDF"""
        try:
            documents = self.doc_manager.process_all_pdfs()
            self.retriever.add_documents(documents)
            
            return {
                "status": "success",
                "total_documents": len(documents)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_documents(self, query: str, top_k: int = 3) -> Dict:
        """搜索文档"""
        results = self.retriever.retrieve_with_context(query, top_k)
        return results
