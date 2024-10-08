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

    def get_x(self):
        return self.rect.x

    def get_y(self):
        return self.rect.y

    def move(self, px):
        self.rect = self.rect.move(0, px)
        return

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

    r_paddle = Paddle(580, 200)

    ball = Ball(320, 240)



    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.quit:
                running = False
                sys.exit()

        keys = pygame.key.get_pressed()
        curr_l_y = l_paddle.get_y()

        curr_r_y = r_paddle.get_y()


        if keys[pygame.K_w] and not keys[pygame.K_s]:
            if curr_l_y > 0:
                l_paddle.move(-10) 
            
        if keys[pygame.K_s] and not keys[pygame.K_w]:
            if curr_l_y < (d.get_height()-75):
                l_paddle.move(10) 

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if curr_r_y > 0:
                r_paddle.move(-10) 
            
        if keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            if curr_r_y < (d.get_height()-75):
                r_paddle.move(10) 
         
            
        d.surface.fill((0, 0, 0))
        pygame.draw.rect(d.surface, l_paddle.color, l_paddle.rect)
        pygame.draw.rect(d.surface, l_paddle.color, r_paddle.rect)
        pygame.draw.circle(d.surface, ball.color, (ball.x, ball.y), ball.radius)
        pygame.display.flip()


if __name__ == '__main__':
    main()
