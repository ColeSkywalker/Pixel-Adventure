import pygame

from config import ANIMATION_DELAY, CHICKEN_VEL, GRAVITY
from src.enemies.enemies import Enemies


class FatBird(Enemies):
    def __init__(self, x, y):
        super().__init__("fatbird", x, y, 40, 48)
        self.fall_count = 0
        self.rect = pygame.Rect(x, y, 32, 34)
        self.x_vel = 0
        self.y_vel = 0
        self.animation_count = 0
        self.sprites = self.load_sprite_sheets("Enemies", "FatBird", 32, 34, True)
        self.sprite = self.sprites["Idle"][0]
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hit = False

    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.hit:
            sprite_sheet = "Hit"
        elif self.y_vel != 0:
            sprite_sheet = "Fall"
        elif self.fall_count == 1:
            sprite_sheet = "Ground"


        sprite_sheet_name = sprite_sheet

        if sprite_sheet_name not in self.sprites:
            sprite_sheet_name = "Idle" + self.direction

        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        x, y = self.rect.topleft
        self.rect.size = self.sprite.get_size()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

    # Movimentation

    def move(self, dy):
        self.rect.y += dy

    def get_hitted(self):
        return True

    def loop(self, player, objects):
        self.y_vel += GRAVITY
        self.move(self.y_vel)
        self.handle_vertical_collision(objects, self.y_vel)
        self.update_sprite()
        self.update_ai(player, objects)

    def handle_vertical_collision(self, objects, dy):
        collided_objects = []
        for obj in objects:
            if hasattr(obj, 'mask') and hasattr(self, 'mask'):
                if pygame.sprite.collide_mask(self, obj):
                    if dy > 0:  # Moving down
                        self.rect.bottom = obj.rect.top
                        self.y_vel = 0  # Landed
                    elif dy < 0:  # Moving up
                        self.rect.top = obj.rect.bottom
                        self.y_vel = 0  # Hit ceiling
                    collided_objects.append(obj)
        return collided_objects

    def collide(self, objects, dx):
        self.move(dx, 0)
        self.update()
        collided_object = None
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                collided_object = obj
                break
        self.move(-dx, 0)
        self.update()

        return collided_object

    def update_ai(self, player, objects):
        print("jfkdjsfl")




