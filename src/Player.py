import pygame.sprite
from os import listdir
from os.path import isfile, join

from src.SpriteEntity import SpriteEntity
from config import *

class Player(SpriteEntity):


    def __init__(self, x ,y, width, height):
        super().__init__(x ,y, width, height)
        self.fruits = 0
        self.rect = pygame.Rect(x,y,width,height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.sprites = self.load_sprite_sheets("Main Characters", "Pink Man", 32, 32, True)
        self.jump_count = 0
        self.jump_key_pressed = False
        self.hit = False
        self.hit_count = 0
        self.catch_fruit = False

    # Sprites
    def flip(self, sprites):
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

    def load_sprite_sheets(self, dir1, dir2, width, height, direction = False):
        path = join("assets", dir1, dir2)
        images = [f for f in listdir(path) if isfile(join(path, f))]

        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

            sprites = []
            for i in range(sprite_sheet.get_width()// width):
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                surface.blit(sprite_sheet, (0, 0), rect)
                sprites.append(pygame.transform.scale2x(surface))
            if direction:
                all_sprites[image.replace(".png", "") + "_right"] = sprites
                all_sprites[image.replace(".png", "") + "_left"] = self.flip(sprites)
            else:
                all_sprites[image.replace(".png", "")] = sprites

        return all_sprites

    # Movimentacao
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

    def jump(self):
        self.y_vel = -GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def loop(self, fps):
        self.y_vel += min(1,(self.fall_count / fps) * GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > FPS * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.hit_count = 0
        self.y_vel *= -1

    def take_hit(self):
        self.hit = True
        self.hit_count = 0
        
    def take_fruit(self, fruit):
        self.catch_fruit = True
        self.fruits += fruit
        
    def update_sprite(self):
        sprite_sheet = "Idle"
        if self.hit:
            sprite_sheet = "Hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "Jump"
            elif self.jump_count == 2:
                sprite_sheet = "DoubleJump"
        elif self.y_vel > GRAVITY * 2:
            sprite_sheet = "Fall"
        elif self.x_vel != 0:
            sprite_sheet = "Run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.sprites[sprite_sheet_name]
        sprite_index = (self.animation_count // ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))



    def handle_vertical_collision(self , objects, dy):
        collided_objects = []
        for obj in objects:
            if pygame.sprite.collide_mask(self, obj):
                if dy > 0:
                    self.rect.bottom = obj.rect.top
                    self.landed()
                elif dy < 0:
                    self.rect.top = obj.rect.bottom
                    self.hit_head()

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

    def handle_move(self, objects):
        keys = pygame.key.get_pressed()

        self.x_vel = 0
        collide_left = self.collide(objects, -PLAYER_VEL * 2)
        collide_right = self.collide(objects, PLAYER_VEL * 2)

        if keys[pygame.K_LEFT] and not collide_left:
            self.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT] and not collide_right:
            self.move_right(PLAYER_VEL)

        if keys[pygame.K_SPACE]:
            if not self.jump_key_pressed and self.jump_count < 2:
                self.jump()
                self.jump_key_pressed = True
        else:
            self.jump_key_pressed = False

        self.handle_vertical_collision(objects, self.y_vel)


