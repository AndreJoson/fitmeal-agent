"""
路由条件
"""

def should_use_rag(state) -> str:
    """条件：是否需要使用 RAG"""
    intent = state.get("intent", "")
    
    if intent in ["get_nutrition", "plan_week", "compare_foods"]:
        return "use_rag"
    
    return "skip_rag"


def should_calculate_nutrition(state) -> str:
    """条件：是否需要计算营养"""
    intent = state.get("intent", "")
    
    if intent in ["get_nutrition", "plan_week"]:
        return "calculate"
    
    return "skip"
