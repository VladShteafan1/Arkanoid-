import pytest

from bonus import Bonus

@pytest.fixture
def initialized_bonus():
    return Bonus(100, 100)

def test_bonus_creation(initialized_bonus):
    bonus = initialized_bonus
    assert bonus.rect.x == 90
    assert bonus.rect.y == 90

def test_bonus_movement(initialized_bonus):
    bonus = initialized_bonus
    initial_y = bonus.rect.y
    bonus.move()
    assert bonus.rect.y == initial_y + 5
