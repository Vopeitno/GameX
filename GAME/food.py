import pygame
import random
from config import screen_x, screen_y, block_size, red, score

# Внутренние переменные модуля (не трогать извне)
_food_pos = (0, 0)
_food_spawned = False

def spawn_food(snake_body):
    """
    Создает еду в случайном месте, не занятом змейкой
    snake_body: список координат змейки [(x1,y1), (x2,y2), ...]
    Возвращает позицию созданной еды (x, y)
    
    """
    global _food_pos, _food_spawned
    
    while True:
        grid_x = random.randint(0, (screen_x - block_size) // block_size)
        grid_y = random.randint(0, (screen_y - block_size) // block_size)
        x = grid_x * block_size
        y = grid_y * block_size
        
        if (x, y) not in snake_body:
            _food_pos = (x, y)
            _food_spawned = True
            return _food_pos

def draw_food(screen):
    """Рисует еду на экране"""
    if _food_spawned:
        pygame.draw.rect(screen, red, (*_food_pos, block_size, block_size))

def check_food_eaten(snake_head):
    """
    Проверяет, съела ли змейка еду
    snake_head: координаты головы змейки (x, y)
    Возвращает True если еда съедена
    """
    global _food_spawned
    if _food_spawned and snake_head == _food_pos:
        _food_spawned = False
        return True
    return False

def increase_score(points=1):
    """Увеличивает счет на указанное количество очков"""
    global score
    score += points
    return score

def get_score():
    """Возвращает текущий счет"""
    return score

def get_food_position():
    """Возвращает текущую позицию еды или None если еды нет"""
    return _food_pos if _food_spawned else None

def is_food_spawned():
    """Проверяет, существует ли еда на поле"""
    return _food_spawned