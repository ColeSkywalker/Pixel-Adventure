import pygame

from config import ANIMATION_DELAY, CHICKEN_VEL, GRAVITY
from src.enemies.enemies import Enemies


class Chicken(Enemies):
    def __init__(self, x, y):
        super().__init__("chicken", x, y, 32, 34)
        self.rect = pygame.Rect(x, y, 32, 34)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.animation_count = 0
        self.sprites = self.load_sprite_sheets("Enemies", "Chicken", 32, 34, True)
        self.sprite = self.sprites["Idle_left"][0]
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hit = False
        self.is_patrolling = True
        self.patrol_direction = -1

    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.hit:
            sprite_sheet = "Hit"
        elif self.x_vel != 0:
            sprite_sheet = "Run"

        if self.x_vel < 0:
            self.direction = "left"
        elif self.x_vel > 0:
            self.direction = "right"

        sprite_sheet_name = sprite_sheet + "_" + self.direction

        if sprite_sheet_name not in self.sprites:
            sprite_sheet_name = "Idle_" + self.direction

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

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def get_hitted(self):
        return True

    def loop(self, player, objects):
        self.y_vel += GRAVITY
        self.move(self.x_vel, self.y_vel)
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
        vision_range = 500
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        collide_left = self.collide(objects, -CHICKEN_VEL * 2)
        collide_right = self.collide(objects, CHICKEN_VEL * 2)

        if abs(dx) < vision_range and abs(dy) < 50:
            self.x_vel = 0
            if dx > 0 and not collide_right:
                self.move_right(CHICKEN_VEL)
            elif dx < 0 and not collide_left:
                self.move_left(CHICKEN_VEL)
        else:
            self.is_patrolling = True

            # Checa por colisão na direção atual
            patrol_velocity = CHICKEN_VEL * self.patrol_direction

            # Se a colisão ocorrer no próximo passo, inverte a direção
            if self.collide(objects, patrol_velocity):
                self.patrol_direction *= -1

            # Move o frango na nova direção de patrulha
            if self.patrol_direction == -1:
                self.move_left(CHICKEN_VEL)
            elif self.patrol_direction == 1:
                self.move_right(CHICKEN_VEL)

