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
    def __init__(self, start_x, start_y):
        self.color = (255, 255, 255)
        self.rect = pygame.Rect((start_x, start_y), (25, 250))



def main():
    pygame.init()
    d = Display(1920, 1080)
    clock = pygame.time.Clock()
    running = True

    l_paddle = Paddle(100, 500)


    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
                sys.exit()

        d.surface.fill((0, 0, 0))
        pygame.draw.rect(d.surface, l_paddle.color, l_paddle.rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
