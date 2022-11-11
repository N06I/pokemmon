import pygame
import os

animData = {
    "male_mc": {
        "idle": (4, (16, 20)),
        "walk": (6, (16, 20)),
        "run": (4, (16, 20))
    }
}

areaExits = {
    # "bill_house": {
    #     pygame.Rect(107, 166, 25, 1): ("celadon_city", (664, 537))
    # },
    # "celadon_city": {
    #     (664, 527): ("bill_house", (120, 167)),
    #     (248, 290): ("celadon_mall_f1", (168, 254)),
    #     (184, 290): ("celadon_mall_f1", (40, 254))
    # },
    # "celadon_mall_f1": {
    #     (168, 260): ("celadon_city", (248, 296)),
    #     (40, 260): ("celadon_city", (184, 296)),
    #     (54, 44): ("celadon_mall_f2", (60, 40)),
    #     (54, 50): ("celadon_mall_f2", (60, 46))
    # },
    # "celadon_mall_f2": {
    #     (44, 40): ("celadon_mall_f1", (74, 44)),
    #     (44, 46): ("celadon_mall_f1", (74, 50))
    # }
}

exitLinks = {}

for pwd, dirs, files in os.walk("../poke_assets/fireRed_leafGreen/backgrounds"):
    for file in files:
        if file[:-4] not in areaExits:
            areaExits[file[:-4]] = []
        if file[:-4] not in exitLinks:
            exitLinks[file[:-4]] = []


def mk_link(area1, area2, data1, data2, twoway=True):
    rect1, rect2 = pygame.Rect(data1), pygame.Rect(data2)
    areaExits[area1].append(rect1)
    exitLinks[area1].append((area2, rect2))
    if twoway:
        areaExits[area2].append(rect2)
        exitLinks[area2].append((area1, rect1))


links = [["bill_house", "celadon_city", [106, 166, 25, 1], [656, 535, 15, 1]]]

for link in links:
    mk_link(*link)

print(areaExits)
print(exitLinks)
