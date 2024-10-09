import pygame, csv
from src.ball import Ball
from src.lib import Frame
from src.paddle import Paddle
from src.lib import GameObject, World

INTERVAL = 0.5

class DataCollector(GameObject):
    def __init__(self, filename: str, ball_key: str, paddle_key: str) -> None:
        self.counter = 0
        self.ball_key = ball_key
        self.paddle_key = paddle_key
        self.ball: Ball = None
        self.paddle: Paddle = None

        self.file = open(filename, 'a', newline='')
        self.writer = csv.writer(self.file)

    def __del__(self):
        self.file.close()

    def on_create(self, world: World) -> None:
        self.ball = world.global_states[self.ball_key]
        self.paddle = world.global_states[self.paddle_key]

    def on_update(self, world: World, frame: Frame) -> None:
        self.counter += frame.dt
        if self.counter > INTERVAL:
            self.counter = 0
            ball_x, ball_y = self.ball.body.position
            ball_vx, ball_vy = self.ball.body.velocity
            _, paddle_y = self.paddle.body.position

            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_w]:    movement = "up"
            elif keystate[pygame.K_s]:  movement = "down"
            else:                       movement = "no"

            self.writer.writerow(
                [int(ball_x), int(ball_y), 
                    int(ball_vx), int(ball_vy), 
                    int(paddle_y), movement])
