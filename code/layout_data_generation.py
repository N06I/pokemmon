import pygame
import numpy as np
import time
import os

surf = pygame.image.load("../poke_assets/fireRed_leafGreen/backgrounds/celadon_city.png")
og = pygame.surfarray.array2d(surf)
# print(f"Image: \n{og}\n")
search = pygame.surfarray.array2d(pygame.image.load("../poke_assets/search/fence1.png"))

sprite_patterns3 = {}
path = "../poke_assets/search/"
for pwd, dirs, files in os.walk("../poke_assets/search/"):
    for file in files:
        # sprite_patterns3.append(pygame.surfarray.array2d(pygame.image.load(f"{path}{file}")))
        sprite_patterns3[file] = pygame.surfarray.array2d(pygame.image.load(f"{path}{file}"))


def matching(pattern, against):
    cols, rows = pattern.shape

    # check center row
    check = rows // 2
    for col in range(cols):
        # if they're equal, do nothing (skip to next iteration)
        a = pattern[col][check]
        b = against[col][check]
        if pattern[col][check] == against[col][check]:
            continue
        # if they're different but pixel on pattern is transparent, skip to next iteration
        if pattern[col][check] == 16777215:
            continue
        return False

    # check center column
    check = cols // 2
    for row in range(rows):
        # if they're equal, do nothing (skip to next iteration)
        if pattern[check][row] == against[check][row]:
            continue
        # if they're different but pixel on pattern is transparent, skip to next iteration
        if pattern[check][row] == 16777215:
            continue
        return False

    # full check
    for col in range(cols):
        for row in range(rows):
            if pattern[col][row] == against[col][row]:
                continue
            if pattern[col][row] == 16777215:
                continue
            return False
    return True


matches = []
stime = time.time()
# working image comparator :D
for pattern_name in sprite_patterns3.keys():
    pattern = sprite_patterns3[pattern_name]
    for col in range(0, (len(og) - len(pattern) + 1), 8):
        for compared_area_start in range(0, (len(og[col]) - len(pattern[0]) + 1), 8):
            against = og[col:col + len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
            if matching(pattern, against):
                print(f"Pattern MATCH! at ({col}, {compared_area_start}) for pattern {pattern_name}\n")
                matches.append((col, compared_area_start))

etime = time.time()
print(f"{len(matches)} total matches: {matches}")
print(f"Total run time: {etime - stime} seconds")


# sys.exit()
# pygame.init()
# screen = pygame.display.set_mode((300, 240))
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     screen.blit(pygame.transform.scale(surf, (300, 240)), (0, 0))
#     pygame.display.update()
