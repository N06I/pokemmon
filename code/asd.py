import pygame
import time
import numpy as np
import os


bg = pygame.surfarray.array2d(pygame.image.load("../poke_assets/fireRed_leafGreen/backgrounds/celadon_city.png"))

sprite_patterns = {}
path = "../poke_assets/search/"
for pwd, dirs, files in os.walk(path):
    for file in files:
        sprite_patterns[file] = pygame.surfarray.array2d(pygame.image.load(f"{path}{file}"))

matches = []
stime = time.time()
# working image comparator :D
for pattern_name in sprite_patterns.keys():
    pattern = sprite_patterns[pattern_name]
    for col in range((len(bg) - len(pattern) + 1)):
        for compared_area_start in range((len(bg[col]) - len(pattern[0]) + 1)):
            against = bg[col:col + len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
            if np.array_equal(pattern, against):
                print(f"Pattern MATCH! at ({col}, {compared_area_start}) for pattern {pattern_name}\n")
                matches.append((col, compared_area_start))

etime = time.time()
print(f"{len(matches)} total matches: {matches}")
print(f"Total run time: {etime - stime} seconds")
