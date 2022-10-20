import pygame
import numpy as np
import sys

surf = pygame.image.load("../poke_assets/fireRed_leafGreen/backgrounds/test.png")

px_map1 = pygame.surfarray.array2d(surf)
folder = [px_map1]
sprite_patterns = []

for file in range(len(folder)):
    sprite_patterns.append([])
    for col in range(len(folder[file])):
        sprite_patterns[file].append([])
        for row in folder[file][col]:
            sprite_patterns[file][col].append(row)  # adds pixel to pattern

            # now, to check for repeat(ambiguous) patterns, iterate through -sprite_patterns- and break once a difference is found



pygame.surfarray.blit_array(surf, folder[0])

print(folder[0])

# sys.exit()

pygame.init()
screen = pygame.display.set_mode((300, 240))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(pygame.transform.scale(surf, (300, 240)), (0, 0))
    pygame.display.update()
