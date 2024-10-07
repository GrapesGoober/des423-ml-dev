from dataclasses import dataclass
from typing import Any
import pygame, pymunk, json, importlib

@dataclass
class Frame:
    """
    A dataclass encapsulating any data available for each frame.

    Attributes:
        `events`    Pygame events since last frame.
        `dt`        Delta time; time elapsed since last frame.
    """
    events:     pygame.event.Event
    dt:         float

class Sprite(pygame.sprite.Sprite):
    """ 
    Sprite class holds images, position, and angle. 
    Adding this to world will automatically take its image, position, angle,
    and camera position to draw it to screen surface. If the `body` attribute is set,
    it will overwrite `x`, `y`, and `angle` based on body's `position` and `angle`.

    Attributes:
        `src_image` The source image to render.
        `x`, `y`    Sprite position at center of image.
        `angle`     Sprite angle at center of image (degrees).
        `body`      Pymunk's rigidbody for the sprite to draw to. Default to `None`.
    """
    def __init__(self, body: pymunk.Body = None) -> None:
        super().__init__()
        self.src_image = pygame.Surface((0,0)) 
        self.angle = 0
        self.x, self.y = 0, 0
        self._camera_pos = 0, 0
        self.body = body

    @property
    def position(self) -> pygame.Vector2: return pygame.Vector2(self.x, self.y)

    @position.setter
    def position(self, val: pygame.Vector2): self.x, self.y = val

    @property
    def image(self) -> pygame.Surface:
        """ (Read only property) Rotated image for pygame's sprite to draw. """
        if self.body: self.angle = self.body.angle * -57.2958
        return pygame.transform.rotate(self.src_image, self.angle)
    
    @property
    def rect(self) -> pygame.Rect:
        """ (Read only property) Computed rect for pygame's sprite to draw. """
        if self.body: self.x, self.y = self.body.position
        screen_coord_x = int(self.x - self._camera_pos[0])
        screen_coord_y = int(self.y - self._camera_pos[1])
        return self.image.get_rect(center=(screen_coord_x, screen_coord_y))

class GameObject:
    """
    Base class to implement custom game logic, sprites, and physics. 

    Methods:
        `__init__`      Constructor to initialize object. Metadata is provided as kwargs.
        `on_create`     Called once to add sprites, physics, or gameobjects to game world.
        `on_remove`     Called once to remove sprites, physics, or gameobjects from game world.
        `on_update`     Called every frame. Put your custom logic here.

    Note: 
    - Upon `on_create`, you must add all your sprites, bodies, shapes, or other gameobjects
    to `world`, otherwise they won't be rendered.
    - `on_remove` is optional. You should remove all objects added to world in `on_create`.
    """

    def __init__(self, **metadata: Any) -> None: ...
    def on_create(self, world: 'World') -> None: ...
    def on_remove(self, world: 'World') -> None: ...
    def on_update(self, world: 'World', frame: Frame) -> None: ...

class World:
    """
    World class contains all the GameObjects to be rendered.  

    Attributes:
        `global_states`     Dictionary containing world-level data, such as game states.
        `camera_position`   X and Y coordinates of camera. Can be moved around dynamically.
        `gameobjects`       list GameObjects added to world. 
        `sprites`           pygame's Group of sprites to be rendered.
        `space`             pymunk's physics space to be simulated.
        `background`        Surface background image. Is optional.

    Methods:
        `load_from_file`    Load a new world from file
        `add`               Add GameObject to world. Will call `GameObject.on_create`.
        `remove`            Remove GameObject to world. Will call `GameObject.on_remove`.
        `start`             Start the world. Will call `GameObject.on_start`.
        `update`            Update the world by 1 frame. Will call `GameObject.on_update`.
        `draw`              Draw the world to the screen.
    """
    def __init__(self) -> None:
        self.global_states: dict[str|Any] = {}
        self.camera_position = [0, 0]
        self.gameobjects: list[GameObject] = []
        self.sprites = pygame.sprite.Group()
        self.space = pymunk.Space()
        self.background: pygame.Surface = None

    def load_from_file(self, world_file) -> None:
        world_data = json.load(world_file)

        objects_to_add: list[GameObject] = []
        for item in world_data:
            key = item['key']
            metadata = item['metadata']
            module_name, class_name = item['location'].rsplit('.', 1)

            module = importlib.import_module(module_name)
            gameobj = getattr(module, class_name)(**metadata)
            if key: self.global_states[key] = gameobj
            if isinstance(gameobj, GameObject): 
                objects_to_add.append(gameobj)
        self.gameobjects += objects_to_add
        for gameobj in objects_to_add: gameobj.on_create(self)

    def add(self, gameobj: GameObject) -> None:
        self.gameobjects.append(gameobj)
        gameobj.on_create(self)

    def remove(self, gameobj: GameObject) -> None:
        if gameobj in self.gameobjects:
            self.gameobjects.remove(gameobj)
            gameobj.on_remove(self)

    def update(self, events: list[pygame.event.Event], dt: float) -> None:
        for gameobj in self.gameobjects: 
            gameobj.on_update(self, Frame(events, dt))
        for s in self.sprites: 
            if isinstance(s, Sprite):
                s._camera_pos = self.camera_position
        # TODO: add fixed-time physics update
        for i in range(10): self.space.step(dt/10)

    def draw(self, surface: pygame.Surface) -> None:
        self.sprites.draw(surface, self.background)