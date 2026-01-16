import pygame
import os

# Инициализация mixer (безопасно)
try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
except:
    print("Mixer не инициализирован")

SFX_DIR = "SFX"

# регуляторы громкости
VOLUME_EAT = 0.8      # Еда
VOLUME_DEAD = 0.7     # Смерть  
VOLUME_PAUSE = 0.5    # Пауза
VOLUME_BUTTON = 0.6   # Кнопки
VOLUME_MUSIC = 0.3    # Музыка

eat_sound = None
dead_sound = None
pause_sound = None
p_sound = None

# Загрузка всех звуков с установкой громкости
for sound_file in ["eat.wav", "dead.wav", "pause.wav", "p.wav"]:
    sound_path = os.path.join(SFX_DIR, sound_file)
    if os.path.exists(sound_path):
        try:
            sound_obj = pygame.mixer.Sound(sound_path)
            if sound_file == "eat.wav":
                eat_sound = sound_obj
                eat_sound.set_volume(VOLUME_EAT)
            elif sound_file == "dead.wav":
                dead_sound = sound_obj
                dead_sound.set_volume(VOLUME_DEAD)
            elif sound_file == "pause.wav":
                pause_sound = sound_obj
                pause_sound.set_volume(VOLUME_PAUSE)
            elif sound_file == "p.wav":
                p_sound = sound_obj
                p_sound.set_volume(VOLUME_BUTTON)
            print(f"{sound_file} загружен (громкость {locals()[f"VOLUME_{sound_file.split('.')[0].upper()}"]})")
        except Exception as e:
            print(f"Ошибка {sound_file}: {e}")
    else:
        print(f"{sound_file} не найден")

def play_eat_sound():
    """Проигрывает звук поедания еды"""
    if eat_sound:
        eat_sound.play()

def play_dead_sound():
    """Звук смерти"""
    if dead_sound:
        dead_sound.play()

def play_pause_sound():
    """Звук паузы"""
    if pause_sound:
        pause_sound.play()

def play_button_sound():
    """Звук кнопок"""
    if p_sound:
        p_sound.play()

def load_bg_music(filename):
    """Загружает фоновую музыку"""
    global bg_music_loaded
    music_path = os.path.join(SFX_DIR, filename)
    if os.path.exists(music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Бесконечный цикл
            pygame.mixer.music.set_volume(VOLUME_MUSIC)  # Громкость музыки
            print(f"Музыка {filename} запущена (громкость {VOLUME_MUSIC})")
        except Exception as e:
            print(f"Ошибка музыки {filename}: {e}")
    else:
        print(f"{filename} не найден")

def stop_bg_music():
    """Останавливает музыку"""
    try:
        pygame.mixer.music.stop()
    except:
        pass

# Функции изменения громкости (бонус)
def set_eat_volume(volume):  # 0.0 - 1.0
    global VOLUME_EAT
    VOLUME_EAT = volume
    if eat_sound: eat_sound.set_volume(volume)

def set_music_volume(volume):
    global VOLUME_MUSIC
    VOLUME_MUSIC = volume
    pygame.mixer.music.set_volume(volume)
