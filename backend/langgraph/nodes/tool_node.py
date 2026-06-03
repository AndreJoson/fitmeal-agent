"""
工具执行节点
"""

async def tool_execution_node(state, db):
    """工具执行节点"""
    intent = state.get("intent", "query_meal")
    
    if intent == "query_meal":
        # 处理食物查询
        state["candidate_foods"] = [
            {
                "id": 1,
                "name": "鸡胸肉",
                "calories": 165,
                "protein": 31,
                "carbs": 0,
                "fat": 3.6
            }
        ]
    
    elif intent == "plan_week":
        # 生成周计划
        state["meal_recommendations"] = []
    
    return state
