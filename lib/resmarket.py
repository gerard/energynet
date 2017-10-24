import sys

from lib.resources import Coal, Oil, Garbage, Nuclear

class ResourceMarketBase:
    """
    This class not only tracks the amount of resources in the market, but also
    the number of resources in the *bank*.  We need to control this in order to
    avoid restocking over the amount of physical resource pieces in the game.
    """
    def __init__(self, buckets, bucketsize, start_bucket):
        self.buckets = list(buckets)
        self.available = bucketsize * len(self.buckets)
        self.bucketsize = bucketsize
        self.attempted_buy = 0
        self.market = {}
        self.restock_rate = 0

        for bucket in self.buckets:
            if bucket >= start_bucket:
                self.market[bucket] = bucketsize
            else:
                self.market[bucket] = 0

    def set_restock_rate(self, amount):
        self.restock_rate = amount

    def restock(self):
        # We don't always restock fully.  Only up to the number of pieces
        # available in the bank.
        if self.restock_rate == 0:
            raise Exception("Restock rate is zero")

        amount = min(self.restock_rate, self.available)

        for bucket in reversed(self.buckets):
            if self.market[bucket] == self.bucketsize:
                continue
            if self.bucketsize - self.market[bucket] <= amount:
                self.market[bucket] += amount
                return
            else:
                # If amount is stricly greater, it means that we fully restock
                # the bucket and continue to a cheaper bucket.
                amount -= (self.bucketsize - self.market[bucket])
                self.market[bucket] = self.bucketsize

        # If we ever reach this, it means we have a bug since it should never
        # be possible to restock the market and have leftover "amount".  The
        # number of pieces is exactly the number needed to fill the market
        # without overflowing.
        raise Exception("Market restock overflow")

    def use(self, amount):
        self.available += amount

    def buy(self, amount, dry_run=False):
        if dry_run:
            self.attempted_buy = amount
        else:
            self.attempted_buy = 0

        cost = 0

        for bucket in self.buckets:
            if not self.market[bucket]:
                continue

            if self.market[bucket] >= amount:
                # This bucket fully satisfies the buy order
                cost += amount * bucket
                self.available -= amount
                if not dry_run:
                    self.market[bucket] -= amount
                return cost
            else:
                # We empty this bucket and continue to the next one
                self.available -= self.market[bucket]
                amount -= self.market[bucket]
                cost += self.market[bucket] * bucket
                if not dry_run:
                    self.market[bucket] = 0

        return sys.maxsize

class CoalMarket(ResourceMarketBase):
    pass

class OilMarket(ResourceMarketBase):
    pass

class GarbageMarket(ResourceMarketBase):
    pass

class NuclearMarket(ResourceMarketBase):
    pass

class ResourcesMarket(dict):
    def __init__(self):
        super().__init__(self)
        self[Coal] = CoalMarket(range(1, 9), 3, 1)
        self[Oil] = OilMarket(range(1, 9), 3, 3)
        self[Garbage] = GarbageMarket(range(1, 9), 3, 7)
        self[Nuclear] = NuclearMarket(list(range(1, 9)) + [10, 12, 14, 16], 1, 10)
