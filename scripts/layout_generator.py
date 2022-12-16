import pygame
import time
import os
import json


def matching(pattern, against):
    cols, rows = pattern.shape

    # check center row
    check = rows // 2
    for col in range(cols):
        # if they're equal, do nothing (skip to next iteration)
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


def generate_layout(area, sprite_patterns):
    bg = pygame.surfarray.array2d(pygame.image.load(f"../poke_assets/fireRed_leafGreen/backgrounds/{area}"))
    with open("../gamedata/layouts.json") as f:
        layouts = json.load(f)
    if area not in layouts:
        layouts[area] = {}
    area_sprites = {}
    stime = time.time()
    # working image comparator :D
    for pattern_name in sprite_patterns.keys():
        pattern = sprite_patterns[pattern_name]
        area_sprites[pattern_name] = []
        for col in range(0, (len(bg) - len(pattern) + 1), 8):
            for compared_area_start in range(0, (len(bg[col]) - len(pattern[0]) + 1), 8):
                against = bg[col:col + len(pattern), compared_area_start:compared_area_start + len(pattern[0])]
                if matching(pattern, against):
                    # print(f"Pattern MATCH! at ({col}, {compared_area_start}) for pattern {pattern_name}")
                    area_sprites[pattern_name].append((col, compared_area_start + len(pattern[0])))
        if len(area_sprites[pattern_name]) == 0:
            del area_sprites[pattern_name]
    etime = time.time()
    print(f"{len(area_sprites)} sprites found: {area_sprites}")
    print(f"Total run time for {area}: {etime - stime} seconds\n")
    layouts[area] = area_sprites
    with open("../gamedata/layouts.json", "w") as f:
        json.dump(layouts, f, indent=2)


def generate_all_layouts(gend_areas):
    sprite_patterns = {}
    path = "../poke_assets/search/"
    for pwd, dirs, files in os.walk(path):
        for file in files:
            sprite_patterns[file] = pygame.surfarray.array2d(pygame.image.load(f"{path}{file}"))

    s_time = time.time()
    for pwd, dirs, files in os.walk("../poke_assets/fireRed_leafGreen/backgrounds/"):
        for file in files:
            generate_layout(file, sprite_patterns)
            gend_areas.append(file)
    e_time = time.time()
    print(f"Total full game sprite recognition script run time: {e_time - s_time} seconds\n")


generated_areas = []
generate_all_layouts(generated_areas)
print(f"Generated areas: {generated_areas}")
