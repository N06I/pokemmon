# d = {
#     'a': {
#         'b': {
#             'b1': {},
#             'b2': {}
#         },
#         'c': {
#             'c1': {}
#         }
#     }
# }
#
#
# def paths(curr, path=[]):
#     for child, dikt in curr.items():
#         path.append(child)
#         yield path
#         yield from paths(dikt, path)
#         path.pop()
#
#
# for path in paths(d):
#     print(path)
import pygame


def frames(anim_strip, length, size):
    for idx in range(length):
        frame = pygame.Surface(size)
        frame.blit(anim_strip, (0, 0), (idx * size[0], 0, size[0], size[1]))
        yield frame


anim_frames = frames(pygame.image.load("../poke_assets/fireRed_leafGreen/sprites/male_mc/walk_down.png"), 6, (16, 20))


print(next(anim_frames))
print(next(anim_frames))
print(next(anim_frames))
print(next(anim_frames))
print(next(anim_frames))
print(next(anim_frames))
