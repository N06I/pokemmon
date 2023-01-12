from entity_stats import *


class Item:
    def __init__(self, item_type, name: str, modifiers: dict):
        self.type = item_type
        self.name = name
        self.modifiers = modifiers

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{mod}:{val}" for mod, val in self.modifiers.items())


class Entity:
    def __init__(self, name):
        self.name = name
        self.action_speed = Stat(1)
        self.stats = {"ms": Stat(action_speed=self.action_speed), "hp": Stat()}
        self.items = {}

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

    def __setitem__(self, key, value):
        self.stats[key] = value

    def __delitem__(self, key):
        del self.stats[key]

    def __getitem__(self, key):
        return self.stats[key]

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{stat}:{val}" for stat, val in self.stats.items())


ent = Entity("homie")
print(ent["ms"])
ent["ms"] += Stat(4, mult=0.2)
print(ent["ms"])

