import pygame
import threading

from area import Area
from raw import areaExits
from character import OtherPlayer


class World:
    def __init__(self, areadata, client, pid, base_display):   # just send a player data object instead of playerpos
        self.client = client
        self.pid = pid
        self.base_display = base_display

        # areas
        self.area = None               # current area
        self.area_name = areadata[0]      # its name
        self.new_area = False
        self.loaded_areas = {}  # {"area1": areaObject} | made a dict to access area names, could be an object list
        self.load_area(areadata)
        thread = threading.Thread(target=self.async_update)
        thread.start()

    def load_area(self, areadata):
        self.area = Area(areadata, self.client, self.pid, self.base_display)
        self.area_name = areadata[0]
        self.loaded_areas[self.area_name] = self.area   # currently useless bc server handles area loading
        self.new_area = False
        # self.client.update_server_area(self.area_name)

    def check_exits(self):
        exitdata = None
        for exitpoint in self.area.exits:
            if self.area.character.hitbox.collidepoint(exitpoint):
                exitdata = areaExits[self.area_name][exitpoint]
            print("exit: ", exitpoint, " char:", self.area.character.rect.midbottom)
        if exitdata:
            self.load_area(exitdata)

    def async_update(self):
        while True:
            self.area.player_dict_simple = self.client.instance_update(self.area.character)
            for pid, playerdata in self.area.player_dict_simple.items():
                # if pid not in self.area.other_players.keys():
                #
                #     self.area.other_players[pid] = OtherPlayer(playerdata[0],
                #                                                [self.area.collide_grp, self.visible_grp],
                #                                                self.area.atkable_grp, self.area.collide_grp,
                #                                                self.area.tile_grp)
                #     self.area.other_players[pid].add(self.area.visible_grp)
                if pid in self.area.player_dict_simple.keys() and pid != self.pid:
                    self.area.other_players[pid].position = playerdata[0]
                    if self.area.other_players[pid].state != playerdata[1]:
                        self.area.other_players[pid].state = playerdata[1]
                        self.area.other_players[pid].anim_idx = 100
            gone = []
            for pid in self.area.other_players.keys():
                if pid not in self.area.player_dict_simple:
                    gone.append(pid)
            for k in gone:
                self.area.other_players[k].kill()
                del self.area.other_players[k]
            if self.new_area:
                self.client.update_server_area(self.area_name)
                self.new_area = False

    def run(self, dt):
        self.area.update(dt)
        self.check_exits()

        # next_area = self.area.character.swaps_area()
        # if next_area:
        #     self.load_area(next_area, )

        # can make a custom pygame userevent which gets sent every 5 minutes? to avoid checking every tick
        # tick = pygame.time.get_ticks()
        # for area, obj in self.loaded_areas.items():
        #     if (tick - obj.updated) > 50000:   # however many ticks of idle area
        #         self.loaded_areas.pop(area)
        #         del obj
