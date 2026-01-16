import pygame  # импорт библиотеки для игр
import sys  #  импорт для выхода из программы
import os   # для проверки путей к файлам
from config import *
from snake import Snake # импортируем все из кода Арсена
from food import spawn_food, draw_food, check_food_eaten, increase_score, get_score
from sfx import load_bg_music, stop_bg_music, play_eat_sound, play_dead_sound, play_button_sound, play_pause_sound  # Импорт SFX
from fonts import get_font  # Импорт шрифтов


class GameEngine:   # создание чертежа для игры 
    """управление всего что происходит на экране""" 
    
    def __init__(self):
        pygame.init()  # Запускаем pygame
        
        self.screen = pygame.display.set_mode((screen_x, screen_y)) # Создаем окно игры 720 на 480
        pygame.display.set_caption("Змейка")
        
        self.clock = pygame.time.Clock()    # Часы для контроля скорости игры

        self.state = 0  # Текущее состояние игры 0 это экран меню 
        
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

    def update_game(self):  # обновление игрового мира 10 раз в секунду 
        """Обновляем состояние игры: двигаем змейку, проверяем столкновения"""
        # Если не в игре - ничего не обновляем
        if self.state != 1:
            return
        
        self.snake.move()    # Двигаем змейку
        #check_self_collision, check_wall_collision проверяем
        if self.snake.check_self_collision() or self.snake.check_wall_collision(): 
            play_dead_sound()
            self.state = 3  # Если врезалась, переходим в состояние "проиграли"
            stop_bg_music()  # Останавливаем музыку при проигрыше
            return
        
        # Проверяем, не съела ли змейка еду
        if check_food_eaten(self.snake.get_head_position()):
            self.snake.grow()          # Змейка растет
            increase_score(1)          # +1 очко
            play_eat_sound()           # Звук поедания еды!
            self.food = spawn_food(self.snake.get_body())  # создаем новую еду если змейка съела прошлую

    def draw(self):
        """Рисуем всё на экране"""
        # Делаем фон черным
        self.screen.fill(black)
        
        # Рисуем еду и змейку, благодаря методам и функция из food.py snake.py
        draw_food(self.screen)
        self.snake.draw(self.screen)
        
        # Рисуем счет в левом верхнем углу
        score_text = self.font_normal.render(f"Счет: {get_score()}", True, white)   # функция render() создание кортинки и текста
        self.screen.blit(score_text, (10, 10))  # blit()  рисует эту картинку 
        
        # В зависимости от состояния игры показываем разный текст
        if self.state == 0:  # Стартовый экран
            title = self.font_big.render("ЗМЕЙКА", True, green)
            start = self.font_normal.render("ПРОБЕЛ - начать", True, white)
            exit_text = self.font_normal.render("ESC - выйти", True, white)
            
            self.screen.blit(title, (screen_x//2 - title.get_width()//2, screen_y//2 + 20))
            self.screen.blit(start, (screen_x//2 - start.get_width()//2, screen_y//2 + 80))
            self.screen.blit(exit_text, (screen_x//2 - exit_text.get_width()//2, screen_y//2 + 130))
        
        elif self.state == 2:  # Пауза
            pause = self.font_big.render("ПАУЗА", True, blue)
            continue_text = self.font_normal.render("ESC - продолжить", True, white)
            restart = self.font_normal.render("R - начать заново", True, white)
            
            self.screen.blit(pause, (screen_x//2 - pause.get_width()//2, screen_y//3))
            self.screen.blit(continue_text, (screen_x//2 - continue_text.get_width()//2, screen_y//2))
            self.screen.blit(restart, (screen_x//2 - restart.get_width()//2, screen_y//2 + 50))
        
        elif self.state == 3:  # Проиграли
            game_over = self.font_big.render("ПРОИГРАЛИ!", True, red)
            score_final = self.font_normal.render(f"Ваш счет: {get_score()}", True, white)
            restart = self.font_normal.render("R - начать заново", True, green)
            menu = self.font_normal.render("ESC - в меню", True, white)
            
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
