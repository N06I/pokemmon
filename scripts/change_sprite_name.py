import os


old_name = "ledge_down_right.png"
new_name = "ledge_down_right0.png"

folders = ["poke_assets/search", "poke_assets/sprites", "gamedata/hitbox"]

for folder in folders:
    for pwd, dirs, files in os.walk(f"../{folder}"):
        for file in files:
            if file == old_name:
                os.rename(f"{pwd}/{old_name}", f"{pwd}/{new_name}")
