import pygame
import os

# ← НОВОЕ: переходим в папку GAME!
os.chdir("GAME")

from game import start_game

if __name__ == "__main__":
    pygame.init()
    start_game()
