import pygame
import time
import os

surf = pygame.image.load("../poke_assets/forma-todo.png")
og = pygame.surfarray.array2d(surf)

parte = pygame.image.load("../poke_assets/forma-parte.png")
asd = pygame.surfarray.array2d(parte)
matches = []
stime = time.time()

print(og)
print(asd)

sprite_patterns3 = [asd]
# path = "../poke_assets/test/"
# for pwd, dirs, files in os.walk(path):
#     for file in files:
#         sprite_patterns3.append(pygame.surfarray.array2d(pygame.image.load(f"{path}{file}")))


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
        # if they're different but pixel on pattern is transparent, do nothing ( skip to next iteration)
        if pattern[col][check] == 16777216:
            continue
        return False

    # check center column
    check = cols // 2
    for row in range(rows):
        # if they're equal, do nothing (skip to next iteration)
        if pattern[check][row] == against[check][row]:
            continue
        # if they're different but pixel on pattern is transparent, do nothing ( skip to next iteration)
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


# working image comparator :D
for pattern_idx in range(len(sprite_patterns3)):
    pattern = sprite_patterns3[pattern_idx]
    for col in range(len(og) - len(pattern) + 1):
        for compared_area_start in range(len(og[col]) - len(pattern[0]) + 1):
            against = og[col:col + len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
            if matching(pattern, against):
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
