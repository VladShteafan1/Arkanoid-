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

    def draw_blocks(self):
        for color, block in enumerate(self.block_list):
            pygame.draw.rect(self.sc, self.color_list[color], block)

    def draw_paddle(self):
        pygame.draw.rect(self.sc, pygame.Color('darkorange'), self.paddle)

    def draw_ball(self):
        pygame.draw.circle(self.sc, pygame.Color('white'), self.ball.center, self.ball_radius)

    def draw_bonuses(self):
        for bonus in self.bonus_list:
            pygame.draw.rect(self.sc, pygame.Color('green'), bonus.rect)

    def update_paddle(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.left -= self.paddle_speed
        if key[pygame.K_RIGHT] and self.paddle.right < self.WIDTH:
            self.paddle.right += self.paddle_speed

    def update_ball(self):
        self.ball.x += self.ball_speed * self.dx
        self.ball.y += self.ball_speed * self.dy

        if self.ball.centerx < self.ball_radius or self.ball.centerx > self.WIDTH - self.ball_radius:
            self.dx = -self.dx
        if self.ball.centery < self.ball_radius:
            self.dy = -self.dy
        if self.ball.colliderect(self.paddle) and self.dy > 0:
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, self.paddle)

        if self.ball.bottom > self.HEIGHT:
            self.game_over()

        hit_index = self.ball.collidelist(self.block_list)
        if hit_index != -1:
            hit_rect = self.block_list.pop(hit_index)
            hit_color = self.color_list.pop(hit_index)
            self.dx, self.dy = self.detect_collision(self.dx, self.dy, self.ball, hit_rect)
            hit_rect.inflate_ip(self.ball.width * 3, self.ball.height * 3)
            pygame.draw.rect(self.sc, hit_color, hit_rect)
            self.drop_bonus(hit_rect.centerx, hit_rect.bottom)

        self.update_bonuses()

    def drop_bonus(self, x, y):
            if rnd(0, 100) / 100 < self.bonus_drop_chance:
                self.bonus_list.append(Bonus(x, y))

    def update_bonuses(self):
        for bonus in self.bonus_list:
            bonus.move()
            if bonus.rect.colliderect(self.paddle):
                self.activate_bonus(bonus)
                self.bonus_list.remove(bonus)
            elif bonus.rect.top > self.HEIGHT:
                self.bonus_list.remove(bonus)

    def activate_bonus(self, bonus):
        if bonus.type == "speed_up":
            if self.ball_speed + 2 <= self.max_ball_speed:
                self.ball_speed += 2

        elif bonus.type == "ball_speed_decrease":
            if self.ball_speed - 2 >= self.min_ball_speed:
                self.ball_speed -= 2

        elif bonus.type == "paddle_extension":
            if self.paddle.width * 2 <= self.max_paddle_width:
                self.paddle.width *= 2

        elif bonus.type == "paddle_size_decrease":
            if self.paddle.width // 2 >= self.min_paddle_width:
                self.paddle.width //= 2

    def detect_collision(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    def check_win_condition(self):
        if not self.block_list:
            return True
        else:
            return False

    def game_over(self):
        self.sc.fill((0, 0, 0))
        game_over_text = self.font.render("YOU DIED", True, pygame.Color('red'))
        restart_text = self.font.render("Press 'R' to restart", True, pygame.Color('white'))
        text_rect = game_over_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.sc.blit(game_over_text, text_rect)
        self.sc.blit(restart_text, restart_rect)
        pygame.display.flip()

    def restart_game(self):
        self.__init__()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Если нажата клавиша 'R'
                        self.restart_game()

            self.sc.fill(self.background_color)

            self.draw_blocks()
            self.draw_paddle()
            self.draw_ball()
            self.draw_bonuses()

            self.update_paddle()
            self.update_ball()

            pygame.display.flip()
            self.clock.tick(self.fps)