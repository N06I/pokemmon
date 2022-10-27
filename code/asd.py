import pygame
import numpy

green = pygame.surfarray.array2d(pygame.image.load("../poke_assets/search/fence1.png"))
# otro = pygame.surfarray.array2d(pygame.image.load("../poke_assets/tree1-test5.svg"))

for col in green:
    print()
    for px in col:
        print(px, end=" ")

# colors = {}
# for col in range(len(green)):
#     for row in range(len(green[col])):
#         if green[col][row] not in colors:
#             colors[green[col][row]] = (col, row)
# print("Colors found:")
# for color, pos in colors.items():
#     print(color, pos)
#
# colors = {}
# for col in range(len(otro)):
#     for row in range(len(otro[col])):
#         if otro[col][row] not in colors:
#             colors[otro[col][row]] = (col, row)
# print("Colors found:")
# for color, pos in colors.items():
#     print(color, pos)
