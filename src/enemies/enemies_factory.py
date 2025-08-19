from src.enemies.chicken import Chicken
from src.enemies.fat_bird import FatBird
from src.enemies.mushroom import Mushroom


class EnemiesFactory:
    def __init__(self):
        self._enemy_types = {
            "chicken": Chicken,
            "fatbird": FatBird,
            "mushroom": Mushroom
        }

    def create(self, name, x, y):
        enemy_class = self._enemy_types.get(name.replace(" ", "").lower())
        if not enemy_class:
            raise ValueError(f"Inimigo '{name}' não encontrado")
        return enemy_class(x, y)

