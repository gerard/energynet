class PowerPlantMarket:
    def __init__(self, stack):
        self.actual = [
            stack.draw(),
            stack.draw(),
            stack.draw(),
            stack.draw()
        ]
        self.future = [
            stack.draw(),
            stack.draw(),
            stack.draw(),
            stack.draw()
        ]
        self.in_auction = (False, None)

    def refill(self, stack):
        if len(self.actual) == 4:
            return

        assert len(self.actual) == 3
        assert len(self.future) == 4

        self.actual.append(stack.draw())
        self.rearrange()

    def rearrange(self):
        allmarket = self.actual + self.future
        allmarket.sort()
        self.actual = allmarket[:4]
        self.future = allmarket[4:]

    def eot_update(self, stack):
        """
        At the end of the turn, the highest costed power plant goes back to the
        stack.
        """
        assert len(self.actual) == 4
        assert len(self.future) == 4

        self.future.sort()
        stack.addback(self.future.pop())
        self.future.append(stack.draw())
        self.rearrange()

    def auction_start(self, pindex):
        self.in_auction = (True, pindex)
        return self.actual[pindex]

    def auction_done(self):
        (_, pindex) = self.in_auction
        self.in_auction = (False, None)
        return self.actual.pop(pindex)
