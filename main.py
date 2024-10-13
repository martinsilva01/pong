import pygame
from pygame.locals import *
import sys
import math

#from audio import *

pygame.init()

vec = pygame.math.Vector2 
HEIGHT = 480
WIDTH = 640
LEFT = 0
RIGHT = 1
FPS = 60
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
 
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, l_or_r):
        super().__init__() 
        self.surf = pygame.Surface((15, 75))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
        self.speed = 10
   
        self.pos = vec((x, y))
        self.rect.center = self.pos 
        self.l_or_r = l_or_r
 
    def move(self):    
        pressed_keys = pygame.key.get_pressed()  

        if (pressed_keys[K_s] and self.l_or_r == 0) or (pressed_keys[K_DOWN] and self.l_or_r == 1):
            if(self.pos.y >= HEIGHT - self.rect.h/2):
                self.pos.y = HEIGHT - self.rect.h/2
            else:
                self.pos.y += self.speed
        if (pressed_keys[K_w] and self.l_or_r == 0) or (pressed_keys[K_UP] and self.l_or_r == 1):
            if(self.pos.y <= 0 + self.rect.h/2):
                self.pos.y = 0 + self.rect.h/2
            else:
                self.pos.y -= self.speed
            
        self.rect.center = self.pos    

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((x, y))
        self.rect.center = self.pos 

        self.direction = [1, 0]
        self.velocity = 4
    
    def move(self):
        self.pos.x += self.direction[0] * self.velocity
        self.pos.y += self.direction[1] * self.velocity

        self.rect.center = self.pos    

    def boundary_bounce(self):
        self.direction[1] *= -1

    def bounce(self, paddle):
        self.direction[0] *= -1
        self.direction[1] = ((paddle.pos[1] - self.pos[1]) / (paddle.rect.h / 2))

    def set_speed(self, newVel):
        self.velocity = newVel

    def change_angle(self, newAng):
        self.direction[0] = math.cos(newAng * math.pi / 180)
        self.direction[1] = math.sin(newAng * math.pi / 180)

class Bot(pygame.sprite.Sprite):
    def __init__(self, x, y, l_or_r):
        super().__init__()
        self.surf = pygame.Surface((15, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.speed = 10

        self.pos = vec((x, y))
        self.rect.center = self.pos
        self.l_or_r = l_or_r

    def BotMove(self, Range, Ball):
        if Ball.pos.x >= Range:
            if Ball.pos.y > self.pos.y:
                if (self.pos.y >= HEIGHT - self.rect.h / 2):
                    self.pos.y = HEIGHT - self.rect.h / 2
                else:
                    self.pos.y += self.speed
            if Ball.pos.y < self.pos.y:
                if (self.pos.y <= 0 + self.rect.h / 2):
                    self.pos.y = 0 + self.rect.h / 2
                else:
                    self.pos.y -= self.speed
        self.rect.center = self.pos



def main():
    BotSwitch = True
    Difficulty = "HARD"  # Manully Toggle BotSwitch and Difficulty for now
    Range = 0  # Reaction Time for the CPU opponent

    if Difficulty == "HARD":
        Range = 170
    elif Difficulty == "MEDIUM":
        Range = 350
    elif Difficulty == "EASY":
        Range = 475



    l_paddle = Paddle(60, HEIGHT/2, LEFT)

    if BotSwitch is True:  # Will create a Paddle object or Bot Object
        r_paddle = Bot(580, HEIGHT / 2, RIGHT)
    else:
        r_paddle = Paddle(580, HEIGHT / 2, RIGHT)

    pong_b = Ball(WIDTH/2, HEIGHT/2)
    
    paddlesGroup = pygame.sprite.Group()
    paddlesGroup.add(l_paddle)
    paddlesGroup.add(r_paddle)

    gamePieceGroup = pygame.sprite.Group()
    gamePieceGroup.add(pong_b)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        displaysurface.fill((0,0,0))
    
        l_paddle.move()

        if BotSwitch is True:  # Based on which opponent is playing
            r_paddle.BotMove(Range, pong_b)
        else:
            r_paddle.move()

        pong_b.move()
        for entity in paddlesGroup:
            displaysurface.blit(entity.surf, entity.rect)
        
        for entity in gamePieceGroup:
            displaysurface.blit(entity.surf, entity.rect)

        collided = pygame.sprite.spritecollide(pong_b, paddlesGroup, False)
        if collided:
            collided = collided[0] # will only ever collide with 1 paddle at a time.
            pong_b.bounce(collided)

        if pong_b.pos[1] <= 0 or pong_b.pos[1] >= HEIGHT:
            pong_b.boundary_bounce()

        if pong_b.velocity != 17:  # Ball will increase in speed every hit
            pong_b.velocity += 0.5  # These values can change depending on how you guys want it to feel
            # Also we will need to reset it to default value at the s

        
        pygame.display.update()
        FramePerSec.tick(FPS)



if __name__ == '__main__':
    main()