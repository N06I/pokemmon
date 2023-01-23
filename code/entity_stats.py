class Modifier:
    def __init__(self, flat=0, mult=0.0):
        self.flat = flat
        self.mult = mult

    def __add__(self, other):
        return self.__class__(self.flat + other.flat, self.mult + other.mult)

    def __sub__(self, other):
        return self.__class__(self.flat - other.flat, self.mult - other.mult)

    def __str__(self):
        return f"[Mod] flat:[{self.flat}] mult:[{self.mult}]"


class Stat(Modifier):
    def __init__(self, flat=0, mult=0.0, action_speed=None):
        """Working. Action speed changes might not be reflected here. Needs testing"""
        super().__init__(flat, mult)
        self.action_speed = action_speed
        if action_speed:
            self.recalc = self._action_recalc
        else:
            self.recalc = self._passive_recalc
        self._value = None
        self.recalc()

    @property
    def value(self):
        return self._value

    def _action_recalc(self):
        self._value = self.flat * (1 + self.mult) * self.action_speed.value

    def _passive_recalc(self):
        self._value = self.flat * (1 + self.mult)

    def __add__(self, other):
        print("added: ", other)
        return Stat(self.flat + other.flat, self.mult + other.mult, self.action_speed)

    def __sub__(self, other):
        print("subtracted: ", other)
        return Stat(self.flat - other.flat, self.mult - other.mult, self.action_speed)

    def __str__(self):
        return f"[{'A' if self.action_speed else 'Non-a'}ction Stat] {self.value} | flat: {self.flat} mult: " \
               f"{self.mult} {('(action:' + str(self.action_speed.value) + ')') if self.action_speed else ''}"


# actspd = Stat(1.1)
# tast = Stat(7, 0.2, actspd)
# tnst = Stat(7, 0.2)
# modd = Modifier(3, 0.05)
# print(tast)
# print(modd)
#
# # print(type(tast))
# # print(type(modd))
# # tast += modd
# # print(tast)
# # tast -= modd
# # print(tast)
# print(tnst)
