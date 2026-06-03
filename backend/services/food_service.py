"""
食物服务 - 食物查询和管理
"""

from sqlalchemy.orm import Session
from database.models import Food, Tag
from typing import List, Dict, Optional


class FoodService:
    """食物服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_foods(self) -> List[Food]:
        """获取所有食物"""
        return self.db.query(Food).filter(Food.is_active == True).all()
    
    def get_food_by_id(self, food_id: int) -> Optional[Food]:
        """根据 ID 获取食物"""
        return self.db.query(Food).filter(Food.id == food_id).first()
    
    def get_food_by_name(self, name: str) -> Optional[Food]:
        """根据名称获取食物"""
        return self.db.query(Food).filter(Food.name == name).first()
    
    def search_by_tags(self, query: dict) -> List[Dict]:
        """根据标签搜索食物"""
        tags = query.get('tags', [])
        max_calories = query.get('max_calories', 999)
        min_protein = query.get('min_protein', 0)
        
        tag_objects = self.db.query(Tag).filter(Tag.name.in_(tags)).all()
        tag_ids = [t.id for t in tag_objects]
        
        foods = self.db.query(Food).filter(
            Food.calories <= max_calories,
            Food.protein >= min_protein,
            Food.is_active == True
        ).all()
        
        result = []
        for food in foods:
            food_tag_ids = [t.id for t in food.tags]
            if any(tag_id in food_tag_ids for tag_id in tag_ids):
                result.append({
                    'id': food.id,
                    'name': food.name,
                    'description': food.description,
                    'calories': food.calories,
                    'protein': food.protein,
                    'carbs': food.carbs,
                    'fat': food.fat,
                    'fiber': food.fiber,
                    'portion_size': food.portion_size,
                    'tags': [t.name for t in food.tags]
                })
        
        return result
    
    def get_high_protein_foods(self, min_protein: float = 20) -> List[Dict]:
        """获取高蛋白食物"""
        foods = self.db.query(Food).filter(
            Food.protein >= min_protein,
            Food.is_active == True
        ).all()
        
        return [
            {
                'id': f.id,
                'name': f.name,
                'calories': f.calories,
                'protein': f.protein,
                'carbs': f.carbs,
                'fat': f.fat
            }
            for f in foods
        ]
    
    def get_low_carb_foods(self, max_carbs: float = 10) -> List[Dict]:
        """获取低碳水食物"""
        foods = self.db.query(Food).filter(
            Food.carbs <= max_carbs,
            Food.is_active == True
        ).all()
        
        return [
            {
                'id': f.id,
                'name': f.name,
                'calories': f.calories,
                'protein': f.protein,
                'carbs': f.carbs,
                'fat': f.fat
            }
            for f in foods
        ]
