import pygame
import pytest

from game import Game
from bonus import Bonus

# Використання фікстури для ініціалізації гри перед кожним тестом
@pytest.fixture
def initialized_game():
    pygame.init()
    game = Game()
    yield game
    pygame.quit()

# Тест перевіряє, що гра ініціалізується коректно
def test_game_initialization(initialized_game):
    game = initialized_game
    assert game.block_list
    assert game.paddle
    assert game.ball
    assert game.bonus_list

# Тест перевіряє оновлення платформи
def test_update_paddle(initialized_game):
    game = initialized_game
    game.update_paddle()
    assert game.paddle

# Параметризований тест для перевірки виявлення колізій
@pytest.mark.parametrize("dx, dy, expected_dx, expected_dy", [
    (1, -1, -1, 1),
    (-1, 1, 1, -1),
    (1, 1, -1, -1),
    (-1, -1, 1, 1),
])
def test_detect_collision(dx, dy, expected_dx, expected_dy):
    game = Game()
    ball = pygame.Rect(100, 100, 10, 10)
    paddle = pygame.Rect(200, 200, 50, 10)
    new_dx, new_dy = game.detect_collision(dx, dy, ball, paddle)
    assert new_dx == expected_dx
    assert new_dy == expected_dy

# Параметризований тест для активації розширення платформи
@pytest.mark.parametrize("paddle_width, expected_width", [
    (330, 660),
    (200, 400),
    (165, 330),
])
def test_activate_paddle_extension(initialized_game, paddle_width, expected_width):
    game = initialized_game
    game.paddle.width = paddle_width
    bonus = Bonus(100, 100)
    bonus.type = "paddle_extension"
    game.activate_bonus(bonus)
    assert game.paddle.width == expected_width