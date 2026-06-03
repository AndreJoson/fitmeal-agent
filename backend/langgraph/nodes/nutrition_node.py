"""
营养计算节点
"""

async def nutrition_calculation_node(state, db):
    """营养计算节点"""
    
    if state["meal_recommendations"]:
        total_nutrition = {
            "calories": 0,
            "protein": 0,
            "carbs": 0,
            "fat": 0
        }
        
        for meal in state["meal_recommendations"]:
            if hasattr(meal, 'calories'):
                total_nutrition["calories"] += meal.calories
                total_nutrition["protein"] += meal.protein
                total_nutrition["carbs"] += meal.carbs
                total_nutrition["fat"] += meal.fat
        
        state["nutrition_analysis"] = total_nutrition
    
    return state
