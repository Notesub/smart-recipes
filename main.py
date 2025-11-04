import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Создаем веб-приложение
app = FastAPI()

# Это наши "базы данных" - просто списки в памяти
recipes_db = []    # Здесь будут храниться все рецепты
user_fridge = []   # Здесь будут храниться продукты пользователя

# Описываем как выглядит рецепт
class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str
    cooking_time: int
    calories: int

# Описываем как выглядит продукт
class FridgeItem(BaseModel):
    product: str

# ============ ЭНДПОИНТЫ ============

# КОРНЕВОЙ ЭНДПОИНТ - самый главный
@app.get("/")
async def root():
    return {"message": "Food Planner API - Добро пожаловать!"}

# Эндпоинт 1: Получить все рецепты
@app.get('/recipes')
async def get_all_recipes():
    # Считаем сколько всего рецептов
    total_recipes = len(recipes_db)
    
    # Проверяем пустая ли база рецептов
    is_empty = total_recipes == 0
    
    return {
        "total_recipes": total_recipes,
        "is_empty": is_empty,
        "recipes": recipes_db
    }

# Эндпоинт 2: Найти рецепты по ингредиентам
@app.get('/recipes/search')
async def search_recipes_by_ingredients(ingredients: str):
    if ingredients == "" or ingredients is None:
        raise HTTPException(
            status_code=400, 
            detail="Укажите ингредиенты через запятую"
        )
    
    # Разделяем строку на отдельные ингредиенты
    ingredients_parts = ingredients.split(",")
    
    # Очищаем каждый ингредиент
    clean_ingredients = []
    for ingredient in ingredients_parts:
        clean_ingredient = ingredient.strip().lower()
        clean_ingredients.append(clean_ingredient)
    
    # Ищем подходящие рецепты
    found_recipes = []
    
    for recipe in recipes_db:
        has_all_ingredients = True
        
        for search_ingredient in clean_ingredients:
            if search_ingredient not in recipe["ingredients"]:
                has_all_ingredients = False
                break
        
        if has_all_ingredients:
            found_recipes.append(recipe)
    
    if len(found_recipes) == 0:
        raise HTTPException(
            status_code=404,
            detail="Не найдено рецептов с указанными ингредиентами"
        )
    
    return {"found_recipes": found_recipes}

# Эндпоинт 3: Добавить новый рецепт
@app.post('/recipes')
async def add_recipe(recipe: Recipe):
    new_recipe = recipe.dict()
    new_recipe_id = len(recipes_db) + 1
    new_recipe["id"] = new_recipe_id
    recipes_db.append(new_recipe)
    
    return {"message": f"Рецепт '{recipe.name}' успешно добавлен"}

# Эндпоинт 4: Посмотреть что в холодильнике
@app.get('/fridge')
async def get_fridge_contents():
    total_products = len(user_fridge)
    is_empty = total_products == 0
    
    return {
        "total_products": total_products,
        "is_empty": is_empty,
        "products": user_fridge
    }

# Эндпоинт 5: Добавить продукт в холодильник
@app.post('/fridge')
async def add_to_fridge(item: FridgeItem):
    product_name = item.product.lower()
    user_fridge.append(product_name)
    
    return {"message": f"Продукт '{item.product}' добавлен в холодильник"}

# Эндпоинт 6: Очистить холодильник
@app.delete('/fridge/clear')
async def clear_fridge():
    user_fridge.clear()
    return {"message": "Холодильник очищен"}

# Эндпоинт 7: Получить рецепты из продуктов в холодильнике
@app.get('/fridge/recipes')
async def get_recipes_from_fridge():
    if len(user_fridge) == 0:
        raise HTTPException(
            status_code=404, 
            detail="В холодильнике нет продуктов"
        )
    
    available_recipes = []
    
    for recipe in recipes_db:
        can_cook = True
        
        for ingredient in recipe["ingredients"]:
            if ingredient not in user_fridge:
                can_cook = False
                break
        
        if can_cook:
            available_recipes.append(recipe)
    
    if len(available_recipes) == 0:
        raise HTTPException(
            status_code=404,
            detail="Нет рецептов для продуктов в холодильнике"
        )
    
    return {"available_recipes": available_recipes}

# Запускаем сервер
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
