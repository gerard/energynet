import random
import functools

from lib.resources import Coal, Oil, Garbage, Nuclear

@functools.total_ordering
class Player:
    def __init__(self, pid, color):
        self.pid = pid
        self.color = color
        self.active = False
        self.cash = 50
        self.auction_rights = True      # Cleared each turn
        self.raise_rights = True        # Cleared each auction

        self.plants = []
        self.resources = {Coal: 0, Oil: 0, Garbage: 0, Nuclear: 0}
        self.network = []

    def __eq__(self, other):
        return self.worth() == other.worth()

    def __lt__(self, other):
        return self.worth() < other.worth()

    def worth(self):
        # Used to establish player order.  There's no possibility for tie since
        # all power plant have distinct prices.
        return max([p.price for p in self.plants])

    def __repr__(self):
        return "P{pid}[${cash:3}|C{cities:2}]{ar}{pr}{more}{plants}".format(
            pid=self.pid,
            cash=self.cash,
            more="/" if self.plants else "",
            plants="/".join([repr(p) for p in self.plants]),
            ar="A" if self.auction_rights else "",
            pr="P" if self.raise_rights else "",
            cities=len(self.network)
        )

class PlayerList:
    """
    A class that contains a list of players and manages player order and status

    Please note: it's important to not confuse indexes with pids.  The pids can
    be anything where equality can be established.  The pid is also the handle
    given to class users.
    The indexes are integers strictly smaller than the number of players which
    are indexes in the player list handled by this class.  A player index will
    change as the game progresses (it's tied to player order), a pid will not.
    The class uses strings as pids on purpose, even if that string is a single
    digit.
    """

    PALETTE = [     # The color palette used to represent the players
        (0, 255, 0),
        (0, 0, 255),
        (128, 128, 0)
    ]

    def __init__(self, n):
        self.list = [
            Player(str(k + 1), PlayerList.PALETTE[k]) for k in range(n)
        ]
        random.shuffle(self.list)
        self.active_auctioneer_pid = 0
        self.active_participant_pid = 0

    def __repr__(self):
        return "\n".join([repr(p) for p in self.list])

    def index(self, who):
        for (n, p) in enumerate(self.list):
            if p.pid == who:
                return n

    def set_active(self, idx):
        for (n, _) in enumerate(self.list):
            self.list[n].active = (n == idx)

    def first(self):
        self.set_active(0)
        return self.list[0].pid

    def last(self):
        self.set_active(len(self.list) - 1)
        return self.list[-1].pid

    def next(self, who):
        if who == self.list[-1].pid:
            return None

        idx = self.index(who) + 1
        self.set_active(idx)
        return self.list[idx].pid

    def canbuy(self, who, resource, howmuch=1):
        p = self.list[self.index(who)]

        total = 0
        for plant in p.plants:
            if plant.canuse(resource):
                # A plant can store twice as much resources as it can use in a
                # single turn.
                total += (2 * plant.cost)

        # TODO: This is not 100% correct.  Hybrid plants can use both Coal and
        #       Oil but they cannot store both types in full amounts.
        return total - p.resources[resource] >= howmuch

    def clear_active(self):
        for p in self.list:
            p.active = False

    def get_cash(self, who):
        return self.list[self.index(who)].cash

    def get_color(self, who):
        return self.list[self.index(who)].color

    def get_network(self, who):
        return self.list[self.index(who)].network

    def remove_auction_rights(self, who):
        self.list[self.index(who)].raise_rights = False
        self.list[self.index(who)].auction_rights = False

    def participant_pass(self, who):
        self.list[self.index(who)].raise_rights = False

    def participants_left(self):
        count = 0
        for p in self.list:
            if p.raise_rights:
                count += 1
        return count

    def auctioneers_left(self):
        count = 0
        for p in self.list:
            if p.auction_rights:
                count += 1
        return count

    def next_auctioneer(self):
        self.clear_active()
        for p in self.list:
            if p.auction_rights:
                p.active = True
                return p.pid
        return -1

    def recalculate_player_order(self):
        self.list.sort()

    def next_auction_participant(self, fromwho):
        self.clear_active()
        fromindex = self.index(fromwho)
        for i in range(len(self.list) - 1):
            k = (fromindex + i + 1) % len(self.list)
            if self.list[k].raise_rights:
                self.list[k].active = True
                return self.list[k].pid

        raise Exception("No more participants in auction")

    def clear_participation_rights(self):
        for (n, p) in enumerate(self.list):
            # Players without right to auction can't participate anymore
            if p.auction_rights:
                self.list[n].raise_rights = True

    def auction_winner(self):
        assert self.participants_left() == 1
        for p in self.list:
            if p.raise_rights:
                return p.pid

    def player_buys_plant(self, who, plant, price):
        self.list[self.index(who)].cash -= price
        self.list[self.index(who)].plants.append(plant)
        self.list[self.index(who)].auction_rights = False
        self.list[self.index(who)].raise_rights = False

    def player_buys_resource(self, who, resource, amount, price):
        self.list[self.index(who)].cash -= price
        self.list[self.index(who)].resources[resource] += amount

    def player_buys_city(self, who, city, price):
        self.list[self.index(who)].cash -= price
        self.list[self.index(who)].network.append(city)
