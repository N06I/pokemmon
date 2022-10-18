import pygame

from cameras import YSortCam, YSortCenterCam
from character import Character, OtherPlayer
from raw import areaExits


class Area:
    # area class settings
    staticCamAreas = ["bill_house"]

    def __init__(self, areadata, client, pid, base_display):
        # tech setup
        self.client = client
        self.pid = pid
        self.base_display = base_display
        self.area_name = areadata[0]
        self.updated = None
        self.must_update = False
        # run threaded function that loops infinitely while area is loaded and handles server sync updating
        # asynchronically to avoid lag on non-zero ms clients       !!! IMPORTANT !!!

        # area loading
        self.exits = areaExits[self.area_name].keys()
        self.background = pygame.image.load(
            f"../poke_assets/fireRed_leafGreen/backgrounds/{self.area_name}.png").convert_alpha()

        # sprite setup
        self.atkable_grp = pygame.sprite.Group()
        self.collide_grp = pygame.sprite.Group()
        self.tile_grp = pygame.sprite.Group()
        self.char_grp = pygame.sprite.GroupSingle()
        self.character = Character(areadata[1], [self.char_grp, self.collide_grp],
                                   self.atkable_grp, self.collide_grp, self.tile_grp)
        self.visible_grp = YSortCam(self.character, self.background, self.base_display) if self.area_name in self.staticCamAreas else YSortCenterCam(self.character, self.background, self.base_display)
        self.character.add(self.visible_grp)
        self.other_players = {self.pid: self.character}
        self.player_dict_simple = {}

    def check_update(self):
        if self.must_update:
            for pid, playerdata in self.player_dict_simple.items():
                if pid not in self.other_players:
                    self.other_players[pid] = OtherPlayer(playerdata[0],
                                                               [self.collide_grp, self.visible_grp],
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
            for k in gone:
                self.other_players[k].kill()
                del self.other_players[k]
            self.must_update = False

    def update(self, dt):
        self.updated = pygame.time.get_ticks()
        self.visible_grp.custom_draw()
        self.visible_grp.update(dt)
        self.check_update()
        # self.sync_update()
        # print("Players in area:", self.other_players)
