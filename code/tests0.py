class Item:
    def __init__(self, name: str, modifiers: dict):
        self.name = name
        self.modifiers = modifiers

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{mod}:{val}" for mod, val in self.modifiers.items())


class Entity:
    def __init__(self, name):
        self.name = name
        self.stats = {}
        self.action_speed = Stat()

    def __setitem__(self, key, value):
        self.stats[key] = value

    def __delitem__(self, key):
        del self.stats[key]

    def __getitem__(self, key):
        return self.stats[key]

    def __str__(self):
        return f"[{self.name}] " + ", ".join(f"{stat}:{val}" for stat, val in self.stats.items())


class Stat:
    def __init__(self, name=None):
        self.name = name
        self._value = 0
        self._flat = self.StatMultiplier(self.recalc)
        self._mult = self.StatMultiplier(self.recalc)

    @property
    def value(self):
        return self._value

    def recalc(self):
        self._value = self._flat * self._mult

    class StatMultiplier:
        def __init__(self, recalc, base=1):
            self.value = base
            self.recalc = recalc

        def __add__(self, other):
            self.recalc()
            return other + self.value

        def __sub__(self, other):
            self.recalc()
            return other - self.value

        def __mul__(self, other):
            return other * self.value


ent = Entity("homie")
