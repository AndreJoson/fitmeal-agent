"""
营养计算服务
"""

from typing import List, Dict, Optional


class NutritionService:
    """营养计算服务"""
    
    @staticmethod
    def calculate_nutrition(meals: List[Dict]) -> Dict:
        """计算食物的营养成分总和"""
        total = {
            "calories": 0.0,
            "protein": 0.0,
            "carbs": 0.0,
            "fat": 0.0,
            "fiber": 0.0,
            "sodium": 0.0
        }
        
        for meal in meals:
            total["calories"] += meal.get("calories", 0)
            total["protein"] += meal.get("protein", 0)
            total["carbs"] += meal.get("carbs", 0)
            total["fat"] += meal.get("fat", 0)
            total["fiber"] += meal.get("fiber", 0)
            total["sodium"] += meal.get("sodium", 0)
        
        # 计算宏量营养比例
        total_macros = total["protein"] + total["carbs"] + total["fat"]
        if total_macros > 0:
            total["protein_ratio"] = round((total["protein"] * 4) / total["calories"] * 100, 1) if total["calories"] > 0 else 0
            total["carbs_ratio"] = round((total["carbs"] * 4) / total["calories"] * 100, 1) if total["calories"] > 0 else 0
            total["fat_ratio"] = round((total["fat"] * 9) / total["calories"] * 100, 1) if total["calories"] > 0 else 0
        
        return total
    
    @staticmethod
    def check_nutrition_balance(nutrition: Dict) -> Dict:
        """检查营养是否均衡"""
        suggestions = []
        is_balanced = True
        
        protein_ratio = nutrition.get("protein_ratio", 0)
        carbs_ratio = nutrition.get("carbs_ratio", 0)
        fat_ratio = nutrition.get("fat_ratio", 0)
        
        if protein_ratio < 20:
            suggestions.append("蛋白质摄入不足")
            is_balanced = False
        elif protein_ratio > 30:
            suggestions.append("蛋白质摄入过多")
            is_balanced = False
        
        if carbs_ratio < 45:
            suggestions.append("碳水化合物摄入不足")
            is_balanced = False
        elif carbs_ratio > 65:
            suggestions.append("碳水化合物摄入过多")
            is_balanced = False
        
        if fat_ratio < 20:
            suggestions.append("脂肪摄入不足")
            is_balanced = False
        elif fat_ratio > 35:
            suggestions.append("脂肪摄入过多")
            is_balanced = False
        
        if is_balanced:
            suggestions.append("营养比例均衡")
        
        return {
            "is_balanced": is_balanced,
            "suggestions": suggestions
        }
    
    @staticmethod
    def calculate_bmi(weight: float, height: float) -> Dict:
        """计算 BMI"""
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        if bmi < 18.5:
            status = "体重过低"
        elif 18.5 <= bmi < 25:
            status = "正常体重"
        elif 25 <= bmi < 30:
            status = "超重"
        else:
            status = "肥胖"
        
        return {
            "bmi": round(bmi, 1),
            "status": status,
            "healthy_range": "18.5 - 24.9"
        }
