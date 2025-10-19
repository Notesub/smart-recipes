import uvicorn
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

# Эндпоинт 1: Получить все рецепты
@app.get('/recipes')
def get_all_recipes():
    # Функция GET - только получает данные, ничего не изменяет
    
    # Считаем сколько всего рецептов
    total_recipes = len(recipes_db)
    
    # Проверяем пустая ли база рецептов
    is_empty = total_recipes == 0
    
    return {
        "total_recipes": total_recipes,  # Показываем количество
        "is_empty": is_empty,            # Показываем пусто или нет
        "recipes": recipes_db            # Отдаем все рецепты
    }

# Эндпоинт 2: Найти рецепты по ингредиентам
@app.get('/recipes/search')
def search_recipes_by_ingredients(ingredients: str):
    # ingredients - это строка типа "курица,рис,лук" из URL
    
    # Проверяем что пользователь указал ингредиенты
    if ingredients == "" or ingredients is None:
        raise HTTPException(
            status_code=400, 
            detail="Укажите ингредиенты через запятую"
        )
    
    # Разделяем строку на отдельные ингредиенты
    ingredients_parts = ingredients.split(",")
    
    # Очищаем каждый ингредиент (убираем пробелы, делаем маленькими буквами)
    clean_ingredients = []
    for ingredient in ingredients_parts:
        clean_ingredient = ingredient.strip().lower()
        clean_ingredients.append(clean_ingredient)
    
    # Ищем подходящие рецепты
    found_recipes = []
    
    # Перебираем ВСЕ рецепты в базе
    for recipe in recipes_db:
        # Для каждого рецепта проверяем есть ли в нем нужные ингредиенты
        has_all_ingredients = True
        
        # Проверяем каждый искомый ингредиент
        for search_ingredient in clean_ingredients:
            if search_ingredient not in recipe["ingredients"]:
                has_all_ingredients = False
                break  # Прерываем проверку если не нашли ингредиент
        
        # Если рецепт подходит - добавляем в результат
        if has_all_ingredients:
            found_recipes.append(recipe)
    
    # Проверяем нашли ли хоть один рецепт
    if len(found_recipes) == 0:
        raise HTTPException(
            status_code=404,
            detail="Не найдено рецептов с указанными ингредиентами"
        )
    
    return {"found_recipes": found_recipes}

# Эндпоинт 3: Добавить новый рецепт
@app.post('/recipes')
def add_recipe(recipe: Recipe):
    # POST - создает новые данные
    
    # Преобразуем рецепт в обычный словарь Python
    new_recipe = recipe.dict()
    
    # Добавляем ID рецепту (просто номер по порядку)
    new_recipe_id = len(recipes_db) + 1
    new_recipe["id"] = new_recipe_id
    
    # Добавляем рецепт в нашу базу
    recipes_db.append(new_recipe)
    
    return {"message": f"Рецепт '{recipe.name}' успешно добавлен"}

# Эндпоинт 4: Посмотреть что в холодильнике
@app.get('/fridge')
def get_fridge_contents():
    total_products = len(user_fridge)
    is_empty = total_products == 0
    
    return {
        "total_products": total_products,
        "is_empty": is_empty,
        "products": user_fridge
    }

# Эндпоинт 5: Добавить продукт в холодильник
@app.post('/fridge')
def add_to_fridge(item: FridgeItem):
    # Добавляем продукт в список (в нижнем регистре)
    product_name = item.product.lower()
    user_fridge.append(product_name)
    
    return {"message": f"Продукт '{item.product}' добавлен в холодильник"}

# Эндпоинт 6: Очистить холодильник
@app.delete('/fridge/clear')
def clear_fridge():
    # Очищаем список продуктов
    user_fridge.clear()
    
    return {"message": "Холодильник очищен"}

# Эндпоинт 7: Получить рецепты из продуктов в холодильнике
@app.get('/fridge/recipes')
def get_recipes_from_fridge():
    # Проверяем есть ли продукты в холодильнике
    if len(user_fridge) == 0:
        raise HTTPException(
            status_code=404, 
            detail="В холодильнике нет продуктов"
        )
    
    # Ищем рецепты которые можно приготовить
    available_recipes = []
    
    # Перебираем все рецепты
    for recipe in recipes_db:
        # Проверяем можно ли приготовить этот рецепт
        can_cook = True
        
        # Проверяем каждый ингредиент рецепта
        for ingredient in recipe["ingredients"]:
            if ingredient not in user_fridge:
                can_cook = False
                break  # Если нет какого-то ингредиента - рецепт не готовим
        
        # Если все ингредиенты есть - добавляем рецепт
        if can_cook:
            available_recipes.append(recipe)
    
    # Проверяем нашли ли рецепты
    if len(available_recipes) == 0:
        raise HTTPException(
            status_code=404,
            detail="Нет рецептов для продуктов в холодильнике"
        )
    
    return {"available_recipes": available_recipes}

# Запускаем сервер когда файл запускают напрямую
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
