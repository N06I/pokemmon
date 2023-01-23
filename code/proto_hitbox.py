import pygame


class Hitbox:
    def __init__(self, mask: pygame.mask.Mask):
        self.mask = mask

        # store the mask surface, set its colorkey and transparency
        self.image = self.mask.to_surface()
        self.image.set_alpha(136)
        self.image.set_colorkey(0)

        # store the center y, useful for Ysort
        self.center = Hitbox.get_center(self.mask)

    def overlap(self, hitbox, offset):
        return self.mask.overlap(hitbox.mask, offset)

    @classmethod
    def from_file(cls, name):
        # load the hitbox image and set the colorkey for the mask
        try:
            hb_image = pygame.image.load(f"../gamedata/hitbox/{name}").convert_alpha()
        except FileNotFoundError:
            try:
                hb_image = pygame.image.load(f"../poke_assets/sprites/{name}").convert_alpha()
            except FileNotFoundError:
                hb_image = pygame.image.load(f"../poke_assets/search/{name}").convert_alpha()
        hb_image.set_colorkey(-1)
        mask = pygame.mask.from_surface(hb_image)

        return Hitbox(mask)

    @classmethod
    def get_center(cls, mask):
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


# mesk = pygame.mask.Mask((10, 10), True)
# musk = pygame.mask.Mask((5, 5), False)
#
# hbx1 = Hitbox(mesk)
# hbx2 = Hitbox(musk)
#
# if hbx1.overlap(hbx2, (0, 0)):
#     print("OL")
# else:
#     print("NOL")
