import numpy
import pygame
import os

trees = {}
path = "../poke_assets/trecuatros/"
for pwd, dirs, files in os.walk(path):
    for file in files:
        trees[file] = pygame.surfarray.pixels3d(pygame.image.load(f"{path}{file}"))

for col in range(len(trees["tree8.png"])):
    print("\n")
    for row in range(len(trees["tree8.png"][0])):
        print(f"\n[{col}, {row}]")
        for tree, pixels in trees.items():
            print(f"og: {trees['tree8.png'][col][row]}; {tree}: {pixels[col][row]}")
            if not numpy.array_equal(trees["tree8.png"][col][row], pixels[col][row]):
                trees["tree8.png"][col][row] = 16777215
                print("Pixel mismatch")
                break
# trees["tree1.png"] = pygame.surfarray.pixels3d(pygame.image.load("../poke_assets/trees/tree1.png"))
print(trees["tree8.png"].shape)

surf = pygame.Surface(trees["tree8.png"].shape[:2])
pygame.surfarray.blit_array(surf, trees["tree8.png"])
pygame.image.save_extended(surf, "../poke_assets/search/tree_filter2.png")
