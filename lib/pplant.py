#!/usr/bin/env python3
import functools

from lib.resources import Coal, Oil, Garbage, Nuclear

@functools.total_ordering
class PowerPlant:
    def __init__(self, price, cost, production):
        self.price = price
        self.cost = cost
        self.production = production
        self.type = "?"
        self.bid = None
        self.resources = []

    def __eq__(self, other):
        return self.price == other.price

    def __ne__(self, other):
        return self.price != other.price

    def __lt__(self, other):
        return self.price < other.price

    def __repr__(self):
        return "[{:02d}] {}{}=>{}".format(
            self.price,
            self.type,
            self.cost,
            self.production
        )

    def production_str(self):
        return "{} => {}".format(self.cost, self.production)

    def canuse(self, resource):
        return resource in self.resources

class CoalPlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "C"
        self.resources = [Coal]

class OilPlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "O"
        self.resources = [Oil]

class GarbagePlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "G"
        self.resources = [Garbage]

class HybridPlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "H"
        self.resources = [Coal, Oil]

class GreenPlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "!"
        self.resources = []

class NuclearPlant(PowerPlant):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "N"
        self.resources = [Nuclear]
