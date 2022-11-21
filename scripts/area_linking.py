import pickle
import os


# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl
# UNUSED, same with exits.pkl


def add_missing():
    with open("../gamedata/exits.pkl", "rb") as f:
        exitdata = pickle.load(f)
        bgareas = []
        for pwd, dirs, files in os.walk("../poke_assets/fireRed_leafGreen/backgrounds"):
            for file in files:
                bgareas.append(file)
                if file not in exitdata:
                    exitdata[file] = {}
    with open("../gamedata/exits.pkl", "wb") as f:
        pickle.dump(exitdata, f)
    return bgareas


def link(areas, two_way=True):
    old_area = areas[0]
    new_area = areas[1]
    with open("../gamedata/exits.pkl", "rb") as f:
        exitdata = pickle.load(f)
        print("Example link: ((x, y), (x, y)), ((x, y), (x, y))")
    link = eval("(" + input() + ")")
    if type(link) != tuple or type(link[0]) != tuple or type(link[1]) != tuple:
        return
    if type[link[0][0]] != tuple or tuple != type[link[0][1]] or type[link[1][0]] != tuple or tuple != type[link[1][1]]:
        return
    for n in link[0][0] + link[0][1] + link[1][0] + link[1][1]:
        if type(n) != int:
            return
    exitdata[old_area][link[0]] = (new_area, link[1])
    if two_way:
        exitdata[new_area][link[1]] = (old_area, link[0])
    with open("../gamedata/exits.pkl", "wb") as f:
        pickle.dump(exitdata, f)
    print(f"Successfully linked {old_area}[{link[0]}] to {new_area} [{link[1]}]")


# with open("../gamedata/exits.pkl", "wb") as f:
#     pickle.dump({}, f)
bgareas = add_missing()
while True:
    key_in = input("\nType 2 area names to add link, 1 to see its exits:")
    if " " not in key_in:
        with open("../gamedata/exits.pkl", "rb") as f:
            exitdata = pickle.load(f)
        print(exitdata[key_in + ".png"])
        continue
    areas = key_in.split(", ")
    if len(key_in) < 4 or key_in == "end" or len(areas) > 2:
        break
    if areas[0] + ".png" not in bgareas or areas[1] + ".png" not in bgareas:
        print("Area names not found")
        continue
    link(areas)
