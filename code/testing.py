import random

import pygame
import numpy as np
import sys
from random import choice


def ra():
    return choice([0, 2366701, 62207, 13217535, 8355711, 15391129, 13387839])


surf = pygame.image.load("../poke_assets/fireRed_leafGreen/backgrounds/test.png")
og = pygame.surfarray.array2d(surf)
px_map1 = og[0]
print(f"Image: \n{og}\n")
sprite_patterns2 = np.array([np.array([choice([0, 2366701, 62207, 13217535, 8355711]) for i in range(random.randint(1, 4))], dtype=object) for j in range(6)], dtype=object)
a = True
cnt = 0
while a:
    cnt += 1
    sprite_patterns3 = np.array([
        np.array([np.array([ra(), ra()]), np.array([ra(), ra()])]),
        np.array([np.array([ra(), ra(), ra()]), np.array([ra(), ra(), ra()]), np.array([ra(), ra(), ra()])]),
        np.array([np.array([ra(), ra(), ra()]), np.array([ra(), ra(), ra()])])], dtype=object)
    # working image comparator :D
    for pattern_idx in range(len(sprite_patterns3)):
        pattern = sprite_patterns3[pattern_idx]
        for col in range(len(og) - len(pattern) + 1):
            for compared_area_start in range(len(og[col]) - len(pattern[0]) + 1):
                against = og[col:col+len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
                if np.array_equal(pattern, against):
                    print(f"Pattern MATCH! at ({col}, {compared_area_start}) for pattern {pattern_idx}:\n{pattern}")
                    a = False
print(f"Attempts until match: {cnt}")

# working 1 dimensional comparator
# for pattern_idx in range(len(sprite_patterns2)):
#     for compared_area_start in range(len(px_map1) - len(sprite_patterns2[pattern_idx]) + 1):
#         print(f"Pattern: {sprite_patterns2[pattern_idx]} | Comparing against: {px_map1[compared_area_start:compared_area_start + len(sprite_patterns2[pattern_idx])]}")
#         if np.array_equal(sprite_patterns2[pattern_idx], px_map1[compared_area_start:compared_area_start + len(sprite_patterns2[pattern_idx])]):
#             print(f"Pattern MATCH! at {compared_area_start} for pattern {pattern_idx}: {sprite_patterns2[pattern_idx]}")

print("\nSprite patterns:")
for pat in sprite_patterns3:
    print(pat)

# for file in range(len(folder)):
#     sprite_patterns.append([])
#     for col in range(len(folder[file])):
#         sprite_patterns[file].append([])
#         for row in folder[file][col]:
#             sprite_patterns[file][col].append(row)  # adds pixel to pattern
#
# # now, to check for repeat(ambiguous) patterns, iterate through -sprite_patterns- and break once a difference is
# found

# pygame.surfarray.blit_array(surf, folder[0])
sys.exit()
pygame.init()
screen = pygame.display.set_mode((300, 240))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(pygame.transform.scale(surf, (300, 240)), (0, 0))
    pygame.display.update()
