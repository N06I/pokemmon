import math

import pygame, time
from file_management import get_sprite_assets


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, groups, atkables, collidables, tiles, name="male_mc"):
        super().__init__(groups)
        # positional info
        self.position = position
        self.current_tile = None

        # general setup
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(topleft=(0, 0))
        self.hitbox = pygame.rect.Rect(self.rect.left, self.rect.top + self.rect.height/3, self.rect.width, self.rect.height/4)
        self.atkableSprites = atkables
        self.collidableSprites = collidables
        self.tileSprites = tiles

        # character states
        self.buffs = {"movespeed": 1}
        self.state = "walk_down"

        # asset loading
        self.assets = get_sprite_assets(name)

        # animation
        self.name = name
        self.anim_idx = 1000
        self.anim_len = 0
        self.anim_size = None
        self.anim_strip = None
        self.anim_speed = 7

        # physics
        self.inputV = pygame.Vector2()
        self.listV = [pygame.Vector2()]

        # combat
        self.cooldowns = {}
        self.stats = {"movespeed": 140, "action_speed": 1}
        self.weight = 50

    @property
    def effective_msV(self):    # movespeed with buff
        return self.stats["movespeed"] if "movespeed" not in self.buffs else self.stats["movespeed"] + self.buffs["movespeed"]

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
        sumV = pygame.Vector2()
        for vector in self.listV:
            sumV += vector
        self.listV = []

        # apply movespeed
        finalV = (self.effective_msV * self.inputV) + sumV

        # check for dragging tiles and apply friction

        drag_tile = False
        for tile in self.tileSprites:
            if self.rect.colliderect(tile.rect):
                drag_tile = True
                self.current_tile = tile

        # decelerate based on self's weight and terrain friction
        finalV -= ((self.current_tile.coef * self.weight) if drag_tile else self.weight * 2) * finalV.normalize() if finalV.magnitude() != 0 else pygame.Vector2()

        # finally apply movement with delta time
        self.position += finalV * dt
        self.rect.midbottom = self.position
        self.hitbox.midbottom = self.position

        for collidable in self.collidableSprites:
            if self.rect.colliderect(collidable.rect):
                print("Collision !")

    def animate(self, dt):
        if self.anim_idx >= self.anim_len:
            self.anim_idx = 0
            # self.anim_end_triggers()

            # removed anim_idx == 0 check; probable redundancy solved by initting all entities with a too high anim_idx
            self.anim_strip = self.assets[self.state][0]
            self.anim_len = self.assets[self.state][1]
            self.anim_size = self.assets[self.state][2]
            # correct for varying animation sizes
            if self.rect.size != self.anim_size:
                midbot = self.rect.midbottom
                self.rect.size = self.anim_size
                self.rect.midbottom = midbot

        self.image = pygame.Surface((self.anim_size[0], self.anim_size[1]), pygame.SRCALPHA)
        self.image.blit(self.anim_strip, (0, 0),
                        (math.trunc(self.anim_idx) * self.anim_size[0], 0, self.anim_size[0], self.anim_size[1]))

        if "static" not in self.state:
            if self.state.split("_")[0] == "idle":
                self.anim_idx += self.anim_speed * dt
            else:
                self.anim_idx += self.anim_speed * dt * self.stats["action_speed"]

    def cast(self, skill, cd):
        if skill not in self.cooldowns:
            self.cooldowns[skill] = (cd * self.buffs["cd"] if "cd" in self.buffs else cd, pygame.time.get_ticks())
            eval(skill + "()")

    def cool_down(self, dt):
        tick = pygame.time.get_ticks()
        delet_this = []
        for skill, timings in self.cooldowns.items():   # timings = (cd, start_tick)
            if tick - timings[1] > timings[0]:
                delet_this.append(skill)
        for s in delet_this:
            del self.cooldowns[s]

    def update(self, dt):
        self.cool_down(dt)
        self.move(dt)
        self.animate(dt)
