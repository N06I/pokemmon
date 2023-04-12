import pygame
from proto_hitbox import Hitbox
from proto_animation import Animator


class GeneralistSprite(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, size, hitbox: Hitbox = None, image=None):
        super().__init__(groups)
        self.rect = pygame.Rect((bottomleft[0] - size[0], bottomleft[1]), size)
        if hitbox:
            self.hitbox = hitbox
        if image:
            self.image = image


class Ledge(GeneralistSprite):
    def __init__(self, groups, bottomleft, size, hitbox, direction):
        super().__init__(groups, bottomleft, size, hitbox)
        self.direction = direction


class AnimatedSprite(GeneralistSprite):
    def __init__(self, groups, bottomleft, size, animations, state="idle",
                 hitbox: Hitbox = None,
                 animator: Animator = None):
        super().__init__(groups, bottomleft, size, hitbox=hitbox)
        self.state = state

        if animator:
            self.animator = animator
        else:
            self.animator = Animator(animations, self.state)

    def update(self):
        self.animator.update()


class Door(AnimatedSprite):
    def __init__(self, groups, bottomleft, size, animations, state, hitbox):
        super().__init__(groups, bottomleft, size, animations, state, hitbox)
        self.state = state

    def interact(self):
        if self.state == "closed":
            self.state = "open"
        else:
            self.state = "closed"


class Water(AnimatedSprite):
    def __init__(self, groups, bottomleft, size, animations, hitbox):
        super().__init__(groups, bottomleft, size, animations, hitbox=hitbox)

    def draw(self, frame):
        self.


class WaterGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def draw_group(self):
        for water_sprite in self.sprites():
            pass

    def update(self, *args, **kwargs) -> None:
        for water_sprite in self.sprites():
            water_sprite.update(*args, *kwargs)
            self.draw_sprite()
