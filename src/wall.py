import pygame
import pymunk
from src.lib import GameObject, Sprite, World

class Wall(GameObject):
    def __init__(self, size: tuple[int, int], position: tuple[int, int]) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Poly.create_box(self.body, size)
        self.shape.elasticity = 1
        x, y = position
        self.body.position = pymunk.Vec2d(x, y)

    def on_create(self, world: World) -> None:
        world.space.add(self.body, self.shape)