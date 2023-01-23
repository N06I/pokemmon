import pygame

from camera import Camera
from entity import Entity
from character import Character
from raw import areaExits
from file_management import get_layout, get_hitbox, get_hitbox_center
from layout_sprites import *


def load_sprite_image(sprite_type):
    try:
        return pygame.image.load(f"../poke_assets/sprites/{sprite_type}").convert_alpha()
    except FileNotFoundError:
        return pygame.image.load(f"../poke_assets/search/{sprite_type}").convert_alpha()


class Area:

    def __init__(self, areadata, client, pid, base_display, get_events):
        # tech setup
        self.client = client
        self.pid = pid
        self.base_display = base_display
        self.area_name = areadata[0]
        self.updated = None
        self.must_update = False

        # area loading
        if self.area_name in areaExits:
            self.exits = areaExits[self.area_name]
        self.background = pygame.image.load(
            f"../poke_assets/fireRed_leafGreen/backgrounds/{self.area_name}.png").convert_alpha()
        self.bg_rect = self.background.get_rect(topleft=(0, 0))

        # sprite setup
        self.char_grp = pygame.sprite.GroupSingle()
        self.collide_grp = pygame.sprite.Group()
        self.ledge_grp = pygame.sprite.Group()
        self.tile_grp = pygame.sprite.Group()
        self.door_grp = pygame.sprite.Group()
        self.character = Character(get_events, areadata[1], [self.char_grp],
                                   self.collide_grp, self.tile_grp, self.door_grp, self.bg_rect)
        self.visible_grp = Camera(self.character, self.background, self.base_display, get_events)
        self.visible_grp.add(self.character)
        self.other_players = {self.pid: self.character}
        self.other_players = {}
        self.player_dict_simple = {}
        # layout sprites
        self.layout_setup(get_layout(self.area_name))

    def update(self, dt):
        self.updated = pygame.time.get_ticks()
        self.visible_grp.update(dt)
        self.visible_grp.custom_draw()
        self.check_update()

    def check_update(self):  # runs every tick (NOT THREADED); updates area if must_update was toggled by async_update()
        if self.must_update:
            for pid, playerdata in self.player_dict_simple.items():
                if pid not in self.other_players and pid != self.pid:
                    print(f"Player {pid} created at {playerdata[0]}.")
                    self.other_players[pid] = Entity(playerdata[0], [self.visible_grp, self.collide_grp],
                                                     self.collide_grp, self.tile_grp, self.door_grp, self.bg_rect)
                    self.other_players[pid].position = playerdata[0]
                    if self.other_players[pid].state != playerdata[1]:
                        self.other_players[pid].state = playerdata[1]
                        self.other_players[pid].anim_idx = 100
            gone = []
            for pid in self.other_players.keys():
                if pid not in self.player_dict_simple:
                    gone.append(pid)
                    print(f"Player {pid} left the area.")
            for k in gone:
                self.other_players[k].kill()
                del self.other_players[k]
            self.must_update = False

    def layout_setup(self, layout):
        for sprite_type, occurs in layout.items():
            if sprite_type.startswith("coll_"):   # for purely collisional sprites
                groups = [self.collide_grp]
                for sprite_pos in occurs:
                    CustomTile(groups, sprite_pos)
                continue
            img = pygame.image.load(f"../poke_assets/sprites/{sprite_type}").convert_alpha()
            img.set_colorkey(-1)
            size = img.get_size()
            mask, mask_image, mask_center = get_hitbox(sprite_type)

            if sprite_type.startswith("tile_"):  # for tile objects
                groups = [self.visible_grp, self.tile_grp]
                for sprite_pos in occurs:
                    CustomTile(groups, sprite_pos, img=img, hitbox=mask, hb_surf=mask_image, friction=2.6)
                continue
            if sprite_type.startswith("ledge_"):    # for ledges
                groups = [self.ledge_grp, self.collide_grp]
                directions = [dirn for dirn in sprite_type[:-5].split("_")[1:]]
                for sprite_pos in occurs:
                    Ledge(groups, sprite_pos, mask, mask_image, size, directions)
                continue
            if sprite_type.startswith("v_"):  # for purely visual sprites
                groups = [self.visible_grp]
            elif sprite_type.startswith("door_"):  # for door objects
                groups = [self.visible_grp, self.collide_grp, self.door_grp]
            else:
                groups = [self.visible_grp, self.collide_grp]
            for sprite_pos in occurs:
                GameObj(groups, sprite_pos, img, mask, mask_image, mask_center, size)

    def mk_generalist_prop(self, sprite_type, occurs):
        groups = [self.visible_grp, self.collide_grp]
        img = load_sprite_image(sprite_type)
        mask = get_hitbox(sprite_type)
        for sprite_pos in occurs:
            GameObj(groups, sprite_pos, img, mask, mask_image, mask_center, size)
