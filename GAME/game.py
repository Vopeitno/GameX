import pygame  # импорт библиотеки для игр
import sys  #  импорт для выхода из программы
import os   # для проверки путей к файлам
import random  # для случайных значений в частицах
import math    # для математики в анимациях
from config import *
from snake import Snake # импортируем все из кода Арсена
from food import spawn_food, draw_food, check_food_eaten, increase_score, get_score
from sfx import load_bg_music, stop_bg_music, play_eat_sound, play_dead_sound, play_button_sound, play_pause_sound  # Импорт SFX
from fonts import get_font  # Импорт шрифтов

# Класс для частиц эффекта 
class Particle:
    """Частицы эффекта при съедении еды"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-10, 10)  # скорость по X -10 и 10
        self.vy = random.uniform(-10, 10)  # скорость по Y тут так же как и по X
        self.lifetime = 15  # живет 15 кадров
        self.color = (255, 50, 50)  # красный цвет (простой кортеж)
        self.size = random.randint(3, 6)  # случайный размер
    
    def update(self):
        """Обновляет позицию частицы"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # гравитация (падает вниз)
        self.lifetime -= 1
        return self.lifetime > 0  # True если частица жива
    
    def draw(self, screen):
        """Рисует частицу с прозрачностью"""
        alpha = min(255, self.lifetime * 10)  # прозрачность
        surf = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(surf, (self.x - self.size, self.y - self.size))

class GameEngine:   # создание чертежа для игры 
    """управление всего что происходит на экране""" 
    
    def __init__(self):
        pygame.init()  # Запускаем pygame
        
        self.screen = pygame.display.set_mode((screen_x, screen_y)) # Создаем окно игры 720 на 480
        pygame.display.set_caption("Змейка")
        
        self.clock = pygame.time.Clock()    # Часы для контроля скорости игры

        self.state = 0  # Текущее состояние игры 0 это экран меню 
        
        # Переменные для новых эффектов, для анимации еды
        self.food_colors = [(255, 50, 50), (255, 100, 100), (255, 200, 200), (255, 255, 255)]
        self.food_color_index = 0
        self.food_pulse = 0
        
        # Для частиц эффекта
        self.particles = []  # список частиц
        
        # Для подсветки границ
        self.glow_surface = None  # поверхность для свечения
        
        # Создаем игровые объекты
        self.snake = Snake()  # Наша змейка
        self.food = spawn_food(self.snake.get_body())  # Первая еда
        
        # Шрифты для текста (кастомные Oswald из fonts.py)
        self.font_big = get_font(48)   # Большой для заголовков
        self.font_normal = get_font(36) # Обычный для текста
        
        # Загружаем фоновую музыку BG_Music.mp3 (если файл существует)
        if os.path.exists("SFX/BG_Music.mp3"):
            load_bg_music("BG_Music.mp3")

    def handle_events(self):    # благодаря этому методу мы следим за событиями(нажатие клавишь)
        """Обрабатываем все события: нажатия клавиш, закрытие окна"""
        for event in pygame.event.get():
            
            # Если нажали крестик - закрываем игру
            if event.type == pygame.QUIT:
                stop_bg_music()  # Останавливаем музыку при выходе
                pygame.quit()
                sys.exit()
            
            # Если нажали какую-то клавишу
            if event.type == pygame.KEYDOWN:
                
                # СТАРТОВЫЙ ЭКРАН - 0
                if self.state == 0:
                    if event.key == pygame.K_SPACE:
                        play_button_sound()
                        self.state = 1  # Начинаем игру
                    elif event.key == pygame.K_ESCAPE:
                        play_button_sound()
                        stop_bg_music()
                        pygame.quit()
                        sys.exit()  # Выходим из игры
                
                # ИГРАЕМ - 1
                elif self.state == 1:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction("DOWN")
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction("RIGHT")
                    elif event.key == pygame.K_ESCAPE:
                        play_pause_sound()
                        self.state = 2  # Ставим на паузу
                
                # ПАУЗА - 2
                elif self.state == 2:
                    if event.key == pygame.K_ESCAPE:
                        play_pause_sound()
                        self.state = 1  # Продолжаем игру
                    elif event.key == pygame.K_r:
                        play_button_sound()
                        self.reset_game()  # Начинаем заново
                
                # ПРОИГРАЛИ - 3
                elif self.state == 3:
                    if event.key == pygame.K_r:
                        play_button_sound()
                        self.reset_game()  # Перезапуск
                    elif event.key == pygame.K_ESCAPE:
                        play_pause_sound()
                        self.state = 0  # Выход в меню

    # Метод для эффектов частиц
    def create_particles(self, x, y):
        """Создает 15 частиц на позиции (x, y)"""
        for _ in range(15):
            self.particles.append(Particle(x + block_size//2, y + block_size//2))
    
    def update_particles(self):
        """Обновляет все частицы"""
        self.particles = [p for p in self.particles if p.update()]
    
    def draw_particles(self):
        """Рисует все частицы"""
        for particle in self.particles:
            particle.draw(self.screen)
    
    # Метод для анимации еды
    def draw_animated_food(self):
        """Рисует анимированную еду (пульсация + смена цвета)"""
        if hasattr(self, 'food') and self.food:
            x, y = self.food
            
            # Смена цвета каждые 0.5 секунды (500 миллисекунд)
            self.food_color_index = (pygame.time.get_ticks() // 500) % len(self.food_colors)
            current_color = self.food_colors[self.food_color_index]
            
            # Пульсация размера
            self.food_pulse = (self.food_pulse + 0.25) % (2 * math.pi)
            pulse = math.sin(self.food_pulse) * 4 + 2  # от -2 до +6 пикселей
            
            # Рисуем большую пульсирующую еду
            pygame.draw.rect(self.screen, current_color,
                           (x + pulse//2, y + pulse//2,
                            block_size - pulse, block_size - pulse))
    
    # Метод для подсветки границ экрана (УПРОЩЁННЫЙ)
    def draw_glow_effect(self):
        """Рисует свечение по краям экрана"""
        if self.glow_surface is None:
            # Создаем поверхность для свечения (один раз)
            self.glow_surface = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
            
            # Цвет свечения (просто белый для всех состояний)
            r, g, b = 255, 255, 255  # белый цвет
            
            # Рисуем несколько слоев с разной прозрачностью
            for i in range(8):
                alpha = 40 - i * 5  # от 40 до 5 прозрачности
                width = 2 + i  # от 2 до 9 пикселей толщины
                color_with_alpha = (r, g, b, alpha)
                pygame.draw.rect(self.glow_surface, color_with_alpha,
                               (i, i, screen_x - 2*i, screen_y - 2*i), width)
        
        # Рисуем свечение на экран
        self.screen.blit(self.glow_surface, (0, 0))

    def update_game(self):  # обновление игрового мира 10 раз в секунду 
        """Обновляем состояние игры: двигаем змейку, проверяем столкновения"""
        # Если не в игре - ничего не обновляем
        if self.state != 1:
            return
        
        # Обновление эффектов
        self.update_particles()  # обновляем частицы

        self.snake.move()    # Двигаем змейку
        #check_self_collision, check_wall_collision проверяем
        if self.snake.check_self_collision() or self.snake.check_wall_collision(): 
            play_dead_sound()
            self.state = 3  # Если врезалась, переходим в состояние "проиграли"
            stop_bg_music()  # Останавливаем музыку при проигрыше
            return
        
        # Проверяем, не съела ли змейка еду
        if check_food_eaten(self.snake.get_head_position()):
            # Создаем частицы на ПОЗИЦИИ ГОЛОВЫ змейки (в момент касания)
            head_x, head_y = self.snake.get_head_position()
            self.create_particles(head_x, head_y)
            
            play_eat_sound()  # звук поедания
            self.snake.grow()  # змейка растет мгновенно
            increase_score(1)  # +1 очко
            self.food = spawn_food(self.snake.get_body())  # создаем новую еду

    def draw(self):
        """Рисуем всё на экране"""
        # Делаем фон черным
        self.screen.fill((0, 0, 0))  # черный фон
        
        # Рисуем эффекты
        self.draw_glow_effect()  # подсветка границ
        self.draw_animated_food()  # анимированная еда вместо draw_food
        self.draw_particles()  # частицы
  
        self.snake.draw(self.screen)  # рисуем змейку
        
        # Рисуем счет в левом верхнем углу
        score_text = self.font_normal.render(f"Счет: {get_score()}", True, (255, 255, 255))   # белый текст
        self.screen.blit(score_text, (10, 10))
        
        # В зависимости от состояния игры показываем разный текст/иконки
        if self.state == 0:  # Стартовый экран
            title = self.font_big.render("ЗМЕЙКА", True, (0, 255, 0))  # зеленый
            start = self.font_normal.render("ПРОБЕЛ - начать", True, (255, 255, 255))
            exit_text = self.font_normal.render("ESC - выйти", True, (255, 255, 255))
            
            self.screen.blit(title, (screen_x//2 - title.get_width()//2, screen_y//2 + 20))
            self.screen.blit(start, (screen_x//2 - start.get_width()//2, screen_y//2 + 80))
            self.screen.blit(exit_text, (screen_x//2 - exit_text.get_width()//2, screen_y//2 + 130))
        
        elif self.state == 2:  # Пауза
            pause = self.font_big.render("ПАУЗА", True, (0, 0, 255))  # синий
            continue_text = self.font_normal.render("ESC - продолжить", True, (255, 255, 255))
            restart = self.font_normal.render("R - начать заново", True, (255, 255, 255))
            
            self.screen.blit(pause, (screen_x//2 - pause.get_width()//2, screen_y//3))
            self.screen.blit(continue_text, (screen_x//2 - continue_text.get_width()//2, screen_y//2))
            self.screen.blit(restart, (screen_x//2 - restart.get_width()//2, screen_y//2 + 50))
        
        elif self.state == 3:  # Проиграли
            game_over = self.font_big.render("ПРОИГРАЛИ!", True, (255, 0, 0))  # красный
            score_final = self.font_normal.render(f"Ваш счет: {get_score()}", True, (255, 255, 255))
            restart = self.font_normal.render("R - начать заново", True, (0, 255, 0))  # зеленый
            menu = self.font_normal.render("ESC - в меню", True, (255, 255, 255))
            
            self.screen.blit(game_over, (screen_x//2 - game_over.get_width()//2, screen_y//3))
            self.screen.blit(score_final, (screen_x//2 - score_final.get_width()//2, screen_y//2))
            self.screen.blit(restart, (screen_x//2 - restart.get_width()//2, screen_y//2 + 50))
            self.screen.blit(menu, (screen_x//2 - menu.get_width()//2, screen_y//2 + 100))
        
        # Обновляем экран
        pygame.display.flip()

    def reset_game(self):     
        self.snake.reset()
        from food import reset_score, spawn_food
        reset_score()
        self.food = spawn_food(self.snake.get_body())
        self.state = 1
        
        # Сброс эффектов
        self.particles = []  # очищаем частицы
        self.glow_surface = None  # сбрасываем подсветку
        
        # Перезапуск фоновой музыки после reset
        stop_bg_music()
        if os.path.exists("SFX/BG_Music.mp3"):
            load_bg_music("BG_Music.mp3")

    def run(self):
        """цикл работает пока игра не закрыта"""
        while True:
            self.handle_events()   # 1. Проверяем нажатия клавиш
            self.update_game()     # 2. Обновляем игру
            self.draw()            # 3. Рисуем всё на экране
            self.clock.tick(FPS)   # 4. Контролируем скорость

# Точка входа в программу (СНАРУЖИ класса!) - импортируется из main.py
def start_game():
    """Функция которая запускает игру"""
    game = GameEngine()
    game.run()