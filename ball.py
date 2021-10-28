import math
from random import randint


class Ball:
    """Mathematical and physical model of motion and absolutely
    elastic collision of balls in two-dimensional space.

    Attributes
    ----------
    x : float
        The x-coordinate of the center of the ball
    y : float
        The x-coordinate of the center of the ball
    vx : float
        x-speed or value of the change in the x-coordinate per unit of time
    vy : float
        y-speed or value of the change in the y-coordinate per unit of time
    ax : float
        x-acceleration or coefficient of change of vx per unit of time.
    ay : float
        y-acceleration or coefficient of change of vy per unit of time.
    radius : float
        Ball radius value, strictly positive
    mass : float
        The mass of the ball, strictly positive (needed to recalculate the velocities of the balls upon collision)
    """

    def __init__(self,
                 x: float, y: float,
                 vx: float, vy: float,
                 ax: float = 1.0, ay: float = 1.0,
                 radius: float = 1.0):
        """Initializes all needed parameters"""
        self.x, self.vx, self.ax = x, vx, ax
        self.y, self.vy, self.ay = y, vy, ay
        self.radius = radius
        self.mass = 10.0 * radius

    def move(self, time=1.0):
        """Recalculates changes in the coordinates of the center and velocities
        along the axes for a given amount of time

        Parameters
        ----------
        time : float
            Amount of time
        """
        self.x += self.vx * time
        self.y += self.vy * time
        self.vx *= self.ax
        self.vy *= self.ay

    def move_back(self, time=1.0):
        """...

        Parameters
        ----------
        time : float
            Amount of time
        """
        self.vx /= self.ax
        self.vy /= self.ay
        self.x -= self.vx * time
        self.y -= self.vy * time

    def bounce_off(self, max_x, max_y, min_x=0.0, min_y=0.0):
        """This method pushes the ball away from the wall
        if the distance from the center to it is less than the radius

        Parameters
        ----------
        max_x : float
            Maximum x-coordinate
        max_y : float
            Maximum y-coordinate
        min_x : float
            Minimum x-coordinate
        min_y : float
            Minimum y-coordinate
        """
        if (self.x - self.radius) <= min_x:
            self.vx = -self.vx
            self.x = min_x + self.radius
        if (self.x + self.radius) >= max_x:
            self.vx = -self.vx
            self.x = max_x - self.radius
        if (self.y - self.radius) <= min_y:
            self.vy = -self.vy
            self.y = min_y + self.radius
        if (self.y + self.radius) >= max_y:
            self.vy = -self.vy
            self.y = max_y - self.radius

    @staticmethod
    def is_overlaps(first, second):
        """Checks if two balls overlap (collide)

        Parameters
        ----------
        first : Ball
            First ball instance
        second : Ball
            Second ball instance

        Returns
        -------
        bool
            True if the distance between the balls is less than the sum of the radii of the balls,
            False otherwise
        """
        return Ball.distance(first, second) + 1e-3 < first.radius + second.radius

    @staticmethod
    def collision(first: 'Ball', second: 'Ball'):
        # Distance between balls
        distance = Ball.distance(first, second)

        # Normal
        nx = (second.x - first.x) / distance
        ny = (second.y - first.y) / distance

        # Tangent
        tx = -ny
        ty = nx

        # Dot Product Normal
        dp_norm1 = first.vx * nx + first.vy * ny
        dp_norm2 = second.vx * nx + second.vy * ny

        # Conservation of momentum in 1D
        m1 = (dp_norm1 * (first.mass - second.mass) + 2 * second.mass * dp_norm2) / (first.mass + second.mass)
        m2 = (dp_norm2 * (second.mass - first.mass) + 2 * first.mass * dp_norm1) / (first.mass + second.mass)

        # Dot Product Tangent
        first_dp_tan = first.vx * tx + first.vy * ty
        second_dp_tan = second.vx * tx + second.vy * ty

        # Update ball velocities
        first.vx = tx * first_dp_tan + nx * m1
        first.vy = ty * first_dp_tan + ny * m1
        second.vx = tx * second_dp_tan + nx * m2
        second.vy = ty * second_dp_tan + ny * m2

        overlap = first.radius + second.radius + 1e-3 - distance
        if randint(0, 1) & 1:
            first.x -= overlap * nx
            first.y -= overlap * ny
        else:
            second.x += overlap * nx
            second.y += overlap * ny

        print(f"COLLISSION: R1 - {first.radius:>5.2f}, "
              f"R2 - {second.radius:>5.2f}, "
              f"overlap - {overlap / (first.radius + second.radius) * 100:>5.2f}%")

    @staticmethod
    def distance(first, second):
        return math.hypot(first.x - second.x, first.y - second.y)

