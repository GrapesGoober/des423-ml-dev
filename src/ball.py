import random
import pygame
import pymunk
from src.lib import GameObject, Sprite, World
from src.lib import Frame

RADIUS = 5
COLOR = (255, 255, 255)
SPEED = 300
ANGLE_RANGE = 45
MASS = 1

class Ball(GameObject):
    def __init__(self, position: tuple[int, int]) -> None:
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, RADIUS)
        self.shape.elasticity = 1
        self.shape.density = MASS / self.shape.area
        self.init_position = position

        self.sprite = Sprite()
        self.sprite.src_image = pygame.Surface((RADIUS*2, RADIUS*2), flags=pygame.SRCALPHA)
        pygame.draw.circle(self.sprite.src_image, COLOR, (RADIUS, RADIUS), RADIUS)
        self.sprite.body = self.body
        self.reset()

    def on_create(self, world: World) -> None:
        world.sprites.add(self.sprite)
        world.space.add(self.body, self.shape)

    def reset(self) -> None:
        x, y = self.init_position
        self.body.position = pymunk.Vec2d(x, y)
        angle = random.randrange(-ANGLE_RANGE, ANGLE_RANGE)
        self.body.velocity = pymunk.Vec2d(-SPEED, 0).rotated_degrees(angle)

