import pygame

animData = {
    "male_mc": {
        "idle": (4, (16, 20)),
        "walk": (6, (16, 20)),
        "run": (4, (16, 20))
    }
}

areaExits = {
    "bill_house": {
        (120, 167): ("celadon_city", (664, 537))
    },
    "celadon_city": {
        (664, 527): ("bill_house", (120, 167)),
        (248, 290): ("celadon_mall_f1", (168, 254)),
        (184, 290): ("celadon_mall_f1", (40, 254))
    },
    "celadon_mall_f1": {
        (168, 260): ("celadon_city", (248, 296)),
        (40, 260): ("celadon_city", (184, 296))
    }
}

spriteHitboxes = {"fence1.png": 1,
                  "ledge1.png": (16, 8)}
