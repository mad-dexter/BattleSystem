import random


class Spell:
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.type = type
        self.cost = cost
        self. dmg = dmg

    def generate_spell_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return  random.randrange(low, high)

    def get_spell_cost(self):
        return self.cost