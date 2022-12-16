import pygame


class GameObj(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, img, hitbox, hb_surf, hb_center, size):
        super().__init__(groups)
        self.image = img
        self.rect = pygame.rect.Rect(bottomleft[0], bottomleft[1] - size[1], size[0], size[1])
        self.hitbox = hitbox
        self.hitbox_surf = hb_surf
        self.hitbox_center = hb_center
