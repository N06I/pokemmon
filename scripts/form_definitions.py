import json

sprite_forms = {"bd_building1.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building2.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building3.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building4.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building5.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building6.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building7.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_building8.png": {"ttrim": 16, "ltrim": 1, "rtrim": 1},
                "bd_clonatron2000.png": {'ttrim': 16},
                "bd_gym1.png": {'ttrim': 16},
                "bd_house1.png": {'ttrim': 16},
                "bd_house2.png": {'ttrim': 16},
                "bd_house3.png": {'ttrim': 16},
                "bd_house4.png": {'ttrim': 16},
                "bd_pokecenter1.png": {'ttrim': 16},
                "bin1.png": {'ttrim': 0.5},
                "building1.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "building14.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "building4.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "building5.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "building7.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "building8.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "desk1.png": {'ttrim': 0.5},
                "d_building1.png": {"ttrim": 0.5, "ltrim": 1, "rtrim": 1},
                "d_hut1.png": {'ttrim': 0.5},
                "d_mall1.png": {'ttrim': 0.5},
                "fancyfence.png": {'ttrim': 0.5},
                "fence1.png": {'ttrim': 0.5},
                "fence2.png": {'ttrim': 0.5},
                "fountain1.png": {'ttrim': 0.2, "ltrim": 4, "rtrim": 4},
                "house1.png": {'ttrim': 0.5},
                "house2.png": {'ttrim': 0.5},
                "house4.png": {'ttrim': 0.5},
                "ledge1.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge2.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge3.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge4.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge5.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge6.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge7.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "ledge8.png": {'ltrim': 0.1, 'rtrim': 0.1},
                "pole1.png": {'ttrim': 0.5},
                "prop1.png": {'ttrim': 0.5},
                "prop10.png": {'ttrim': 0.5},
                "prop11.png": {'ttrim': 0.5},
                "prop12.png": {'ttrim': 0.5},
                "prop13.png": {'ttrim': 0.5},
                "prop14.png": {'ttrim': 0.5},
                "prop15.png": {'ttrim': 0.5},
                "prop16.png": {'ttrim': 0.5},
                "prop17.png": {'ttrim': 0.5},
                "prop18.png": {'ttrim': 0.5},
                "prop19.png": {'ttrim': 0.5},
                "prop2.png": {'ttrim': 0.5},
                "prop20.png": {'ttrim': 0.5},
                "prop21.png": {'ttrim': 0.5},
                "prop3.png": {'ttrim': 0.5},
                "prop4.png": {'ttrim': 0.5},
                "prop5.png": {'ttrim': 0.5},
                "prop6.png": {'ttrim': 0.5},
                "prop7.png": {'ttrim': 21},
                "prop8.png": {'ttrim': 0.5},
                "prop9.png": {'ttrim': 0.5},
                "sapling1.png": {'ttrim': 0.5},
                "seat_east1.png": {'ttrim': 0.5},
                "seat_west1.png": {'ttrim': 0.5},
                "sofa1.png": {'ttrim': 0.5},
                "sofa2.png": {'ttrim': 0.5},
                "store_cab1.png": {'ttrim': 0.5},
                "store_cab2.png": {'ttrim': 0.5},
                "store_cab3.png": {'ttrim': 0.5},
                "table1.png": {'ttrim': 0.5},
                "tile_weed1.png": {'ttrim': 0.5},
                "tree.png": {'ttrim': 0.5},
                "vending1.png": {'ttrim': 0.5},
                "vitrina1.png": {'ttrim': 0.5},
                "vitrina2.png": {'ttrim': 0.5},
                "v_arch1.png": {'ttrim': 0.5},
                "v_arch2.png": {'ttrim': 0.5},
                "v_flower1.png": {'ttrim': 0.5},
                "v_flower2.png": {'ttrim': 0.5},
                "v_idk1.png": {'ttrim': 0.5},
                "v_idk2.png": {'ttrim': 0.5},
                "v_roof1.png": {'ttrim': 0.5},
                "v_roof2.png": {'ttrim': 0.5},
                "v_skyscrtop.png": {'ttrim': 0.5},
                "v_tube1.png": {'ttrim': 0.5}}

# for sprite_type, form in sprite_forms.items():
#     if "building" in sprite_type:
#         print(f'"{sprite_type}": {{"ttrim": {form["ttrim"]}, "ltrim": 1, "rtrim": 1}},')
#     else:
#         print(f'"{sprite_type}": {form},')
    # if ("ltrim" or "rtrim" in form) and "ttrim" in form:
    #     print(f'"{sprite_type}": {{"ttrim": {form["ttrim"]}}},')
    # else:
    #     print(f'"{sprite_type}": {form},')

with open("../gamedata/layouts.json") as f:
    layouts = json.load(f)

for sprite_type, form in sprite_forms.items():
    for area, sprites in layouts.items():
        if sprite_type in sprites:
            layouts[area][sprite_type]["form"] = form

with open("../gamedata/layouts.json", "w") as f:
    json.dump(layouts, f)
