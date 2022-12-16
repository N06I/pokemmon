import json
import os
import pygame

from raw import animData


def load_gamestate(pid):
    path = f"../gamedata/data.json"
    with open(path, "r") as file:
        gamedata = json.load(file)
    return gamedata["gamestate"]


def make_game(pid):
    newdict = {"gamestate": ("bill_house", (120, 90))}
    with open(f"../gamedata/data.json", "w") as file:
        json.dump(newdict, file)
    return True


def get_sprite_assets(name):
    path = f"../poke_assets/fireRed_leafGreen/sprites/{name}"
    assets = {}
    for pwd, dirs, files in os.walk(path):
        for file in files:
            key = file.split(".")[0]
            anim_len = animData[name][key.split("_")[0]][0]
            anim_size = animData[name][key.split("_")[0]][1]
            assets[key] = [pygame.image.load(f"{path}/{file}").convert_alpha(), anim_len, anim_size]
    return assets


def get_layout(area):
    with open("../gamedata/layouts.json") as f:
        layouts = json.load(f)
        return layouts[f"{area}.png"]


def get_hitbox(name):
    # load the hitbox image and set the colorkey for the mask
    hb_image = pygame.image.load(f"../gamedata/hitbox/{name}")
    hb_image.set_colorkey(16777215)

    # create the mask and the mask surface, set mask surf colorkey and transparency
    mask = pygame.mask.from_surface(hb_image)
    mask_surf = mask.to_surface()
    mask_surf.set_alpha(136)
    mask_surf.set_colorkey((0, 0, 0))

    mask_center = get_hitbox_center(mask)

    return mask, mask_surf, mask_center


def get_hitbox_center(mask):
    start = -1
    end = 0
    for x in range(mask.get_size()[0]):
        for y in range(mask.get_size()[1]):
            if mask.get_at((x, y)) == 1:
                if start == -1:
                    start = y
                else:
                    end = y
                break
    return (start + end) / 2
