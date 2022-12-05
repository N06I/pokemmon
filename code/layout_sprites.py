import pygame


class GameObj(pygame.sprite.Sprite):
    def __init__(self, groups, bottomleft, img, size, **kwargs):
        super().__init__(groups)
        self.image = img
        self.rect = pygame.rect.Rect(bottomleft[0], bottomleft[1] - size[1], size[0], size[1])
        self.hitbox = self.rect.copy()

        for arg, val in kwargs.items():
            if arg == "ltrim":
                if val >= 1:
                    trim = val
                else:
                    trim = val*self.hitbox.w
                self.hitbox = pygame.Rect(self.hitbox.left + trim, self.hitbox.top, self.hitbox.w - trim, self.hitbox.h)
            if arg == "rtrim":
                if val >= 1:
                    trim = val
                else:
                    trim = val * self.hitbox.w
                self.hitbox = pygame.Rect(self.hitbox.left, self.hitbox.top, self.hitbox.w - trim, self.hitbox.h)
            if arg == "ttrim":
                if val >= 1:
                    trim = val
                else:
                    trim = val * self.hitbox.h
                self.hitbox = pygame.Rect(self.hitbox.left, self.hitbox.top + trim, self.hitbox.w, self.hitbox.h - trim)
            if arg == "btrim":
                if val >= 1:
                    trim = val
                else:
                    trim = val * self.hitbox.h
                self.hitbox = pygame.Rect(self.hitbox.left, self.hitbox.top, self.hitbox.w, self.hitbox.h - trim)
