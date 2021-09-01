import pygame
import random
from pygame.locals import *
import os


WIDTH = 1024
HEIGHT = 838
FPS = 60
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DIRT = "sprites/blocks/Dirt.png"
animation_frames = {"player_walk" : []}

for i in range(1, 15):
    sprite = pygame.image.load(f"sprites/player/Player_Walk ({i}).gif")
    animation_frames["player_walk"].append(sprite)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/player/Player_Walk (1).gif")
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.is_falling = True
        self.state = "idle"
        self.frame_number = 0
        self.ticks_from_last_frame = pygame.time.get_ticks()
        self.view_direction = "right"
        self.is_jumping = False
    
    
    def key_checker(self, key):
        if key == pygame.K_SPACE and not self.is_jumping:
            self.max_jump_height = self.rect.y - 50
            self.is_jumping = True

    def jump(self):
        if self.is_jumping:
            self.rect.y -= 5
            if self.rect.y == self.max_jump_height:
                self.is_jumping = False

    def animation(self, state="move"):
        now = pygame.time.get_ticks()
        if now - self.ticks_from_last_frame > 100:
            self.ticks_from_last_frame = now
            self.frame_number += 1
            if self.frame_number == 14:
                self.frame_number = 0
            _sprite = animation_frames["player_walk"][self.frame_number]
            self.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)


    def set_idle(self):
        _sprite = pygame.image.load("sprites/player/Player_Walk (1).gif")
        self.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)
            

    def move(self):
        keys = pygame.key.get_pressed()
        if keys [K_a]:
            self.rect.x -= 2
            self.state = "move"
            self.view_direction = "left"
        elif keys [K_d]:
            self.rect.x += 2
            self.state = "move"
            self.view_direction = "right"
        else:
            self.state = "idle"
            self.set_idle()

    def gravity(self):
        if self.is_falling:
            self.rect.y += 2


    def update(self):
        self.gravity()
        self.move()
        if self.state == "move":
            self.animation()
        self.jump()

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("sprites/background.png")
        self.bg_rect = self.bg.get_rect()
        self.create_ground()
        self.is_continue = True
    
    def create_ground(self):
        for x in range(0, 1024, 32):
            ground_block = Block(DIRT, x, 600)
            sprites.add(ground_block)
            grounds.add(ground_block)
    
    def run(self):
        while self.is_continue:
            self.surface.fill(BLACK)
            self.surface.blit(self.bg, self.bg_rect)
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    player.key_checker(event.key)


            sprites.update()
            player_ground_collision = pygame.sprite.spritecollide(player, grounds, False)
            if player_ground_collision:
                player.is_falling = False
            else:
                player.is_falling = True

            sprites.draw(self.surface)

            pygame.display.flip()
    

class Block(pygame.sprite.Sprite):
    def __init__(self, block, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(block)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

sprites = pygame.sprite.Group()
grounds = pygame.sprite.Group()
player = Player()
sprites.add(player)

if __name__ == '__main__':
    g = Game()
    g.run()