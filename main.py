import pygame
from pygame.locals import *
import sys
import math

#from audio import *

pygame.init()

vec = pygame.math.Vector2 
HEIGHT = 580
WIDTH = 640
LEFT = 0
RIGHT = 1
FPS = 60
FramePerSec = pygame.time.Clock()
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Button:
    def __init__(self, pos, width, height, text=""):
        self.rect = pygame.Rect(pos, (width, height))
        self.color = (255, 255, 255)
        self.pos = pos
        self.end_x = pos[0] + width
        self.end_y = pos[1] + height

    def PressButton(self, MousePos):
        if (MousePos[0] <= self.end_x) and (MousePos[0] >= self.pos[0]) and (MousePos[1] <= self.end_y) and (MousePos[1] >= self.pos[1]):
            return True

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


def StartMenu():
    pygame.init()
    ButtonIndent = 60
    TextIndent = 10

    StartButton = Button((ButtonIndent, 375), 450, 100)
    ExitButton = Button((ButtonIndent, 500), 150, 50)
    ReturnButton = Button((ButtonIndent, 500), 150, 50)

    OnePlayerButton = Button((ButtonIndent, 330), 450, 65)
    TwoPlayerButton = Button((ButtonIndent, 410), 450, 65)

    EasyButton = Button((ButtonIndent, 300), 450, 50)
    MediumButton = Button((ButtonIndent, 365), 450, 50)
    HardButton = Button((ButtonIndent, 430), 450, 50)

    Screen = displaysurface#Display(640, 580)
    clock = pygame.time.Clock()
    running = True
    screen_index = 1

    Big_Font = pygame.font.SysFont('Roboto', 100)
    Medium_Font = pygame.font.SysFont('Roboto', 70)
    Small_Font = pygame.font.SysFont('Roboto', 60)
    Title_Font = pygame.font.SysFont("Impact", 250)
    Subtitle_Font = pygame.font.SysFont("Impact", 37)

    Pong_Text = Title_Font.render("PONG", True, (255, 255, 255), (0, 0, 0))
    Sub_Text = Subtitle_Font.render("By Team 3", True, (255, 255, 255), (0, 0, 0))
    Start_Text = Big_Font.render("Start Game", True, (0, 0, 0), (255, 255, 255))
    Single_Text = Medium_Font.render("Singleplayer", True, (0, 0, 0), (255, 255, 255))
    Multi_Text = Medium_Font.render("Multiplayer", True, (0, 0, 0), (255, 255, 255))
    Easy_Text = Small_Font.render("Easy CPU", True, (0, 0, 0), (255, 255, 255))
    Medium_Text = Small_Font.render("Medium CPU", True, (0, 0, 0), (255, 255, 255))
    Hard_Text = Small_Font.render("Hard CPU", True, (0, 0, 0), (255, 255, 255))
    Exit_Text = Small_Font.render("Quit", True, (0, 0, 0), (255, 255, 255))
    Back_Text = Small_Font.render("Back", True, (0, 0, 0), (255, 255, 255))

    while running is True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if screen_index == 3:
                    if EasyButton.PressButton(pos):
                        print("WIP: Easy CPU")
                        running = False
                    if MediumButton.PressButton(pos):
                        print("WIP: Medium CPU")
                        running = False
                    if HardButton.PressButton(pos):
                        print("WIP: Hard CPU")
                        running = False

                if screen_index == 2:
                    if OnePlayerButton.PressButton(pos):
                        screen_index = 3
                    if TwoPlayerButton.PressButton(pos):
                        running = False

                if screen_index == 1:
                    if StartButton.PressButton(pos):
                        screen_index = 2
                    if ExitButton.PressButton(pos):
                        sys.exit()
                if (screen_index == 2) or (screen_index == 3):
                    if ReturnButton.PressButton(pos):
                        screen_index = 1

        if screen_index == 1:
            Screen.fill((0, 0, 0))
            pygame.draw.rect(Screen, StartButton.color, StartButton.rect)
            pygame.draw.rect(Screen, ExitButton.color, ExitButton.rect)

            Screen.blit(Start_Text, (StartButton.pos[0] + TextIndent, StartButton.pos[1] + 15))
            Screen.blit(Exit_Text, (ExitButton.pos[0] + TextIndent, ExitButton.pos[1] + 5))

        if screen_index == 2:
            Screen.fill((0, 0, 0))
            pygame.draw.rect(Screen, OnePlayerButton.color, OnePlayerButton.rect)
            pygame.draw.rect(Screen, TwoPlayerButton.color, TwoPlayerButton.rect)
            pygame.draw.rect(Screen, ReturnButton.color, ReturnButton.rect)

            Screen.blit(Single_Text, (OnePlayerButton.pos[0] + TextIndent, OnePlayerButton.pos[1] + 10))
            Screen.blit(Multi_Text, (TwoPlayerButton.pos[0] + TextIndent, TwoPlayerButton.pos[1] + 10))
            Screen.blit(Back_Text, (ExitButton.pos[0] + TextIndent, ExitButton.pos[1] + 5))

        if screen_index == 3:
            Screen.fill((0, 0, 0))
            pygame.draw.rect(Screen, EasyButton.color, EasyButton.rect)
            pygame.draw.rect(Screen, MediumButton.color, MediumButton.rect)
            pygame.draw.rect(Screen, HardButton.color, HardButton.rect)
            pygame.draw.rect(Screen, ReturnButton.color, ReturnButton.rect)

            Screen.blit(Back_Text, (ExitButton.pos[0] + TextIndent, ExitButton.pos[1] + 5))
            Screen.blit(Easy_Text, (EasyButton.pos[0] + TextIndent, EasyButton.pos[1] + 5))
            Screen.blit(Medium_Text, (MediumButton.pos[0] + TextIndent, MediumButton.pos[1] + 5))
            Screen.blit(Hard_Text, (HardButton.pos[0] + TextIndent, HardButton.pos[1] + 5))

        Screen.blit(Pong_Text, (60, -20))
        Screen.blit(Sub_Text, (435, 240))
        pygame.display.flip()


if __name__ == '__main__':
    StartMenu()
    main()