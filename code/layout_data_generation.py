import pygame
import numpy as np
import time

surf = pygame.image.load("../poke_assets/fireRed_leafGreen/backgrounds/celadon_city.png")
og = pygame.surfarray.array2d(surf)

search = pygame.surfarray.array2d(pygame.image.load("../poke_assets/search/house1.png"))
matches = []
stime = time.time()

sprite_patterns3 = np.array([search])
# working image comparator :D
for pattern_idx in range(len(sprite_patterns3)):
    pattern = sprite_patterns3[pattern_idx]
    for col in range(len(og) - len(pattern) + 1):
        for compared_area_start in range(len(og[col]) - len(pattern[0]) + 1):
            against = og[col:col+len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
            if np.array_equal(pattern, against):
                print(f"Pattern MATCH! at ({col}, {compared_area_start}) for pattern {pattern_idx}\n")
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
