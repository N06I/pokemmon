import pygame
import sys

reso = (640, 360)


def get_hitbox_center(mask):
    start = -1
    end = 0
    for x in range(mask.get_size()[0]):
        for y in range(mask.get_size()[1]):
            if mask.get_at((x, y)) == 1:
                if start == -1:
                    start = y
                else:
                    end = y
                break
    return (start + end) / 2


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode(reso)
        self.clock = pygame.time.Clock()
        self.event_loop = []
        self.img = pygame.image.load("../gamedata/hitbox/tree.png").convert_alpha()
        self.rect = self.img.get_rect(topleft=(0, 0))
        self.img.set_colorkey(-1)
        self.mask = pygame.mask.from_surface(self.img)
        self.mask_surf = self.mask.to_surface()
        self.rect.move_ip((300, 40))
        print(self.rect.topleft)

        vec = pygame.Vector2(2.4, 4.343)
        print(vec + (3, 2))

        # print(pygame.surfarray.array2d(self.img))
        # for x in range(self.mask.get_size()[0]):
        #     print()
        #     for y in range(self.mask.get_size()[1]):
        #         print(self.mask.get_at((x, y)), end=" ")
        # print("LOL")
        # print(get_hitbox_center(self.mask))

    def run(self):
        while True:
            self.event_loop = pygame.event.get()
            for event in self.event_loop.copy():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("#191919")
            self.screen.blit(self.img, self.rect)
            self.screen.blit(self.mask_surf, (200, 200))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Game()
    game.run()

