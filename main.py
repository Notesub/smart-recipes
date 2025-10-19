from fastapi import FastAPI
from typing import List, Optional
app = FastAPI()

# === ОПИСАНИЕ API ЭНДПОИНТОВ ===

# Получить рецепты по указанным ингредиентам
# Вход: ingredients - строка с продуктами через запятую
# Выход: {"recipes": [{"id": int, "name": str, "ingredients": List[str], "cooking_time": int}]}
# GET /recipes?ingredients=курица,рис,лук

# Получить детальную информацию о конкретном рецепте
# Вход: recipe_id - идентификатор рецепта (число)
# Выход: {"id": int, "name": str, "ingredients": List[str], "instructions": str, "cooking_time": int, "calories": int}
# GET /recipes/{recipe_id}

# Добавить продукты в виртуальный холодильник
# Вход: {"products": List[str]} - JSON с массивом продуктов
# Выход: {"message": str, "fridge": List[str]}
# POST /fridge

# Посмотреть текущие продукты в холодильнике
# Вход: нет
# Выход: {"fridge": List[str]}
# GET /fridge

# Получить рецепты из текущих продуктов в холодильнике
# Вход: нет
# Выход: {"recipes": [{"id": int, "name": str, "ingredients": List[str], "cooking_time": int}]}
# GET /fridge/recipes

# === РЕАЛЬНАЯ РЕАЛИЗАЦИЯ ===

# Временная база данных (потом заменим на настоящую БД)

recipes_db = [
    {
        "id": 1,
        "name": "Курица с рисом",
        "ingredients": ["курица", "рис", "лук", "морковь"],
        "instructions": "Обжарить курицу, добавить овощи, тушить с рисом",
        "cooking_time": 30,
        "calories": 450
    }
]

user_fridge = []

# Продукты пользователя

# Здесь будет твой реальный код эндпоинтов...
# (который мы писали ранее)

@app.get("/")
def read_root():
    return {"message": "Food Planner API"}
