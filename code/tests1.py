import time

import pygame
import sys
from tests0 import Chat

base_reso = (320, 180)
reso = (640, 360)
reso = (1280, 720)

# data stored in server, received once when game launches
area_name = "area1"
pos = (320, 180)


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode(reso)
        pygame.display.set_caption("Pokeman")
        self.base_display = pygame.Surface(base_reso)
        self.clock = pygame.time.Clock()
        self.pid = 1
        self.event_loop = []

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
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # chat toggle
                    if event.key == pygame.K_RETURN:
                        if self.chatting:
                            self.chat.send(self.chat.in_text)
                        self.chatting = not self.chatting

            self.base_display.fill("#191919")

            self.screen.blit(pygame.transform.scale(self.base_display, reso), (0, 0))
            self.chat.update(self.event_loop, dt)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()
