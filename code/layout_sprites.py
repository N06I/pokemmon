import pygame
from file_management import get_hitbox_center


class GameObj(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, img, hitbox, hb_surf, hb_center, size):
        super().__init__(groups)
        self.image = img
        self.rect = pygame.rect.Rect(bottomleft[0], bottomleft[1] - size[1], size[0], size[1])
        self.hitbox = hitbox
        self.hitbox_surf = hb_surf
        self.hitbox_center = hb_center


class CustomTile(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, img=None, hitbox=None, hb_surf=None, hb_center=None, size=(16, 16), friction=0):
        super().__init__(groups)
        self.image = img if img is not None else pygame.Surface(size)
        self.rect = pygame.rect.Rect(bottomleft[0], bottomleft[1] - size[1], size[0], size[1])
        self.hitbox = hitbox if hitbox is not None else pygame.mask.Mask(size, True)
        self.hitbox_surf = hb_surf if hb_surf is not None else self.hitbox.to_surface()
        self.hitbox_surf.set_colorkey(0)
        self.hitbox_center = get_hitbox_center(self.hitbox)
        self.coef = friction


class Ledge(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, hitbox, hb_surf, size, directions):
        super().__init__(groups)
        self.rect = pygame.Rect(bottomleft[0], bottomleft[1] - size[1], size[0], size[1])
        self.hitbox = hitbox
        self.hitbox_surf = hb_surf
        self.hitbox_surf.set_colorkey(0)
        self.directions = directions
