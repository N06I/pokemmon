import time

import pygame
import sys
from world import World
from client import Client
from file_management import load_gamestate, make_game
from chat import Chat

base_reso = (320, 180)
reso = (640, 360)
reso = (1280, 720)

# data stored in server, received once when game launches
area_name = "area1"
pos = (320, 180)


class Game:
    def __init__(self):
        new_game = True  # placeholder for somehow saving game state, could be from online login
        account_id = None

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode(reso)
        pygame.display.set_caption("Pokeman")
        self.base_display = pygame.Surface(base_reso)
        self.clock = pygame.time.Clock()
        self.client = Client()
        self.pid = self.client.set_pid()
        self.event_loop = []

        # for now, I'm just creating a new game each time the game is launched
        self.gamestate = make_game(self.pid)    # returns true
        self.gamestate = load_gamestate(self.pid)   # loads stored tuple: ("areaname", (pos, ition))

        self.world = World(self, self.gamestate, self.client, self.pid, self.base_display)
        self.chat = Chat(self)
        self.chat.send("Welcome back", "sys")
        self.chatting = False

    def run(self):
        prev_time = time.time()
        while True:
            tyme = time.time()
            dt = tyme - prev_time
            prev_time = tyme
            self.event_loop = pygame.event.get()
            for event in self.event_loop.copy():
                if event.type == pygame.QUIT:
                    self.world.end = True
                    pygame.quit()
                    self.client.send(self.client.DISCONNECT_MESSAGE)
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # chat toggle
                    if event.key == pygame.K_RETURN:
                        if self.chatting:
                            self.chat.send(self.chat.in_text)
                        self.chatting = not self.chatting
                        self.chat.set_colors()

            self.base_display.fill("#191919")

            self.world.run(dt)
            self.screen.blit(pygame.transform.scale(self.base_display, reso), (0, 0))
            self.chat.update(self.event_loop, dt)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
