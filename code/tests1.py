class Item:
    def __init__(self, name: str, modifiers: dict):
        self.name = name
        self.modifiers = modifiers

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{mod}:{val}" for mod, val in self.modifiers.items())


class Entity:
    def __init__(self):
        self.name = "mister"
        self.position = 0
        self.stats = {"ms": Stat(10), "aspd": Stat(1.2), "hp": Stat(100)}
        self.equipped_items = {}

    def equip(self, slot, item: Item):
        if slot in self.equipped_items:
            self.unequip(slot)
        self.equipped_items[slot] = item
        print(f"{item.name} equipped. Stats: ", end="")
        for modifier, value in item.modifiers.items():
            print(f"{modifier} {value}", end="; ")
            self.stats[modifier] += value
        print()

    def unequip(self, slot):
        print(f"{self.equipped_items[slot].name} unequipped. Stats: ", end="")
        for modifier, value in self.equipped_items[slot].modifiers.items():
            print(f"{modifier} {value}", end="; ")
            self.stats[modifier] -= value
        print()
        del self.equipped_items[slot]

    def move(self):
        print(f"Called move => Old pos: {self.position}", end=", ")
        self.position += self.stats["ms"]   # for now
        print(f"New pos: {self.position}")

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{stat}:{val}" for stat, val in self.stats.items())


class Stat:
    def __init__(self, val, flat=True):
        self._value = val
        self._flat = flat

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @value.deleter
    def value(self):
        del self._value

    def __add__(self, other):
        if self._flat:
            return self.value + other
        return self.value * other

    def __sub__(self, other):
        if self._flat:
            return other - self.value
        return other / self.value

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __str__(self):
        if self._flat:
            return str(self.value)
        return str(self.value*100 - 100) + "%"


class Equipment:
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.data = dict(*args, **kwargs)

    def __setitem__(self, key, value):
        self.callback(key, value)
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]
        self.callback(key)

    def __getitem__(self, key):
        return self.data[key]

    def __repr__(self):
        for slot, item in self.data.items():
            print(f"[{slot}] " + ", ".join(f"{mod}:{amt}" for mod, amt in item.modifiers.items()))
        return "-=-=-"



ent = Entity()
print(ent)
ent.move()
ent.move()
itm = Item("Helm of Wisdom", {"ms": Stat(2.4, flat=False), "aspd": Stat(10), "hp": Stat(10)})
ent.equip("helm", itm)
print(ent)
itam = Item("Shoulderguards of opium", {"ms"})
print(ent)
