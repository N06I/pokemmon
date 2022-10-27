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
    newdict = {"gamestate": ("bill_house", (320, 184))}
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
