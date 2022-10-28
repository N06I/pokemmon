import pygame
from raw import spriteHitboxes


class Prop(pygame.sprite.Sprite):
    def __init__(self, groups, position, image=None):
        super().__init__(groups)
        self.image = image
        if self.image is not None: self.rect = self.image.get_rect(topleft=position)


class LongProp(Prop):
    def __init__(self, groups, position, end):
        super().__init__(groups, position)
        self.rect = pygame.Rect(position, (end[0]-position[0], end[1]-position[1]))
