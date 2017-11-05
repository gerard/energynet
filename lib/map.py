#!/usr/bin/env python3
# pylint: disable=invalid-name
import sys

from lib.util import cwise_sort

class MapVertex:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos
        self.buildings = 0
        self.building_colors = []

    def __repr__(self):
        return self.name

    def get_colors(self):
        ret = [(255, 255, 255)] * 3
        for (n, c) in enumerate(self.building_colors):
            ret[n] = c
        return ret

class MapEdge:
    def __init__(self, fro, to, cost):
        self.fro = fro
        self.to = to
        self.cost = cost

class Map:
    def __init__(self, size, translated=None, transposed=False):
        self.vlist = list()
        self.elist = list()
        self.size = size
        self.transposed = transposed
        self.translation = translated
        self.active_city = None
        self.next_city = None

    def translate(self, translation):
        self.translation = translation

    def vertex(self, v):
        self.vlist.append(v)

    def get_vertex(self, name):
        for v in self.vlist:
            if name == v.name:
                return v

    def edge(self, e):
        assert e.fro in self.vlist
        assert e.to in self.vlist
        self.elist.append(e)

    def city(self, name, pos):
        if self.translation:
            pos = (pos[0] + self.translation[0], pos[1] + self.translation[1])
        if self.transposed:
            pos = (pos[1], pos[0])
        assert pos[0] < self.size[0]
        assert pos[1] < self.size[1]
        self.vertex(MapVertex(name, pos))

    def road(self, fro, to, cost):
        self.edge(MapEdge(self.get_vertex(fro), self.get_vertex(to), cost))

    def index(self, city):
        for (n, c) in enumerate(self.vlist):
            if c.name == city.name:
                return n

    def get_reachable_cities(self, fromcity):
        """
        These are returned in clockwise order for UI usability purposes.
        """
        clist = []
        for r in self.elist:
            if r.fro.name == fromcity.name:
                clist.append((r.to.pos[0], r.to.pos[1], r.to))
            elif r.to.name == fromcity.name:
                clist.append((r.fro.pos[0], r.fro.pos[1], r.fro))

        # The purpose of the awkward format of the list elements is to allow
        # for easy sorting, see cwise_sort documentation.
        clist_sorted = cwise_sort(fromcity.pos, clist)

        # Scrape away the extra coordinates
        return [e[2] for e in clist_sorted]

    def set_active_city(self, city):
        self.active_city = self.index(city)

    def set_next_city(self, city):
        self.next_city = self.index(city)

    def get_active_city(self):
        return self.vlist[self.active_city]

    def set_active_to_next(self):
        self.active_city = self.next_city

    def first(self):
        return self.vlist[0]

    def build(self, city, color):
        self.vlist[self.index(city)].buildings += 1
        self.vlist[self.index(city)].building_colors.append(color)

    def building_cost(self, city, step=1):
        nbuildings = self.vlist[self.index(city)].buildings
        if nbuildings == 0:
            return 10
        elif nbuildings == 1 and step > 1:
            return 15
        elif nbuildings == 2 and step > 2:
            return 20

        return sys.maxsize
