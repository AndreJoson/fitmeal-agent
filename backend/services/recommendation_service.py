"""
推荐引擎服务
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.models import MealPlan, DailyMeal, MealItem, Food


class RecommendationService:
    """推荐引擎"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_meal_plan(self, params: Dict) -> List[Dict]:
        """生成餐计划"""
        user_id = params.get('user_id')
        days = params.get('days', 7)
        daily_calories = params.get('daily_calories', 1800)
        high_protein = params.get('high_protein', False)
        low_carb = params.get('low_carb', False)
        
        foods = self.db.query(Food).filter(Food.is_active == True).all()
        
        filtered_foods = []
        for food in foods:
            if food.calories > daily_calories * 1.5:
                continue
            if high_protein and food.protein < 15:
                continue
            if low_carb and food.carbs > 15:
                continue
            filtered_foods.append(food)
        
        meal_plan = []
        start_date = datetime.now()
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            day_meals = {
                "date": current_date.strftime("%Y-%m-%d"),
                "breakfast": self._select_meals(filtered_foods, "breakfast", daily_calories // 3),
                "lunch": self._select_meals(filtered_foods, "lunch", daily_calories // 3),
                "dinner": self._select_meals(filtered_foods, "dinner", daily_calories // 3),
                "daily_summary": {
                    "target_calories": daily_calories,
                    "actual_calories": 0
                }
            }
            
            total_calories = sum(
                m.get("calories", 0) for m in 
                day_meals["breakfast"] + day_meals["lunch"] + day_meals["dinner"]
            )
            day_meals["daily_summary"]["actual_calories"] = total_calories
            
            meal_plan.append(day_meals)
        
        return meal_plan
    
    def _select_meals(self, foods: List[Food], meal_type: str, target_calories: float) -> List[Dict]:
        """为餐选择食物"""
        selected = []
        remaining_calories = target_calories
        
        for food in foods:
            if food.calories <= remaining_calories:
                selected.append({
                    "id": food.id,
                    "name": food.name,
                    "calories": food.calories,
                    "protein": food.protein,
                    "carbs": food.carbs,
                    "fat": food.fat,
                    "portion_size": food.portion_size
                })
                remaining_calories -= food.calories
                
                if len(selected) >= 3 or remaining_calories < 100:
                    break
        
        return selected
