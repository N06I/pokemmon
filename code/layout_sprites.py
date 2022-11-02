import pygame
from raw import spriteHitboxes


class Prop(pygame.sprite.Sprite):
    def __init__(self, groups, position, image=pygame.Surface((8, 8)), singletile=False):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=position)
        if singletile:
            self.hitbox = pygame.Rect(self.rect.left, self.rect.bottom - 12, 16, 12)
        else:
            self.hitbox = self.rect.copy()


class LongHidden(pygame.sprite.Sprite):
    def __init__(self, groups, position, end):
        super().__init__(groups)
        self.rect = pygame.Rect(position, (end[0]-position[0], end[1]-position[1]))
        self.rect.bottomleft = self.rect.topleft
        self.hitbox = self.rect
        # self.image = pygame.Surface(self.rect.size)
        # self.image.fill("#191919")

