import pygame


class Chat:
    def __init__(self, base_display):
        self.b_display = base_display
        reso = base_display.get_size()
        self.rect = pygame.Rect(0, reso[1]/3*2, reso[0]/3, reso[1]/3)

    def update(self):
        pygame.draw.rect(self.b_display, pygame.Color("lightskyblue3"), self.rect, 2)
        print("chat:", self.rect)
