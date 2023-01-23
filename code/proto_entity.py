import pygame
from proto_sprites import AnimatedSprite


class Entity(AnimatedSprite):
    def __init__(self, groups, bottomleft, size):
        animations = None
        super().__init__(groups, bottomleft, size, animations, initial_state="down_idle", hitbox_obj=hitbox_obj)
        self.position = pygame.Vector2(self.rect.midbottom)
