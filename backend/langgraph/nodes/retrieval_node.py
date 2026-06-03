"""
检索节点
"""

from rag.retriever import RAGRetriever
from database.models import User
from sqlalchemy.orm import Session

async def retrieval_node(state, db: Session):
    """检索节点 - RAG + 数据库查询"""
    
    retriever = RAGRetriever()
    user_message = state["user_message"]
    
    # RAG 检索
    try:
        rag_results = retriever.retrieve(user_message, top_k=3)
        state["retrieved_documents"] = rag_results
        state["relevant_chunks"] = [doc.get("content") for doc in rag_results]
    except:
        state["retrieved_documents"] = []
        state["relevant_chunks"] = []
    
    # 获取用户信息
    user_id = state.get("user_id")
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            state["user_info"] = {
                "age": user.age,
                "weight": user.current_weight,
                "height": user.height,
                "daily_calories": user.daily_calories
            }
    
    return state
