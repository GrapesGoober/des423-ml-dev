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




class AiPaddle(Paddle):
    def __init__(self, position: tuple[int, int], y_cap: tuple[int, int], ball_key: str) -> None:
        from pickle import load
        from src.ball import Ball

        super().__init__(position, y_cap)
        
        self.ball_key = ball_key
        self.ball: Ball = None
        self.paddle: Paddle = None
        with open("src\\model.pkl", "rb") as f:
            self.model = load(f)
        
    def on_create(self, world: World) -> None:
        super().on_create(world)
        self.ball = world.global_states[self.ball_key]
    
    def on_update(self, world: World, frame: Frame) -> None:
        
        ball_x, ball_y = self.ball.body.position
        ball_vx, ball_vy = self.ball.body.velocity
        _, paddle_y = self.body.position

        prediction = self.model.predict([[ball_x, ball_y, ball_vx, ball_vy, paddle_y]])
        v_vector = pymunk.Vec2d(0, SPEED * frame.dt)
        if prediction == 'up':      self.body.position -= v_vector
        elif prediction == 'down':  self.body.position += v_vector
        
        super().on_update(world, frame)

        
        