import pygame.sprite


class YSortCam(pygame.sprite.Group):
    def __init__(self, character, background, base_display):
        super().__init__()
        self.screen = base_display
        self.screen_size = self.screen.get_size()
        self.background = background
        self.bg_rect = self.background.get_rect(center=self.screen_size)
        self.character = character

    def custom_draw(self):
        self.screen.blit(self.background, self.bg_rect)
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            self.screen.blit(sprite.image, sprite.rect)


class YSortCenterCam(YSortCam):
    def __init__(self, character, background, base_display):
        super().__init__(character, background, base_display)

    def custom_draw(self):
        displacement = (self.screen_size[0]/2 - self.character.rect.centerx, self.screen_size[1]/2 - self.character.rect.centery)
        self.screen.blit(self.background, displacement)
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            screen_pos = (sprite.rect.left + displacement[0], sprite.rect.top + displacement[1])
            self.screen.blit(sprite.image, screen_pos)


class Camera(pygame.sprite.Group):
    def __init__(self, character, background, base_display):
        super().__init__()
        self.screen = base_display
        self.screen_size = self.screen.get_size()
        self.width_half = self.screen_size[0] / 2
        self.height_half = self.screen_size[1] / 2
        self.background = background
        self.bg_w = background.get_width()
        self.bg_h = background.get_height()
        self.bg_rect = self.background.get_rect(center=self.screen_size)
        self.character = character

        self.displacement_x = self.width_half - self.character.rect.centerx
        self.displacement_y = self.height_half - self.character.rect.centery

    def custom_draw(self):
        if (self.bg_w - self.width_half) >= self.character.rect.centerx >= self.width_half:
            self.displacement_x = self.width_half - self.character.rect.centerx
        if (self.bg_h - self.height_half) >= self.character.rect.centery >= self.height_half:
            self.displacement_y = self.height_half - self.character.rect.centery

        displacement = (self.displacement_x, self.displacement_y)
        self.screen.blit(self.background, displacement)
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            screen_pos = (sprite.rect.left + displacement[0], sprite.rect.top + displacement[1])
            self.screen.blit(sprite.image, screen_pos)
