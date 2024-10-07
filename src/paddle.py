import pygame
import pymunk
from src.lib import GameObject, Sprite, World
from src.lib import Frame

SIZE = 10, 50
COLOR = (255, 255, 255)
SPEED = 300

class Paddle(GameObject):
    def __init__(self, position: tuple[int, int], y_cap: tuple[int, int]) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly.create_box(self.body, SIZE)
        self.shape.elasticity = 1
        self.shape.collision_type = id(Paddle)
        x, y = position
        self.body.position = pymunk.Vec2d(x, y)
        self.y_cap = y_cap

        self.sprite = Sprite()
        self.sprite.src_image = pygame.Surface(SIZE, flags=pygame.SRCALPHA)
        self.sprite.src_image.fill(COLOR)
        self.sprite.body = self.body

    def on_create(self, world: World) -> None:
        world.sprites.add(self.sprite)
        world.space.add(self.body, self.shape)

    def on_update(self, world: World, frame: Frame) -> None:
        x, y = self.body.position
        y = max(self.y_cap[0], min(y, self.y_cap[1]))
        self.body.position = pymunk.Vec2d(x, y)

class PlayerPaddle(Paddle):
    def on_update(self, world: World, frame: Frame) -> None:
        keystate = pygame.key.get_pressed()
        v_vector = pymunk.Vec2d(0, SPEED * frame.dt)
        if keystate[pygame.K_w]: self.body.position -= v_vector
        if keystate[pygame.K_s]: self.body.position += v_vector
        return super().on_update(world, frame)


        