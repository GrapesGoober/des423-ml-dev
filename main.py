import pygame
from src.lib import World

WIDTH, HEIGHT = 640, 360
FPS = 60

if __name__ == "__main__":

    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    screen: pygame.surface.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PONG")

    world = World()
    with open("pong.json") as f: world.load_from_file(f)

    while True:
        # handle event
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: pygame.quit(), exit()
        dt = clock.tick(FPS)/1000
        world.update(events, dt)
        screen.fill((0, 0, 0))
        world.draw(screen)
        pygame.display.update()



