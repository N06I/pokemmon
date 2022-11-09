import pygame


class Prop(pygame.sprite.Sprite):
    def __init__(self, groups, position, image=pygame.Surface((8, 8)), singletile=False, full=False):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=position)
        if singletile:
            self.hitbox = pygame.Rect(self.rect.left+1, self.rect.bottom - 12, 14, 12)
        else:
            if full:
                self.hitbox = self.rect.copy()
            else:
                half = self.rect.height/2
                self.hitbox = pygame.Rect(self.rect.left, self.rect.top + half, self.rect.width, half)
