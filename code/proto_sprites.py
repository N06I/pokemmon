import pygame
from proto_hitbox import Hitbox


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
    def __init__(self, groups, bottomleft, size, animations, state="idle", hitbox: Hitbox = None):
        super().__init__(groups, bottomleft, size, hitbox=hitbox)
        self.animations = animations
        self.state = state

    def update(self):
        self.animations[self.state].update()


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
