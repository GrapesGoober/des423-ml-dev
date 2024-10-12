import random
import pygame
import pymunk
from src.lib import GameObject, Sprite, World
from src.paddle import Paddle
from src.wall import ResetWall

RADIUS = 5
COLOR = (255, 255, 255)
SPEED = 600
ANGLE_RANGE = 45
MASS = 1

class Ball(GameObject):
    def __init__(self, position: tuple[int, int], random_y: int) -> None:
        self.body = pymunk.Body()
        self.shape = pymunk.Circle(self.body, RADIUS)
        self.shape.elasticity = 1
        self.shape.collision_type = id(Ball)
        self.shape.density = MASS / self.shape.area
        self.init_position = position
        self.random_y = random_y

        self.sprite = Sprite()
        self.sprite.src_image = pygame.Surface((RADIUS*2, RADIUS*2), flags=pygame.SRCALPHA)
        pygame.draw.circle(self.sprite.src_image, COLOR, (RADIUS, RADIUS), RADIUS)
        self.sprite.body = self.body
        self.reset()

    def on_create(self, world: World) -> None:
        world.sprites.add(self.sprite)
        world.space.add(self.body, self.shape)
        handler = world.space.add_wildcard_collision_handler(id(Ball))
        handler.post_solve = self.on_collide

    def on_collide(self, arb: pymunk.Arbiter, space, _):
        _, other = arb.shapes
        if other.collision_type == id(Paddle):
            self.reset()
        if other.collision_type == id(ResetWall):
            self.reset()
        return True
        
    def reset(self) -> None:
        x, y = self.init_position
        y += random.randrange( -self.random_y, self.random_y)
        self.body.position = pymunk.Vec2d(x, y)
        angle = random.randrange(-ANGLE_RANGE, ANGLE_RANGE)
        self.body.velocity = pymunk.Vec2d(SPEED, 0).rotated_degrees(angle)


