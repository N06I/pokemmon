import threading
import pygame


gr = pygame.sprite.Group()


class A(pygame.sprite.Sprite):
    def __init__(self, groups):
        self.image = pygame.Surface((0, 0))
        super().__init__(groups)
        self.a = 1
        # thread = threading.Thread(target=self.ba)
        # thread.start()
        del self
        print("LMAO")

    def ba(self):
        while True:
            self.a = 2
            print(self.a)


ja = A([gr])
print(ja.image)
