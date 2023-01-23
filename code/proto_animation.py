import math
import pygame

from raw import animData


class Animation:
    """Animation class, updated each tick and mainly used for the "get_frame" method"""

    def __init__(self, animData: dict, state: str, anim_speed: int = 7):
        self.animData = animData  # dictionary with the animation strip image corresponding to each sprite state
        self.anim_speed = anim_speed

        self.state = state  # the animator's corresponding sprite's state
        self.frames = []

        self.index = 0
        self.set_animation(self.state)

    def save_previous_anim(self):
        self.previous_state = self.state
        self.previous_frames = self.frames

    def set_animation(self, state):
        self.save_previous_anim()

        self.index = 0
        self.frames = []
        self.anim_strip = self.animationData[state][0]
        self.length = self.animationData[state][1]
        self.size = self.animationData[state][2]

    def get_next_frame(self, state, action_speed, dt):
        # reset animation when it ends
        if self.index >= self.length:
            self.index = 0

        # check if animation must change, if so, check if it can use the stored one, if not, load the new one
        if state != self.state:
            if state == self.previous_state:
                self.save_previous_anim()
                self.frames = self.previous_frames
            self.set_animation(state)

        # check if the frames list is long enough to have the current frame stored. If it's not, cut it and append
        if len(self.frames) <= math.floor(self.index):
            img = pygame.Surface(self.size)
            img.blit(self.anim_strip, (0, 0), (math.trunc(self.index) * self.size[0], 0, self.size[0], self.size[1]))
            self.frames.append(img)

        # increment animation index
        if "static" not in self.state:
            if "idle" in self.state:
                self.index += self.anim_speed * dt
            else:
                self.index += self.anim_speed * dt * action_speed.value
        return self.frames[math.floor(self.index)]

# class SynchAnimation:
#     def __init__(self, frames, repeat: bool):
#         self.anim_strip = strip
#         self.anim_len = len(self.anim_frames)
#         self.anim_idx = 0
#         self.play = False
#         self.repeat = repeat
#
#     def trigger(self):
#         self.play = True
#
#     def toggle_repeat(self):
#         self.repeat = not self.repeat
#
#     def check_end(self):
#         if self.anim_idx >= self.anim_len:
#             self.anim_idx = 0
#             if not self.repeat:
#                 self.play = False
#
#     def update(self):
#         if self.play or self.repeat:
#             self.anim_idx += 1
#             self.check_end()
