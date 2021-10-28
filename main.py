import pygame

from field import Field


def main():
    """Start point"""
    pygame.display.set_caption('Balls')
    pygame.init()

    Field.WIDTH = 800
    Field.HEIGHT = 500

    Field.BALL_MIN_X_SPEED = Field.BALL_MIN_Y_SPEED = 0
    Field.BALL_MAX_X_SPEED = Field.BALL_MAX_Y_SPEED = 5
    Field.BALL_MIN_RADIUS = 15
    Field.BALL_MAX_RADIUS = 25

    field = Field(n_balls=10)
    field.add_balls()
    window = pygame.display.set_mode((Field.WIDTH, Field.HEIGHT))

    clock = pygame.time.Clock()
    clock.tick(1)
    FPS = 60

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill('black')

        # for ball in field.balls:
        #     pygame.draw.aaline(window, 'white', [ball.x, ball.y], [ball.x + ball.vx * 10000, ball.y + ball.vy * 10000])

        for ball in field.balls:
            pygame.draw.circle(window, ball.color, (round(ball.x), round(ball.y)), ball.radius)
            # pygame.draw.circle(window, 'black', (ball.x, ball.y), ball.radius - 3)

        field.move_all()
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == '__main__':
    main()
