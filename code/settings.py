import pygame


class Settings:
    def __init__(self, get_events):
        self.get_events = get_events
        self.event_loop = get_events()
        # setting classes
        self.camera = self.CameraSettings()
        self.sound = self.SoundSettings()

    def update(self):
        self.event_loop = self.get_events()
        if pygame.K_F3 in self.event_loop:
            if pygame.K_h in self.event_loop:
                self.camera.show_hitboxes.toggle()
            if pygame.K_b in self.event_loop:
                self.camera.show_bounding.toggle()

    class CameraSettings:
        def __init__(self):
            self.show_hitboxes = Setting(False)
            self.show_bounding = Setting(False)

    class SoundSettings:
        def __init__(self):
            self.volume = Setting(50)


class Setting:
    def __init__(self, value):
        self.val = value

    def toggle(self):
        if type(self.val) is bool:
            self.val = not self.val
        else:
            print("Setting isn't toggleable")
