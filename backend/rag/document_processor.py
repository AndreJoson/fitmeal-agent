"""
PDF 文档处理和切分模块
"""

from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import os


class PDFProcessor:
    """PDF 处理器 - 读取、切分文本"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> tuple:
        """读取 PDF 文件"""
        pdf_reader = PdfReader(file_path)
        text = ""
        metadata = {
            "source": os.path.basename(file_path),
            "pages": len(pdf_reader.pages),
            "file_path": file_path
        }
        
        for page_num, page in enumerate(pdf_reader.pages):
            text += f"\n--- 第 {page_num + 1} 页 ---\n"
            text += page.extract_text()
        
        return text, metadata
    
    def split_text(self, text: str, metadata: dict) -> List[Dict]:
        """切分文本"""
        chunks = self.text_splitter.split_text(text)
        
        documents = []
        for i, chunk in enumerate(chunks):
            documents.append({
                "content": chunk,
                "metadata": {
                    **metadata,
                    "chunk_id": i,
                    "chunk_size": len(chunk),
                    "total_chunks": len(chunks)
                }
            })
        
        return documents
    
    def process_pdf(self, file_path: str) -> List[Dict]:
        """处理 PDF 的完整流程"""
        text, metadata = self.load_pdf(file_path)
        documents = self.split_text(text, metadata)
        return documents


class DocumentManager:
    """文档管理器 - 管理 PDF 上传和处理"""
    
    def __init__(self, data_dir: str = "data/documents"):
        self.data_dir = data_dir
        self.processor = PDFProcessor()
        os.makedirs(data_dir, exist_ok=True)
    
    def upload_pdf(self, file_path: str) -> List[Dict]:
        """上传和处理 PDF"""
        filename = os.path.basename(file_path)
        dest_path = os.path.join(self.data_dir, filename)
        
        import shutil
        shutil.copy(file_path, dest_path)
        
        documents = self.processor.process_pdf(dest_path)
        return documents
    
    def process_all_pdfs(self) -> List[Dict]:
        """处理目录中的所有 PDF"""
        all_documents = []
        
        for file in os.listdir(self.data_dir):
            if file.endswith('.pdf'):
                file_path = os.path.join(self.data_dir, file)
                documents = self.processor.process_pdf(file_path)
                all_documents.extend(documents)
        
        return all_documents
    
    def get_uploaded_files(self) -> List[str]:
        """获取已上传的 PDF 文件列表"""
        files = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.pdf'):
                files.append(file)
        return files
