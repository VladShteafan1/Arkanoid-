import pygame
from random import choice

class Bonus:
    def __init__(self, x, y):
        """
            Ініціалізує об'єкт бонусу з вказанням його розмірів та позиції
        """
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(x - self.width // 2, y - self.height // 2, self.width, self.height)
        self.type = choice(["speed_up", "paddle_extension", "ball_speed_decrease", "paddle_size_decrease"])
    def move(self):
        """
            Зміщує бонус вниз по екрану.
        """
        self.rect.y += 5