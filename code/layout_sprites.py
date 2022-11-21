import pygame


class Prop(pygame.sprite.Sprite):
    def __init__(self, groups, position, image=pygame.Surface((8, 8)), singletile=False, hb_size_fraction=0.5):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(bottomleft=position)
        if singletile:
            self.hitbox = pygame.Rect(self.rect.left+1, self.rect.bottom - 12, 14, 12)
        else:
            hb_height = self.rect.height * hb_size_fraction
            self.hitbox = pygame.Rect(self.rect.left, self.rect.top + self.rect.height - hb_height,
                                      self.rect.width, hb_height)
