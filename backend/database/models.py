"""
数据库模型 - SQLAlchemy ORM 定义
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# ========== 关联表 ==========

# 食物-标签关联表
food_tag_association = Table(
    'food_tag',
    Base.metadata,
    Column('food_id', Integer, ForeignKey('food.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)

# 用户-禁忌标签关联表
user_restriction_association = Table(
    'user_restriction',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)


# ========== 模型定义 ==========

class Food(Base):
    """食物表"""
    __tablename__ = 'food'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(String(500))
    calories = Column(Float)  # kcal per 100g
    protein = Column(Float)   # g
    carbs = Column(Float)     # g
    fat = Column(Float)       # g
    fiber = Column(Float)     # g
    sodium = Column(Float)    # mg
    portion_size = Column(String(50), default="100g")
    image_url = Column(String(300), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    tags = relationship("Tag", secondary=food_tag_association, back_populates="foods")
    meal_items = relationship("MealItem", back_populates="food", cascade="all, delete-orphan")


class Tag(Base):
    """标签表"""
    __tablename__ = 'tag'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    category = Column(String(50), index=True)  # meal_type, food_group, allergen, nutrition_type 等
    description = Column(String(200))
    color = Column(String(7), default="#000000")  # 前端显示颜色
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    foods = relationship("Food", secondary=food_tag_association, back_populates="tags")
    users = relationship("User", secondary=user_restriction_association)


class User(Base):
    """用户表"""
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)  # M/F
    current_weight = Column(Float, nullable=True)  # kg
    target_weight = Column(Float, nullable=True)   # kg
    height = Column(Float, nullable=True)  # cm
    daily_calories = Column(Float, nullable=True)
    activity_level = Column(String(20), nullable=True)  # sedentary/light/moderate/active
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    restrictions = relationship("Tag", secondary=user_restriction_association)
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
    conversation_history = relationship("ConversationHistory", back_populates="user", cascade="all, delete-orphan")


class MealPlan(Base):
    """餐计划表"""
    __tablename__ = 'meal_plan'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    name = Column(String(100))
    description = Column(String(500), nullable=True)
    duration_days = Column(Integer)
    start_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="meal_plans")
    daily_meals = relationship("DailyMeal", back_populates="meal_plan", cascade="all, delete-orphan")


class DailyMeal(Base):
    """每日餐表"""
    __tablename__ = 'daily_meal'
    
    id = Column(Integer, primary_key=True, index=True)
    meal_plan_id = Column(Integer, ForeignKey('meal_plan.id'), index=True)
    meal_date = Column(DateTime)
    meal_type = Column(String(20), index=True)  # breakfast/lunch/dinner/snack
    
    # 关系
    meal_plan = relationship("MealPlan", back_populates="daily_meals")
    meal_items = relationship("MealItem", back_populates="daily_meal", cascade="all, delete-orphan")


class MealItem(Base):
    """餐项目表"""
    __tablename__ = 'meal_item'
    
    id = Column(Integer, primary_key=True, index=True)
    daily_meal_id = Column(Integer, ForeignKey('daily_meal.id'), index=True)
    food_id = Column(Integer, ForeignKey('food.id'), index=True)
    quantity = Column(Float)  # 数量（克）
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    daily_meal = relationship("DailyMeal", back_populates="meal_items")
    food = relationship("Food", back_populates="meal_items")


class ConversationHistory(Base):
    """对话记录表"""
    __tablename__ = 'conversation_history'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    user_message = Column(String(1000))
    agent_response = Column(String(2000))
    intent = Column(String(50), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # 关系
    user = relationship("User", back_populates="conversation_history")


class DocumentMetadata(Base):
    """文档元数据表 (RAG)"""
    __tablename__ = 'document_metadata'
    
    id = Column(Integer, primary_key=True, index=True)
    source_file = Column(String(255), index=True)  # PDF 文件名
    chunk_id = Column(Integer)
    total_chunks = Column(Integer)
    content_length = Column(Integer)
    embedding_model = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
