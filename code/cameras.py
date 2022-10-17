import pygame.sprite


class YSortCam(pygame.sprite.Group):
    def __init__(self, character, background, base_display):
        super().__init__()
        self.screen = base_display
        self.screen_center = (self.screen.get_size()[0]/2, self.screen.get_size()[1]/2)
        self.background = background
        self.bg_rect = self.background.get_rect(center=self.screen_center)
        self.character = character

    def custom_draw(self):
        self.screen.blit(self.background, self.bg_rect)
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            self.screen.blit(sprite.image, sprite.rect)


class YSortCenterCam(YSortCam):
    def __init__(self, character, background, base_display):
        super().__init__(character, background, base_display)

    def custom_draw(self):
        displacement = (self.screen_center[0] - self.character.rect.centerx, self.screen_center[1] - self.character.rect.centery)
        self.screen.blit(self.background, displacement)
        for sprite in sorted(self.sprites(), key=lambda x: x.rect.bottom):
            offset = (sprite.rect.left + displacement[0], sprite.rect.top + displacement[1])
            self.screen.blit(sprite.image, offset)

    # def draw(self, follow):
    #     pos = (self.screen_center[0] - self.character.rect.centerx, self.screen_center[1] - self.character.rect.centery)
    #     self.base_display.blit(self.floor, pos if self.area_offset == (0, 0) else self.area_offset)
    #     if follow:
    #         for sprite in sorted(self.sprites(), key=lambda sprite: sprite.hitbox.centery):
    #             self.follow_blyat(sprite)
    #     else:
    #         for sprite in sorted(self.sprites(), key=lambda sprite: sprite.hitbox.centery):
    #             self.blyat(sprite)
    #     self.base_display.blit(self.roof, pos if self.area_offset == (0, 0) else self.area_offset)

