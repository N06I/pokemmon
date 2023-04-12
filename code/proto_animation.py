import math
import pygame


class Animator:
    """Animation engine, used by sprites to return the current animation's current frame using the get_frame() method.
    The same Animator object should be used for sprites that are to be simultaneously animated.

    Assets dict is shared between all animators for the same sprite type
    """
    # can use a shared dict to save the latest loaded frames to avoid repeat animation cutting during
    # peak concurrent player times. Unnecessary here, obviously
    def __init__(self, assets: dict, state: str, anim_speed: int = 7):
        self.assets = assets  # entity's state as key, returns [anim_strip: pygame.Surface, length: int, size: tuple]
        self.anim_speed = anim_speed

        self.set_animation(state)

    def set_animation(self, state):
        # setting animation start values
        self.frames = []
        self.index = 0
        self.anim_strip = self.assets[state][0]
        self.length = self.assets[state][1]
        self.size = self.assets[state][2]
        self.state = state

    def get_frame(self, state, action_speed, dt):

        # increment animation index
        if "static" not in self.state:
            if "idle" in self.state:
                self.index += self.anim_speed * dt
            else:
                self.index += self.anim_speed * dt * action_speed.value

        # reset animation when it ends
        if self.index >= self.length:
            self.index = 0

        # check if animation must change, if so, set the new one
        if state != self.state:
            self.set_animation(state)

        # check if the frames list is long enough to have the current frame stored. If it's not, cut it and append
        if len(self.frames) <= math.floor(self.index):
            img = pygame.Surface(self.size, pygame.SRCALPHA)
            img.blit(self.anim_strip, (0, 0), (math.trunc(self.index) * self.size[0], 0, self.size[0], self.size[1]))
            self.frames.append(img)
        # print(f"[loaded_frames]{self.frames}")
        return self.frames[math.floor(self.index)]
