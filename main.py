import pygame
from pygame.locals import *
import sys
import math
import time
import random
from audio import *

pygame.init()

# Constants
vec = pygame.math.Vector2
HEIGHT = 768
WIDTH = 1024
LEFT = 1
RIGHT = -1
FPS = 60
FramePerSec = pygame.time.Clock()

# Initialize music state
music_on = True

replay = True
BotSwitch = True  # if it is singleplayer
Difficulty = "HARD"  # Manully Toggle BotSwitch and Difficulty for now
Range = 0  # Reaction Time for the CPU opponent

# Set up display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Start background music
play_background_music()

# Menu buttons
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

# Paddle sprites
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, l_or_r):
        super().__init__() 
        self.surf = pygame.Surface((15, 75))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.speed = 10
   
        self.pos = vec((x, y))
        self.rect.center = self.pos 
        self.l_or_r = l_or_r
 
    def move(self):    
        pressed_keys = pygame.key.get_pressed()  

        if (pressed_keys[K_s] and self.l_or_r == LEFT) or (pressed_keys[K_DOWN] and self.l_or_r == RIGHT):
            if (self.pos.y >= HEIGHT - self.rect.h/2):
                self.pos.y = HEIGHT - self.rect.h/2
            else:
                self.pos.y += self.speed
        if (pressed_keys[K_w] and self.l_or_r == LEFT) or (pressed_keys[K_UP] and self.l_or_r == RIGHT):
            if (self.pos.y <= 0 + self.rect.h/2):
                self.pos.y = 0 + self.rect.h/2
            else:
                self.pos.y -= self.speed
            
        self.rect.center = self.pos    


# Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__() 
        self.surf = pygame.Surface((15, 15))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    
        self.pos = vec((x, y))
        self.rect.center = self.pos 
    
        self.direction = [1, 0]
        self.velocity = 6
    
    def move(self):
        self.pos.x += self.direction[0] * self.velocity
        self.pos.y += self.direction[1] * self.velocity
    
        self.rect.center = self.pos    
    
    def bounce(self, paddle):
        self.direction[0] *= -1
        self.direction[1] = ((paddle.pos[1] - self.pos[1]) / ((paddle.rect.h) / 2))
    
    def set_speed(self, newVel):
        self.velocity = newVel
    
    def change_angle(self, newAng):
        self.direction[0] = math.cos(newAng * math.pi / 180)
        self.direction[1] = math.sin(newAng * math.pi / 180)
    

# the cpu AI
class Bot(Paddle):
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


def StartMenu():
    ButtonIndent = (WIDTH / 4)
    TextIndent = 10
    global Difficulty
    global BotSwitch

    StartButton = Button((ButtonIndent, 350), 450, 100)
    ExitButton = Button((ButtonIndent, 500), 150, 50)
    ReturnButton = Button((ButtonIndent, 500), 150, 50)

    OnePlayerButton = Button((ButtonIndent, 330), 450, 65)
    TwoPlayerButton = Button((ButtonIndent, 410), 450, 65)

    EasyButton = Button((ButtonIndent, 300), 450, 50)
    MediumButton = Button((ButtonIndent, 365), 450, 50)
    HardButton = Button((ButtonIndent, 430), 450, 50)

    Screen = displaysurface
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
    Multi_Text = Medium_Font.render("Multiplayer (Bo5)", True, (0, 0, 0), (255, 255, 255))
    Easy_Text = Small_Font.render("Easy CPU", True, (0, 0, 0), (255, 255, 255))
    Medium_Text = Small_Font.render("Medium CPU", True, (0, 0, 0), (255, 255, 255))
    Hard_Text = Small_Font.render("Hard CPU", True, (0, 0, 0), (255, 255, 255))
    Exit_Text = Small_Font.render("Quit", True, (0, 0, 0), (255, 255, 255))
    Back_Text = Small_Font.render("Back", True, (0, 0, 0), (255, 255, 255))

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if screen_index == 3:
                    if EasyButton.PressButton(pos):
                        play_sound(button_select_sound)
                        print("WIP: Easy CPU")
                        Difficulty = "EASY"
                        running = False
                    if MediumButton.PressButton(pos):
                        play_sound(button_select_sound)
                        print("WIP: Medium CPU")
                        Difficulty = "MEDIUM"
                        running = False
                    if HardButton.PressButton(pos):
                        play_sound(button_select_sound)
                        print("WIP: Hard CPU")
                        Difficulty = "HARD"
                        running = False

                if screen_index == 2:
                    if OnePlayerButton.PressButton(pos):
                        play_sound(button_select_sound)
                        screen_index = 3
                        BotSwitch = True
                    if TwoPlayerButton.PressButton(pos):
                        play_sound(button_select_sound)
                        BotSwitch = False
                        running = False

                if screen_index == 1:
                    if StartButton.PressButton(pos):
                        play_sound(button_select_sound)
                        screen_index = 2
                    if ExitButton.PressButton(pos):
                        play_sound(button_select_sound)
                        sys.exit()
                if (screen_index == 2) or (screen_index == 3):
                    if ReturnButton.PressButton(pos):
                        play_sound(button_select_sound)
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
    
            Screen.blit(Easy_Text, (EasyButton.pos[0] + TextIndent, EasyButton.pos[1] + 5))
            Screen.blit(Medium_Text, (MediumButton.pos[0] + TextIndent, MediumButton.pos[1] + 5))
            Screen.blit(Hard_Text, (HardButton.pos[0] + TextIndent, HardButton.pos[1] + 5))
            Screen.blit(Back_Text, (ReturnButton.pos[0] + TextIndent, ReturnButton.pos[1] + 5))
        Screen.blit(Pong_Text, ((WIDTH / 2) - 250, (HEIGHT / 10)))
        Screen.blit(Sub_Text, ((WIDTH / 2) - 250, 150 + (HEIGHT / 10)))

        pygame.display.flip()

def EndMenu(score):
    ButtonIndent = (WIDTH / 4)
    TextIndent = 10
    global Difficulty
    global BotSwitch

    MenuButton = Button((ButtonIndent, HEIGHT * 0.5), 300, 70)
    QuitButton = Button((ButtonIndent, HEIGHT * 0.6), 300, 70)
    
    Screen = displaysurface  # Display(640, 580)
    clock = pygame.time.Clock()
    running = True

    Big_Font = pygame.font.SysFont('Roboto', 100)
    Medium_Font = pygame.font.SysFont('Roboto', 70)

    Menu_Text = Medium_Font.render("Main Menu", True, (0, 0, 0), (255, 255, 255))
    Quit_Text = Medium_Font.render("Quit Game", True, (0, 0, 0), (255, 255, 255))
    Score_Text = Medium_Font.render(f"Your Score: {score}", True, (0, 0, 0), (255, 255, 255))


    scores = []
    with open(f"LeaderBoards/Local{Difficulty}.txt", 'r') as file:
        for line in file:
            scores.append(int(line))

    endMsg = ""
    if BotSwitch:
        endMsg = "Game Over"
        with open(f"LeaderBoards/Local{Difficulty}.txt", 'w') as file:
            for i in range(3):
                if score > scores[i]:
                    scores[i] = score
                    break
            
            for number in scores:
                file.write(f"{number}\n")

    Leaderboard_Text = Medium_Font.render(f"TOP {Difficulty} SCORES: First. {scores[0]} Second. {scores[1]} Third {scores[2]}", True, (0, 0, 0), (255, 255, 255))

    if not BotSwitch:
        if score:
            endMsg = "Right Player Wins!"
        else:
            endMsg = "Left Player Wins!"
    WinText = Big_Font.render(f"{endMsg}", True, (0, 0, 0), (255, 255, 255))
    
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                if MenuButton.PressButton(pos):
                    play_sound(button_select_sound)
                    running = False
                if QuitButton.PressButton(pos):
                    play_sound(button_select_sound)
                    sys.exit()
    

        Screen.fill((0, 0, 0))
        pygame.draw.rect(Screen, MenuButton.color, MenuButton.rect)
        pygame.draw.rect(Screen, QuitButton.color, QuitButton.rect)

        Screen.blit(Menu_Text, (MenuButton.pos[0] + TextIndent, MenuButton.pos[1] + 15))
        Screen.blit(Quit_Text, (QuitButton.pos[0] + TextIndent, QuitButton.pos[1] + 5))

        
        if BotSwitch:
            Screen.blit(Leaderboard_Text, ((WIDTH / 2) - 500, (HEIGHT / 10)))
            Screen.blit(Score_Text, ((WIDTH / 2) - 500, (HEIGHT / 10) - 50))

        Screen.blit(WinText, ((WIDTH / 2) - 250, 150 + (HEIGHT / 10)))
        pygame.display.flip()

    
def main():
    global music_on
    left_score = 0
    right_score = 0
    Small_Font = pygame.font.SysFont('Roboto', 60)
    left_scoreboard = Small_Font.render(f'{left_score}', True, (255, 255, 255), (0, 0, 0))
    right_scoreboard = Small_Font.render(f'{right_score}', True, (255, 255, 255), (0, 0, 0))
    game_paused = False

    # Determine CPU range based on difficulty
    if Difficulty == "HARD":
        Range = 170
    elif Difficulty == "MEDIUM":
        Range = 350
    elif Difficulty == "EASY":
        Range = 475

    last_collided = None

    # Create paddles and ball
    l_paddle = Paddle(60, HEIGHT / 2, LEFT)
    if BotSwitch:  # Single-player
        r_paddle = Bot(WIDTH - 60, HEIGHT / 2, RIGHT)
    else:  # Multiplayer
        r_paddle = Paddle(WIDTH - 60, HEIGHT / 2, RIGHT)

    pong_b = Ball(WIDTH / 2, HEIGHT / 2)

    paddlesGroup = pygame.sprite.Group()
    paddlesGroup.add(l_paddle)
    paddlesGroup.add(r_paddle)

    gamePieceGroup = pygame.sprite.Group()
    gamePieceGroup.add(pong_b)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause
                    game_paused = not game_paused
                if event.key == pygame.K_m:  # Mute/Unmute
                    if music_on:
                        stop_background_music()
                    else:
                        play_background_music()
                    music_on = not music_on

        if game_paused:
            font = pygame.font.Font(None, 36)
            text = font.render("Paused", True, (255, 255, 255))
            displaysurface.fill((0, 0, 0))
            displaysurface.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
            pygame.display.flip()
            continue

        # Clear screen
        displaysurface.fill((0, 0, 0))

        # Update and render scoreboards
        displaysurface.blit(left_scoreboard, ((WIDTH / 2) - 120, 30))
        displaysurface.blit(right_scoreboard, ((WIDTH / 2) + 60, 30))

        # Paddle movement
        l_paddle.move()
        if BotSwitch:  # CPU opponent
            r_paddle.BotMove(Range, pong_b)
        else:  # Human opponent
            r_paddle.move()

        # Ball movement
        pong_b.move()

        # Render paddles and ball
        for entity in paddlesGroup:
            displaysurface.blit(entity.surf, entity.rect)
        for entity in gamePieceGroup:
            displaysurface.blit(entity.surf, entity.rect)

        # Paddle Collision Bounce
        collided = pygame.sprite.spritecollide(pong_b, paddlesGroup, False)
        if collided:
            collided = collided[0]  # Only one paddle collision at a time
            if collided != last_collided:
                if pong_b.velocity <= 30:
                    pong_b.velocity += 0.4
                pong_b.bounce(collided)
                last_collided = collided
                play_sound(paddle_hit_sound)

        # Top/Bottom Boundary Bounce
        if pong_b.pos[1] <= 0:
            pong_b.pos[1] = 1
            pong_b.direction[1] = abs(pong_b.direction[1])
            play_sound(wall_hit_sound)

        if pong_b.pos[1] >= HEIGHT:
            pong_b.pos[1] = HEIGHT - 1
            pong_b.direction[1] = -abs(pong_b.direction[1])
            play_sound(wall_hit_sound)

        # Check for scoring
        if pong_b.pos[0] < 0 or pong_b.pos[0] > WIDTH:
            if pong_b.pos[0] < 0:
                right_score += 1
            elif pong_b.pos[0] > WIDTH:
                left_score += 1

            play_sound(score_sound)

            # Check for win condition
            if right_score >= 3:
                EndMenu(left_score)
                break
            elif left_score >= 3 and not BotSwitch:
                EndMenu(0)
                break

            # Reset ball
            last_collided = None
            pong_b.pos = vec(WIDTH / 2, HEIGHT / 2)
            pong_b.velocity = 6
            pong_b.direction = random.choice([[1, 0], [-1, 0]])
            left_scoreboard = Small_Font.render(f'{left_score}', True, (255, 255, 255), (0, 0, 0))
            right_scoreboard = Small_Font.render(f'{right_score}', True, (255, 255, 255), (0, 0, 0))
            time.sleep(1)

        pygame.display.update()
        FramePerSec.tick(FPS)



if __name__ == '__main__':
    pygame.init()
    while replay:
        StartMenu()
        main()
