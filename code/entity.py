import math
import pygame

from file_management import get_sprite_assets, get_hitbox
from entity_stats import *
from proto_animation import Animator


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, groups, collidables, tiles, doors, background, name="male_mc"):
        super().__init__(groups)
        # positional info
        self.position = pygame.Vector2(position)

        # general setup
        self.name = name
        self.surf = pygame.Surface((16, 16))
        self.hitbox, self.hitbox_surf, self.hitbox_center = get_hitbox(f"{name}.png")
        self.rect = self.surf.get_rect(topleft=(0, 0))  # ????
        self.rect = pygame.rect.Rect(self.rect.left, self.rect.top + self.rect.height / 3, self.rect.width,
                                       self.rect.height / 4)

        # accessible sprites
        self.collidableSprites = collidables
        self.tileSprites = tiles
        self.doorSprites = doors
        self.bg_rect = background

        # character states
        self.buffs = {"movespeed": 1}
        self.state = "walk_down"

        # asset loading
        self.assets = get_sprite_assets(name)
        print(self.assets)

        # animation
        self.anim_idx = 1000
        self.anim_len = 0
        self.anim_size = None
        self.anim_strip = None
        self.anim_speed = 7

        # physics
        self.inputV = pygame.Vector2()
        self.v_list = [pygame.Vector2()]

        # combat relevant data
        self.cooldowns = {}
        self.action_speed = Stat(1)
        self.stats = {"movespeed": Stat(160, action_speed=self.action_speed)}   # good ms amt = 140 ~ 150
        self.items = {}
        self.weight = 50

        # test
        self.animator = Animator(get_sprite_assets(name), self.state)

    def set_action(self, new):
        if new not in self.state:
            self.state = f"{new}_{self.state.split('_')[1]}"
            self.anim_idx = 100

    def set_direction(self, new):
        if new not in self.state:
            self.state = f"{self.state.split('_')[0]}_{new}"
            self.anim_idx = 100

    def action_input(self):
        pass

    def move(self, dt):
        # check current frame's external speed vector list, extract total vector, empty list
        v_sum = pygame.Vector2()
        for vector in self.v_list:
            v_sum += vector
        self.v_list = []

        # apply movespeed
        self.finalV = (self.stats["movespeed"].value * self.inputV) + v_sum

        # set friction based on terrain
        if tile := self.check_tiles():
            friction = tile.coef * self.weight
        else:
            friction = 2 * self.weight
        # decelerate based on self's weight and terrain friction
        self.finalV -= friction * self.finalV.normalize() if self.finalV.magnitude() != 0 else pygame.Vector2()
        self.finalV *= dt

        # finally apply movement, axis by axis to allow single axis movement during collisions
        # horizontal
        self.apply_movement(0)
        if not self.bg_rect.contains(self.rect):
            self.undo_movement(0)
        elif self.check_collidables():
            print("colliding x")
            self.relocate(0)
        # vertical
        self.apply_movement(1)
        if not self.bg_rect.contains(self.rect):
            self.undo_movement(1)
        elif self.check_collidables():
            print("colliding y")
            self.relocate(1)

    def apply_movement(self, axis):
        self.position[axis] += self.finalV[axis]
        self.rect.midbottom = self.position

    def undo_movement(self, axis):
        self.position[axis] -= self.finalV[axis]
        self.rect.midbottom = self.position

    def check_collidables(self):
        return self.collided(self.collidableSprites)

    def check_tiles(self):
        return self.collided(self.tileSprites)

    def mask_colliding(self, rect, collidable):
        x = collidable.rect.left - rect.left
        y = collidable.rect.top - rect.top
        if self.hitbox.overlap(collidable.hitbox, (x, y)):
            return collidable

    def collided(self, group):
        for collidable in group:
            if self.rect.colliderect(collidable.rect):
                if self.mask_colliding(self.rect, collidable):
                    return collidable

    def check_sides(self, rect1, rect2):
        for collidable in self.collidableSprites:
            one, two = False, False
            if rect1.colliderect(collidable.rect):
                one = self.mask_colliding(rect1, collidable)
            if rect2.colliderect(collidable.rect):
                two = self.mask_colliding(rect2, collidable)
            if one and not two:
                return 1
            elif two and not one:
                return -1
            elif one and two:
                return 0
        return 0

    def relocate(self, axis):
        self.undo_movement(axis)
        if axis == 0:
            slide = self.check_sides(self.rect.move(0, -math.ceil(abs(self.inputV[0]))),
                                     self.rect.move(0, math.ceil(abs(self.inputV[0]))))
            # set position based on test
            self.position += (0, slide)
        elif axis == 1:
            slide = self.check_sides(self.rect.move(-math.ceil(abs(self.inputV[1])), 0),
                                     self.rect.move(math.ceil(abs(self.inputV[1])), 0))
            # set position based on test
            self.position += (slide, 0)
        # set rect
        self.rect.midbottom = self.position

    def animate(self, dt):
        self.image = self.animator.get_next_frame(self.state, self.action_speed, dt)
        # if self.anim_idx >= self.anim_len:
        #     self.anim_idx = 0
        #     # self.anim_end_triggers()
        #
        #     # removed anim_idx == 0 check; probable redundancy solved by initting all entities with a too high anim_idx
        #     self.anim_strip = self.assets[self.state][0]
        #     self.anim_len = self.assets[self.state][1]
        #     self.anim_size = self.assets[self.state][2]
        #     # correct for varying animation sizes
        #     if self.rect.size != self.anim_size:
        #         midbot = self.rect.midbottom
        #         self.rect.size = self.anim_size
        #         self.rect.midbottom = midbot
        #
        # self.image = pygame.Surface((self.anim_size[0], self.anim_size[1]), pygame.SRCALPHA)
        # self.image.blit(self.anim_strip, (0, 0),
        #                 (math.trunc(self.anim_idx) * self.anim_size[0], 0, self.anim_size[0], self.anim_size[1]))
        #
        # if "static" not in self.state:
        #     if "idle" in self.state:
        #         self.anim_idx += self.anim_speed * dt
        #     else:
        #         self.anim_idx += self.anim_speed * dt * self.action_speed.value

    def cast(self, skill, cd):
        if skill not in self.cooldowns:
            self.cooldowns[skill] = ((cd * self["cd"] / self.action_speed.value) if "cd" in self.buffs else cd,
                                     pygame.time.get_ticks())
            eval(skill + "()")

    def cool_down(self, dt):
        tick = pygame.time.get_ticks()
        delet_this = []
        for skill, timings in self.cooldowns.items():  # timings = (cd, start_tick)
            if tick - timings[1] > timings[0]:
                delet_this.append(skill)
        for s in delet_this:
            del self.cooldowns[s]

    def teleport(self, pos):
        self.position = pos
        self.rect.midbottom = self.position

    def equip(self, item):
        item_type = item.type
        if item_type in self.items:
            self.unequip(item_type)

        self.items[item_type] = item
        for modifier in item.modifiers:
            self.stats[modifier] += modifier

    def unequip(self, item_slot):
        for modifier in self.items[item_slot].modifiers:
            self.stats[modifier] -= modifier
        del self.items[item_slot]

    def update(self, dt):
        self.cool_down(dt)
        self.move(dt)
        self.animate(dt)

    def __setitem__(self, key, value):
        self.stats[key] = value

    def __delitem__(self, key):
        del self.stats[key]

    def __getitem__(self, key):
        return self.stats[key]

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{stat}:{val}" for stat, val in self.stats.items())
