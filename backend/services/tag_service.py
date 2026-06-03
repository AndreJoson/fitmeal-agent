"""
标签服务 - 标签管理
"""

from sqlalchemy.orm import Session
from database.models import Tag, User, Food
from typing import List, Dict, Optional


class TagService:
    """标签服务"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_tags(self, category: Optional[str] = None) -> List[Dict]:
        """获取所有标签"""
        query = self.db.query(Tag).filter(Tag.is_active == True)
        
        if category:
            query = query.filter(Tag.category == category)
        
        tags = query.all()
        
        return [
            {
                'id': t.id,
                'name': t.name,
                'category': t.category,
                'description': t.description,
                'color': t.color
            }
            for t in tags
        ]
    
    def get_user_restrictions(self, user_id: int) -> dict:
        """获取用户的禁忌标签"""
        user = self.db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return {"error": "用户不存在"}
        
        restrictions = {
            'allergens': [],
            'dislikes': []
        }
        
        for tag in user.restrictions:
            if tag.category == 'allergen':
                restrictions['allergens'].append(tag.name)
            else:
                restrictions['dislikes'].append(tag.name)
        
        return restrictions
