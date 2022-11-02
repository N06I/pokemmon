import pygame

from cameras import YSortCam, YSortCenterCam
from character import Character, OtherPlayer
from raw import areaExits, spriteHitboxes
from file_management import get_layout
from layout_sprites import *


class Area:

    def __init__(self, areadata, client, pid, base_display):
        # tech setup
        self.client = client
        self.pid = pid
        self.base_display = base_display
        self.area_name = areadata[0]
        self.updated = None
        self.must_update = False

        # area loading
        self.exits = areaExits[self.area_name].keys()
        self.background = pygame.image.load(
            f"../poke_assets/fireRed_leafGreen/backgrounds/{self.area_name}.png").convert_alpha()

        # sprite setup
        self.atkable_grp = pygame.sprite.Group()
        self.collide_grp = pygame.sprite.Group()
        self.tile_grp = pygame.sprite.Group()
        self.char_grp = pygame.sprite.GroupSingle()
        self.character = Character(areadata[1], [self.char_grp],
                                   self.atkable_grp, self.collide_grp, self.tile_grp)
        self.visible_grp = YSortCenterCam(self.character, self.background, self.base_display)
        self.character.add(self.visible_grp)
        self.other_players = {self.pid: self.character}
        self.player_dict_simple = {}

        # layout sprites
        self.layout_setup(get_layout(self.area_name))

    def check_update(self):  # runs every tick (NOT THREADED); updates area if must_update was toggled by async_update()
        if self.must_update:
            for pid, playerdata in self.player_dict_simple.items():
                if pid not in self.other_players:
                    print(f"Player {pid} created at {playerdata[0]}.")
                    self.other_players[pid] = OtherPlayer(playerdata[0],
                                                          [self.visible_grp],
                                                          self.atkable_grp, self.collide_grp,
                                                          self.tile_grp)
            for pid, playerdata in self.player_dict_simple.items():
                if pid in self.player_dict_simple.keys() and pid != self.pid and pid in self.other_players:
                    self.other_players[pid].position = playerdata[0]
                    if self.other_players[pid].state != playerdata[1]:
                        self.other_players[pid].state = playerdata[1]
                        self.other_players[pid].anim_idx = 100
            gone = []
            for pid in self.other_players.keys():
                if pid not in self.player_dict_simple:
                    gone.append(pid)
                    print(f"Player {pid} left the area.")
            for k in gone:
                self.other_players[k].kill()
                del self.other_players[k]
            self.must_update = False

    def layout_setup(self, layout):
        for sprite_type, positions in layout.items():

            if sprite_type.startswith("left"):  # for creating n-length hitbox based on indicators like sides of a ledge
                sprite = f"{sprite_type.split('left_')[1]}"
                righties = layout[f"right_{sprite}"]
                # searches for the nearest right side of this prop to create a longer single object instead of several
                for sprite_pos in positions:
                    righty = (50000, sprite_pos[1])
                    for rightie in righties:
                        if sprite_pos[0] < rightie[0] < righty[0] and rightie[1] == righty[1]:
                            righty = rightie
                    print(f"Left: {sprite_pos} Right: {righty}")
                    LongHidden([self.collide_grp], sprite_pos,
                               (righty[0] + spriteHitboxes[sprite][0], righty[1] + spriteHitboxes[sprite][1]))
            elif not sprite_type.startswith("right"):  # avoid "right" elements, they're taken care of by their "left"
                img = pygame.image.load(f"../poke_assets/search/{sprite_type}").convert_alpha()
                img.set_colorkey(16777215)
                singletile = False
                if sprite_type.startswith("tile"):  # for things like slowing ground and shit
                    groups = [self.visible_grp, self.tile_grp]
                elif sprite_type.startswith("d_"):  # for buildings with doors, doors will prob be their own object
                    groups = [self.visible_grp, self.collide_grp]
                elif sprite_type.startswith("v_"):  # for purely visual sprites
                    groups = [self.visible_grp]
                elif sprite_type.startswith("prop"):  # for 16x16 hitbox sprites
                    groups = [self.visible_grp, self.collide_grp]
                    singletile = True
                else:           # for sprites with other hitbox shapes
                    groups = [self.visible_grp, self.collide_grp]
                for sprite_pos in positions:
                    Prop(groups, sprite_pos, img, singletile)

    def update(self, dt):
        self.updated = pygame.time.get_ticks()
        self.visible_grp.custom_draw()
        self.visible_grp.update(dt)
        self.check_update()
        # self.sync_update()
        # print("Players in area:", self.other_players)
