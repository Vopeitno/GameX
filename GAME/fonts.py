import pygame
import os

FONT_DIR = "FONTS"

OSWALD_PATH = os.path.join(FONT_DIR, "Oswald.ttf")

def get_font(size):
    if os.path.exists(OSWALD_PATH):
        print("Oswald загружен!")
        return pygame.font.Font(OSWALD_PATH, size)
    print("Oswald не найден - системный шрифт")
    return pygame.font.Font(None, size)
