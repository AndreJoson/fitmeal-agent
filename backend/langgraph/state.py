"""
LangGraph 状态定义
"""

from typing import TypedDict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MealRecommendation:
    """单个餐食推荐"""
    food_id: int
    name: str
    quantity: float
    calories: float
    protein: float
    carbs: float
    fat: float
    source_documents: List[str] = field(default_factory=list)


class ConversationState(TypedDict, total=False):
    """LangGraph 中的状态"""
    # 基础信息
    user_id: int
    user_message: str
    timestamp: datetime
    
    # 意图识别
    intent: str
    confidence: float
    
    # 用户信息
    user_info: Optional[dict]
    user_restrictions: Optional[dict]
    
    # RAG 检索结果
    retrieved_documents: List[dict]
    relevant_chunks: List[str]
    
    # 食物推荐
    candidate_foods: List[dict]
    meal_recommendations: List[MealRecommendation]
    
    # 营养分析
    nutrition_analysis: Optional[dict]
    nutrition_suggestions: List[str]
    
    # 最终响应
    final_response: str
    sources: List[str]
    
    # 错误处理
    errors: List[str]
