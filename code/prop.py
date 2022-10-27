import pygame
from raw import spriteHitboxes


class Prop(pygame.sprite.Sprite):
    def __init__(self, groups, position, image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
