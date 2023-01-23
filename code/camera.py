import pygame


class Camera(pygame.sprite.LayeredUpdates):
    def __init__(self, character, background, base_display, get_events):
        super().__init__()
        self.settings = {"hitbox": False, "bounding_box": False}
        self.get_events = get_events

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
        for layer in self.layers():
            for sprite in sorted(self.get_sprites_from_layer(layer), key=lambda x: (x.rect.top + x.hitbox_center)):
                screen_pos = (sprite.rect.left + displacement[0], sprite.rect.top + displacement[1])
                self.screen.blit(sprite.image, screen_pos)

                # draw rect and hitbox for testing
                if self.settings["bounding_box"]:
                    onscreen_rect = sprite.rect.move(displacement)
                    pygame.draw.rect(self.screen, (128, 54, 76), onscreen_rect, 1)
                if self.settings["hitbox"]:
                    self.screen.blit(sprite.hitbox_surf, screen_pos)

    def toggle_setting(self, setting):
        self.settings[setting] = not self.settings[setting]

    def update(self, *args, **kwargs) -> None:
        for sprite in self.sprites():
            sprite.update(*args, **kwargs)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_F3]:
            for event in self.get_events():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        self.toggle_setting("hitbox")
                    if event.key == pygame.K_b:
                        self.toggle_setting("bounding_box")
