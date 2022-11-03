import time

import pygame
import sys
from world import World
from client import Client
from file_management import load_gamestate, make_game

reso = (640, 360)
scaled_reso = (1280, 720)

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
        self.base_display = pygame.Surface(reso)
        self.clock = pygame.time.Clock()
        self.client = Client()
        self.pid = self.client.set_pid()

        # for now, I'm just creating a new game each time the game is launched
        self.gamestate = make_game(self.pid)    # returns true
        self.gamestate = load_gamestate(self.pid)   # loads stored tuple: ("areaname", (pos, ition))

        self.world = World(self.gamestate, self.client, self.pid, self.base_display)

    def run(self):
        prev_time = time.time()
        while True:
            tyme = time.time()
            dt = tyme - prev_time
            prev_time = tyme
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.world.end = True
                    self.client.send(self.client.DISCONNECT_MESSAGE)
                    time.sleep(0.5)
                    pygame.quit()
                    sys.exit()

            self.base_display.fill("#191919")

            self.world.run(dt)
            self.screen.blit(pygame.transform.scale(self.base_display, scaled_reso), (-scaled_reso[0]/4, -scaled_reso[1]/4))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
