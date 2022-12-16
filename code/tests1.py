import pygame


# class Hitbox(pygame.mask.Mask):
#     def __init__(self, size, fill: bool = False):
#         super().__init__(size, fill)
#
# a = Hitbox((2, 3))


class A:
    def __init__(self):
        self.x = [1, 2]
        self.bee = B(self.x)
        self.run()
        print(self.bee.x)

    def run(self):
        self.x = [3, 2]


class B:
    def __init__(self, x):
        self.x = x
        print(self.x)


aa = A()
