import pygame
from config import block_size, screen_x, screen_y, green, blue, black

class Snake:
    def __init__(self):
        """Создает змейку из 3 сегментов в центре экрана"""
        center_x = (screen_x // 2) // block_size * block_size
        center_y = (screen_y // 2) // block_size * block_size
        
        # Тело змейки: голова и два сегмента хвоста
        self.body = [
            (center_x, center_y),
            (center_x - block_size, center_y),
            (center_x - block_size * 2, center_y)
        ]
        self.direction = "RIGHT"  # Начальное направление
        self.grow_next = False    # Флаг роста при съедении еды

    def move(self):
        """Двигает змейку в текущем направлении"""
        head_x, head_y = self.body[0]
        
        # Вычисляем новую позицию головы
        if self.direction == "UP":
            new_head = (head_x, head_y - block_size)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + block_size)
        elif self.direction == "LEFT":
            new_head = (head_x - block_size, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + block_size, head_y)
        
        # Добавляем новую голову
        self.body.insert(0, new_head)
        
        # Удаляем хвост, если не нужно расти
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False

    def change_direction(self, new_dir):
        """Меняет направление, запрещая поворот на 180°"""
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir

    def check_self_collision(self):
        """Проверяет, не врезалась ли голова в тело"""
        return self.body[0] in self.body[1:]

    def check_wall_collision(self):
        """Проверяет, не вышла ли змейка за экран"""
        x, y = self.body[0]
        return x < 0 or x >= screen_x or y < 0 or y >= screen_y

    def grow(self):
        """Помечает, что змейка должна вырасти"""
        self.grow_next = True

    def get_head_position(self):
        """Возвращает координаты головы (для проверки еды)"""
        return self.body[0]

    def get_body(self):
        """Возвращает все тело (для спавна еды)"""
        return self.body

    def draw(self, screen):
        """Рисует змейку на экране"""
        for i, (x, y) in enumerate(self.body):
            # Голова - синяя, тело - зеленое
            color = blue if i == 0 else green
            pygame.draw.rect(screen, color, (x, y, block_size, block_size))
            pygame.draw.rect(screen, black, (x, y, block_size, block_size), 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        center_x = (screen_x // 2) // block_size * block_size
        center_y = (screen_y // 2) // block_size * block_size
        
        self.body = [
            (center_x, center_y),
            (center_x - block_size, center_y),
            (center_x - block_size * 2, center_y)
        ]
        self.direction = "RIGHT"
        self.grow_next = False