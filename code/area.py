import pygame

from cameras import YSortCam, YSortCenterCam
from character import Character
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

    def update(self, dt):
        self.updated = pygame.time.get_ticks()
        # self.sync_update()
        self.visible_grp.custom_draw()
        self.visible_grp.update(dt)
        # print("Players in area:", self.other_players)
