import pygame

from config import ANIMATION_DELAY, CHICKEN_VEL, GRAVITY, FPS
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
        self.is_dead = False
        self.death_timer = 0

    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.hit or self.is_dead:
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

    def die(self):
        self.x_vel = 0
        self.hit = True
        self.is_dead = True
        self.death_timer = FPS // 2

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

    def loop(self, player, objects):
        self.update_sprite()

        self.update_ai(player, objects)

        self.y_vel += GRAVITY

        # X
        self.move(self.x_vel, 0)
        self.handle_horizontal_collision(objects)
        # Y
        self.handle_vertical_collision(objects)

        if self.is_dead:
            self.death_timer -= 1
            if self.death_timer <= 0:
                return "remove"
        self.update_sprite()

    def handle_horizontal_collision(self, objects):
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if self.x_vel > 0:  # right
                    self.rect.right = obj.rect.left
                elif self.x_vel < 0:  # left
                    self.rect.left = obj.rect.right
                self.x_vel = 0

    def handle_vertical_collision(self, objects):
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if self.y_vel > 0:
                    self.rect.bottom = obj.rect.top
                elif self.y_vel < 0:
                    self.rect.top = obj.rect.bottom
                self.y_vel = 0

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
        if player.is_dead:
            return

        collide_left = self.collide(objects, -CHICKEN_VEL * 2)
        collide_right = self.collide(objects, CHICKEN_VEL * 2)

        if self.is_dead:
            self.x_vel = 0
            return

        player_on_top = (
                pygame.sprite.collide_mask(self, player) and
                player.y_vel > 0 and
                player.rect.bottom <= self.rect.top + 5
        )
        if player_on_top:

            self.x_vel = 0
            if self.patrol_direction == -1:
                if collide_left:
                    self.patrol_direction = 1
                else:
                    self.move_left(CHICKEN_VEL // 2)
            else:
                if collide_right:
                    self.patrol_direction = -1
                else:
                    self.move_right(CHICKEN_VEL // 2)
            return
        vision_range = 400
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.bottom - self.rect.bottom

        if abs(dx) < vision_range and abs(dy) < 150:
            if dx > 0 and not collide_right:
                self.move_right(CHICKEN_VEL)
            elif dx < 0 and not collide_left:
                self.move_left(CHICKEN_VEL)
        else:
        # Patrolling
            if self.patrol_direction == -1:
                if collide_left:
                    self.patrol_direction = 1
                else:
                    self.move_left(CHICKEN_VEL // 2)
            else:
                if collide_right:
                    self.patrol_direction = -1
                else:
                    self.move_right(CHICKEN_VEL // 2)


