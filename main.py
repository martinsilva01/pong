import sys
import pygame


class Display:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((width, height))

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


class Paddle():
    def __init__(self, x, y):
        self.color = (255, 255, 255)
        self.rect = pygame.Rect((x, y), (15, 75))

class Ball():
    def __init__(self, x, y):
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.radius = 8 



def main():
    pygame.init()
    d = Display(640, 480)
    clock = pygame.time.Clock()
    running = True

    l_paddle = Paddle(60, 200)
    ball = Ball(320, 240)



    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
                sys.exit()

        d.surface.fill((0, 0, 0))
        pygame.draw.rect(d.surface, l_paddle.color, l_paddle.rect)
        pygame.draw.circle(d.surface, ball.color, (ball.x, ball.y), ball.radius)
        pygame.display.flip()


if __name__ == '__main__':
    main()
