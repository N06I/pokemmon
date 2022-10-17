import pygame

#a = pygame.Surface((10, 10))
#b = a.get_rect(topleft=(5,0))

#print(b.midtop)

weight = 50
move_vector = pygame.Vector2(10, 10)

print(move_vector - weight)


# class Entity:
#     def __init__(self):
#         # combat
#         self.cooldowns = {}
#         self.buffs = {}
#         self.stats = {"movespeed": 3}
#         self.mass = 100
#         self.gravity = 10
#
#     @property
#     def weight(self):
#         return self.mass * self.gravity
#
# a = Entity()
# print(a.weight)
# a.mass+=10
# print(a.weight)
