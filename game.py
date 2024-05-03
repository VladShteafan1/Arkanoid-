import pygame
from random import randrange as rnd, choice
from bonus import Bonus


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1200, 800
        self.fps = 60

        self.max_paddle_width = 660
        self.min_paddle_width = 165

        self.paddle_w = 330
        self.paddle_h = 35
        self.paddle_speed = 15
        self.paddle = pygame.Rect(self.WIDTH // 2 - self.paddle_w // 2, self.HEIGHT - self.paddle_h - 10, self.paddle_w,
                                  self.paddle_h)

        self.max_ball_speed = 10
        self.min_ball_speed = 4

        self.ball_radius = 20
        self.ball_speed = 6
        self.ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(self.ball_rect, self.WIDTH - self.ball_rect), self.HEIGHT // 2, self.ball_rect,
                                self.ball_rect)
        self.dx, self.dy = 1, -1

        self.block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

        pygame.init()
        self.sc = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36)

        self.font_size = 72
        self.font = pygame.font.Font(None, self.font_size)

        self.background_color = pygame.Color('black')

        self.bonus_list = []
        self.bonus_drop_chance = 1

        self.paddle_extension_duration = 5000
        self.paddle_extended = False
        self.paddle_extension_end_time = 0

