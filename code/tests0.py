import pygame


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.button_down = True
        self.position = 0
        self.ms_stat = 10
        self.action_speed = 1
        self.items = [Item(2), Item(6)]
        self.buffs = [Buff(0.1), Buff(-0.5), Buff(0.2), Buff(1)]

    @property
    def move_speed(self):
        return (self.ms_stat + sum(item.ms for item in self.items)) * sum(buff.factor for buff in self.buffs)

    def move(self):
        if self.button_down:
            self.position += self.move_speed * self.action_speed


class Item:
    def __init__(self, ms):
        self.ms = ms


class Buff:
    def __init__(self, factor):
        self.factor = factor


ent = Entity([])
print(ent.move_speed)
