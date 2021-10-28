from random import randint, uniform, normalvariate
from itertools import combinations

from ball import Ball


class Field:
    WIDTH, HEIGHT = 400, 400
    BALL_MIN_X_SPEED = BALL_MIN_Y_SPEED = 0
    BALL_MAX_X_SPEED = BALL_MAX_Y_SPEED = 7
    BALL_MIN_RADIUS, BALL_MAX_RADIUS = 10, 10
    BALL_X_ACCELERATION = BALL_Y_ACCELERATION = 1 - 1e-6

    def __init__(self, n_balls: int) -> None:
        self.n_balls = n_balls
        self.balls = list()

    @staticmethod
    def get_random_x_speed():
        turn = (-1) ** randint(0, 1)
        return turn * uniform(Field.BALL_MIN_X_SPEED, Field.BALL_MAX_X_SPEED)

    @staticmethod
    def get_random_y_speed():
        turn = (-1) ** randint(0, 1)
        return turn * uniform(Field.BALL_MIN_Y_SPEED, Field.BALL_MAX_Y_SPEED)

    @property
    def random_ball(self) -> Ball:
        radius = uniform(Field.BALL_MIN_RADIUS, Field.BALL_MAX_RADIUS)
        return Ball(
            x=uniform(1 + radius, Field.WIDTH - radius - 1),
            y=uniform(1 + radius, Field.HEIGHT - radius - 1),
            vx=Field.get_random_x_speed(),
            vy=Field.get_random_y_speed(),
            ax=Field.BALL_X_ACCELERATION,
            ay=Field.BALL_Y_ACCELERATION,
            radius=radius
        )

    def add_balls(self):
        """Adds n_balls random balls to the field, so that none of them overlap with the other"""
        for _ in range(self.n_balls):
            new_ball = self.random_ball

            while any(Ball.is_overlaps(new_ball, other_ball) for other_ball in self.balls):
                new_ball = self.random_ball

            new_ball.color = (randint(0, 255),
                              randint(0, 255),
                              randint(0, 255))
            self.balls.append(new_ball)

    def move_all(self, time=1.0, handle_collisions=True):
        """
        """
        collised = set()

        if handle_collisions:
            for (i, first), (j, second) in combinations(enumerate(self.balls), r=2):
                if Ball.is_overlaps(first, second):
                    collised.update((i, j))
                    Ball.collision(first, second)

        for i, ball in enumerate(self.balls):
            if i not in collised:
                ball.move(time=time)
                ball.bounce_off(max_x=self.WIDTH, max_y=self.HEIGHT)
