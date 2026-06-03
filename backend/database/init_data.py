"""
食物和标签数据初始化脚本
"""

import json
from pathlib import Path

# 定义标签数据
TAGS_DATA = {
    "tags": [
        {"id": 1, "name": "早餐", "category": "meal_type", "description": "早餐食物", "color": "#FFD700"},
        {"id": 2, "name": "午餐", "category": "meal_type", "description": "午餐食物", "color": "#FF6347"},
        {"id": 3, "name": "晚餐", "category": "meal_type", "description": "晚餐食物", "color": "#4169E1"},
        {"id": 10, "name": "鸡肉", "category": "food_group", "description": "家禽类", "color": "#CD853F"},
        {"id": 20, "name": "高蛋白", "category": "nutrition_type", "description": "蛋白质含量高", "color": "#FF1493"},
    ]
}

# 定义食物数据
FOODS_DATA = {
    "foods": [
        {
            "name": "鸡胸肉",
            "description": "去皮鸡胸肉，高蛋白低脂肪",
            "calories": 165,
            "protein": 31,
            "carbs": 0,
            "fat": 3.6,
            "fiber": 0,
            "sodium": 75,
            "portion_size": "100g",
            "tags": ["午餐", "晚餐", "鸡肉", "高蛋白"]
        },
        {
            "name": "鸡蛋",
            "description": "水煮鸡蛋，营养丰富",
            "calories": 155,
            "protein": 13,
            "carbs": 1.1,
            "fat": 11,
            "fiber": 0,
            "sodium": 124,
            "portion_size": "100g",
            "tags": ["早餐", "高蛋白"]
        },
    ]
}

def init_tags(db_session):
    """初始化标签"""
    from database.models import Tag
    
    for tag_data in TAGS_DATA["tags"]:
        existing = db_session.query(Tag).filter(Tag.name == tag_data["name"]).first()
        if not existing:
            tag = Tag(
                name=tag_data["name"],
                category=tag_data["category"],
                description=tag_data["description"],
                color=tag_data["color"]
            )
            db_session.add(tag)
    
    db_session.commit()
    print(f"✅ 已初始化 {len(TAGS_DATA['tags'])} 个标签")

def init_foods(db_session):
    """初始化食物"""
    from database.models import Food, Tag
    
    for food_data in FOODS_DATA["foods"]:
        existing = db_session.query(Food).filter(Food.name == food_data["name"]).first()
        if not existing:
            food = Food(
                name=food_data["name"],
                description=food_data["description"],
                calories=food_data["calories"],
                protein=food_data["protein"],
                carbs=food_data["carbs"],
                fat=food_data["fat"],
                fiber=food_data["fiber"],
                sodium=food_data["sodium"],
                portion_size=food_data["portion_size"]
            )
            
            for tag_name in food_data["tags"]:
                tag = db_session.query(Tag).filter(Tag.name == tag_name).first()
                if tag:
                    food.tags.append(tag)
            
            db_session.add(food)
    
    db_session.commit()
    print(f"✅ 已初始化 {len(FOODS_DATA['foods'])} 种食物")

def main():
    """主函数"""
    from database.connection import SessionLocal, init_db
    
    db = SessionLocal()
    
    try:
        print("🔄 开始初始化数据...")
        init_db()
        init_tags(db)
        init_foods(db)
        print("✅ 数据初始化完成！")
    except Exception as e:
        print(f"❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
