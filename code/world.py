import time

import pygame
import threading

from area import Area
from raw import areaExits, exitLinks


class World:
    def __init__(self, game, areadata, client, pid, base_display):
        self.game = game
        self.client = client
        self.pid = pid
        self.base_display = base_display

        # areas
        self.area = None               # current area object
        self.area_name = areadata[0]      # its name
        self.new_area = False
        self.loaded_areas = {}  # {"area1": areaObject} | currently useless bc areas are being loaded as new (for now)
        self.load_area(areadata)

        self.end = False
        self.update_thread = threading.Thread(target=self.async_update)
        self.update_thread.start()

    def load_area(self, areadata):
        self.area = Area(self.game, areadata, self.client, self.pid, self.base_display)
        self.area_name = areadata[0]
        self.loaded_areas[self.area_name] = self.area   # currently useless bc server handles area loading
        self.new_area = True
        print(areaExits)

        # replace method with this when background loaded areas (client) are implemented
        # if areadata[0] in self.loaded_areas:
        #     self.set_area(self.loaded_areas[areadata[0]], areadata)
        # else:
        #     area = Area(self.game, areadata, self.client, self.pid, self.base_display)
        #     self.set_area(area, areadata)

    def set_area(self, area, areadata):
        self.area = area
        self.area_name = areadata[0]
        self.new_area = True

    def check_exits(self):
        char_hbx = self.area.character.hitbox
        exitdata = None
        for i, exitrect in enumerate(self.area.exits):
            if char_hbx.colliderect(exitrect):
                spawnrect = exitLinks[self.area_name][i][1]
                if exitrect.width > 1:
                    x = spawnrect.centerx + spawnrect.width * (char_hbx.centerx - exitrect.centerx) / exitrect.width
                else:
                    x = spawnrect.centerx
                if exitrect.height > 1:
                    y = spawnrect.centery + spawnrect.height * (char_hbx.centery - exitrect.centery) / exitrect.height
                else:
                    y = spawnrect.bottom
                exitdata = (exitLinks[self.area_name][i][0], (x, y))
            # print("exit: ", exit, " char:", self.area.character.rect.midbottom)
        if exitdata:
            if pygame.key.get_pressed()[pygame.K_e]:
                self.load_area(exitdata)

    def async_update(self):     # runs in a separate thread; sets must_update so area knows an update was received
        while True:
            if self.end:
                break
            time.sleep(0.005)   # need to sleep to not overwhelm OS with crazy amounts of unnecessary update requests

            # request instance update and set flat so area update method knows to grab the updated data
            self.area.player_dict_simple = self.client.instance_update(self.area.character)
            self.area.must_update = True

            # if area has changed, update the area on server side
            if self.new_area:
                self.client.update_server_area(self.area_name)
                self.new_area = False

            # if player has sent new_message, send it to the server and reset flag
            if self.game.chat.new_message:
                self.client.send(self.game.chat.last_sent)
                self.game.chat.new_message = False

            # request chat update and set flag so chat knows to receive it
            self.game.chat.new_received = self.client.chat_update()
            self.game.chat.must_update = True

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
