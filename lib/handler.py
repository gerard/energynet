import re
import sys
import pygame       # Need event mapping to get rid of this

from lib.game_status import GameStatus
from lib.resources import Coal, Oil, Garbage, Nuclear

class Handler:
    HANDLER_NOP = "H/NOP "
    HANDLER_PUSH = "H/PUSH"
    HANDLER_POP = "H/POP "
    HANDLER_REPLACE = "H/REPL"

    def __init__(self, game):
        self.game = game
        self.status = self.prompt = ""

    def __call__(self, event):
        if event.key == pygame.K_q:
            return (Handler.HANDLER_PUSH, HandlerQuit(self.game))
        elif event.key == pygame.K_F1:
            toggle_status = self.game.toggle_road_costs()
            self.status = "Road costs {}".format(
                "ON" if toggle_status else "OFF"
            )
        elif event.key == pygame.K_F2:
            toggle_status = self.game.toggle_city_labels()
            self.status = "City labels {}".format(
                "ON" if toggle_status else "OFF"
            )
        elif event.key == pygame.K_F10:
            self.status = "(tip: {})".format(self.game.get_random_tip())

        return (Handler.HANDLER_NOP, None)

    def __repr__(self):
        return "{}[{}]".format(
            re.sub("Handler", "", self.__class__.__name__),
            re.sub("0x", "", hex(id(self)))
        )

    def reactivate(self):   # pylint: disable=no-self-use
        return (Handler.HANDLER_NOP, None)

    def chain(self, event, hstatus, hnext=None):
        if hstatus == Handler.HANDLER_NOP:
            return super(type(self), self).__call__(event)
        if hstatus == Handler.HANDLER_POP:
            return (hstatus, None)

        assert hnext
        return (hstatus, hnext)

    @staticmethod
    def post():
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))

class HandlerQuit(Handler):
    def __init__(self, game):
        super().__init__(game)
        self.status = "Sad to see you go!"
        self.prompt = "Do you want to quit? (y/n)"

    def __call__(self, ev):
        if ev.key == pygame.K_y:
            sys.exit(1)
        elif ev.key == pygame.K_n:
            return self.chain(ev, Handler.HANDLER_POP)

        return (Handler.HANDLER_NOP, None)

class HandlerPressEnter(Handler):
    def __init__(self, game, msg):
        super().__init__(game)
        self.status = msg
        self.prompt = "Press enter to continue"

    def __call__(self, ev):
        if ev.key == pygame.K_RETURN:
            return self.chain(ev, Handler.HANDLER_POP)
        return self.chain(ev, Handler.HANDLER_NOP)

class HandlerAuction(Handler):
    def __init__(self, game, plant, top_bidder):
        super().__init__(game)
        self.participant = self.game.players.next_auction_participant(top_bidder)
        self.top_bidder = top_bidder
        self.plant = plant
        # Participant must raise at least $1
        self.participant_bid = plant.bid + 1
        self.set_statusprompt()

    def set_statusprompt(self):
        self.status = "Plant {} will be auctioned, current bid: ${} by P{}".format(
            self.plant, self.plant.bid, self.top_bidder)
        self.prompt = "P{}: (r)aise ${}(m)(l) or (p)ass?".format(
            self.participant, self.participant_bid)

    def __call__(self, ev):
        if ev.key == pygame.K_m:
            self.participant_bid += 1
        elif ev.key == pygame.K_l and self.participant_bid - 1 > self.plant.bid:
            self.participant_bid -= 1
        elif ev.key == pygame.K_r:
            self.plant.bid = self.participant_bid
            nh = HandlerAuction(self.game, self.plant, self.participant)
            return self.chain(ev, Handler.HANDLER_REPLACE, nh)
        elif ev.key == pygame.K_p:
            self.game.players.participant_pass(self.participant)

            # The auctioning process can only terminate on a pass since nothing
            # else reduces the participants to one.
            if self.game.players.participants_left() > 1:
                nh = HandlerAuction(self.game, self.plant, self.top_bidder)
                return self.chain(ev, Handler.HANDLER_REPLACE, nh)

            winner = self.game.players.auction_winner()
            plant = self.game.pmkt.auction_done()
            price = self.plant.bid
            self.game.players.player_buys_plant(winner, plant, price)
            self.game.players.remove_auction_rights(winner)
            nh = HandlerPressEnter(
                self.game,
                (
                    "P{} wins the bid for {}.  ".format(winner, plant) +
                    "Pays {}.".format(price)
                )
            )
            return self.chain(ev, Handler.HANDLER_REPLACE, nh)
        else:
            return self.chain(ev, Handler.HANDLER_NOP)

        self.set_statusprompt()
        return self.chain(ev, Handler.HANDLER_NOP)

class HandlerAuctionStart(Handler):
    def __init__(self, game):
        super().__init__(game)
        self.game.players.clear_participation_rights()
        self.auctioneer = self.game.players.next_auctioneer()
        self.status = "Auction stage started"
        self.prompt = (
            "P{}: ".format(self.auctioneer) +
            "Pick a power plant to auction (1)(2)(3)(4) or (p)ass"
        )

    def __call__(self, ev):
        if pygame.K_1 <= ev.key <= pygame.K_4:
            pindex = ev.key - pygame.K_1
            plant = self.game.pmkt.auction_start(pindex)

            if plant.price > self.game.players.get_cash(self.auctioneer):
                self.status = "P{} can't afford that".format(self.auctioneer)
                return self.chain(ev, Handler.HANDLER_NOP)

            if self.game.players.auctioneers_left() == 1:
                winner = self.auctioneer
                plant = self.game.pmkt.auction_done()
                price = plant.price
                self.game.players.player_buys_plant(winner, plant, price)
                self.game.players.remove_auction_rights(winner)
                self.game.next_stage()
                nh = HandlerPressEnter(
                    self.game,
                    "P{} wins the bid for {}.  Pays {}.".format(winner,
                                                                plant,
                                                                price)
                )
                self.game.pmkt.refill(self.game.pstack)
                return self.chain(ev, Handler.HANDLER_REPLACE, nh)

            plant.bid = plant.price
            hnext = HandlerAuction(self.game, plant, self.auctioneer)
            return self.chain(ev, Handler.HANDLER_PUSH, hnext)

        if ev.key == pygame.K_p:
            if self.game.turn == 1:
                nh = HandlerPressEnter(
                    self.game,
                    "You must buy a plant on your first turn"
                )
                return self.chain(ev, Handler.HANDLER_PUSH, nh)

            # If a player passes when he needs to start an auction, he loses
            # the right to participate on auctions this turn
            self.game.players.remove_auction_rights(self.auctioneer)
            nh = HandlerAuctionStart(self.game)
            return self.chain(ev, Handler.HANDLER_REPLACE, nh)

        return self.chain(ev, Handler.HANDLER_NOP)

    def reactivate(self):
        self.game.pmkt.refill(self.game.pstack)
        if self.game.players.auctioneers_left():
            self.game.players.clear_participation_rights()
            nh = HandlerAuctionStart(self.game)
            return self.chain(None, Handler.HANDLER_REPLACE, nh)

        return self.chain(None, Handler.HANDLER_POP)

class HandlerResBuy(Handler):
    def __init__(self, game, buyer, resource):
        super().__init__(game)
        self.buyer = buyer
        self.resource = resource
        self.amount = 0
        self.price = 0
        self.extrastatus = ""
        self.set_statusprompt()

    def __call__(self, ev):
        self.extrastatus = ""

        if ev.key == pygame.K_m:
            self.amount += 1
        elif ev.key == pygame.K_l and self.amount > 0:
            self.amount -= 1
        elif ev.key == pygame.K_o:
            self.game.rmkt[self.resource].buy(self.amount)
            self.game.players.player_buys_resource(self.buyer,
                                                   self.resource,
                                                   self.amount,
                                                   self.price)
            nh = HandlerPressEnter(
                self.game,
                "P{} buys {}[{}] for ${}".format(
                    self.buyer,
                    self.resource.__class__.__name__,
                    self.amount,
                    self.price
                )
            )
            return self.chain(None, Handler.HANDLER_REPLACE, nh)
        else:
            return self.chain(ev, Handler.HANDLER_NOP)

        price = self.game.rmkt[self.resource].buy(self.amount, dry_run=True)
        if price > self.game.players.get_cash(self.buyer):
            self.extrastatus = "No cash left."
            self.amount -= 1
        elif self.game.players.canbuy(self.buyer,
                                      self.resource,
                                      howmuch=self.amount):
            self.price = price
        else:
            self.extrastatus = "Resource quota exceeded"
            self.amount -= 1

        # We rerun the dry_run of the buy to display the correct amount of
        # resources being bought in case we exceeded a limit
        self.game.rmkt[self.resource].buy(self.amount, dry_run=True)
        self.set_statusprompt()
        return self.chain(ev, Handler.HANDLER_NOP)

    def set_statusprompt(self):
        self.status = "P{} is buying {}. {}".format(
            self.buyer,
            self.resource.__class__.__name__,
            self.extrastatus
        )
        self.prompt = "Buying {}[${}].  (o)k (m)ore (l)ess.".format(
            self.amount,
            self.price
        )

class HandlerResBuyStart(Handler):
    def __init__(self, game, buyer=None):
        super().__init__(game)
        if buyer:
            self.buyer = buyer
        else:
            self.buyer = self.game.players.first()

        self.canbuy_c = self.game.players.canbuy(self.buyer, Coal)
        self.canbuy_o = self.game.players.canbuy(self.buyer, Oil)
        self.canbuy_g = self.game.players.canbuy(self.buyer, Garbage)
        self.canbuy_n = self.game.players.canbuy(self.buyer, Nuclear)

        self.status = "Resource acquisition stage started"
        self.prompt = "P{pid}: Buy {c}{o}{g}{n} or (p)ass".format(
            pid=self.buyer,
            c="(c)oal" if self.canbuy_c else "",
            o="(o)il" if self.canbuy_o else "",
            g="(g)arbage" if self.canbuy_g else "",
            n="(n)uclear" if self.canbuy_n else "",
        )

    def __call__(self, ev):
        if ev.key == pygame.K_p:
            buyernext = self.game.players.next(self.buyer)
            if buyernext:
                nh = HandlerResBuyStart(self.game, buyernext)
                return self.chain(None, Handler.HANDLER_REPLACE, nh)
            self.game.next_stage()
            return self.chain(None, Handler.HANDLER_POP)

        if ev.key == pygame.K_c and self.canbuy_c:
            nh = HandlerResBuy(self.game, self.buyer, Coal)
        elif ev.key == pygame.K_o and self.canbuy_o:
            nh = HandlerResBuy(self.game, self.buyer, Oil)
        elif ev.key == pygame.K_g and self.canbuy_g:
            nh = HandlerResBuy(self.game, self.buyer, Garbage)
        elif ev.key == pygame.K_n and self.canbuy_n:
            nh = HandlerResBuy(self.game, self.buyer, Nuclear)
        else:
            return self.chain(ev, Handler.HANDLER_NOP)

        return self.chain(None, Handler.HANDLER_PUSH, nh)

class HandlerCityBuy(Handler):
    def __init__(self, game, buyer=None):
        super().__init__(game)
        if buyer:
            self.buyer = buyer
        else:
            self.buyer = self.game.players.first()

        # "Randomly" pick the first city to be the active city.
        self.active_city = self.game.gmap.first()
        self.game.gmap.set_active_city(self.active_city)
        self.rcities = self.game.gmap.get_reachable_cities(self.active_city)
        self.game.gmap.set_next_city(self.rcities[0])

        self.status = "City acquisition stage started"
        self.set_statusprompt()

    def arrange_reachable_cities(self, n):
        """
        This just rotates the reachable_cities array and updates the game
        status on what is the next city that would be navigated to by the UI.
        That's why we keep next_city on the global state.
        """
        self.rcities = self.rcities[n:] + self.rcities[:n]
        self.game.gmap.set_next_city(self.rcities[0])

    def set_statusprompt(self):
        if len(self.rcities) == 1:
            self.prompt = "Build (b){}, travel (w){} or (p)ass".format(
                self.active_city,
                self.rcities[0],
            )
        else:
            self.prompt = (
                "Select (a){}, (d){}, build (b){}, travel (w){} or (p)ass"
            ).format(
                self.rcities[-1],
                self.rcities[1],
                self.active_city,
                self.rcities[0],
            )

    def __call__(self, ev):
        if ev.key == pygame.K_a and len(self.rcities) > 1:
            self.arrange_reachable_cities(-1)
        elif ev.key == pygame.K_d and len(self.rcities) > 1:
            self.arrange_reachable_cities(1)
        elif ev.key == pygame.K_w:
            self.game.gmap.set_active_to_next()
            self.active_city = self.game.gmap.get_active_city()
            self.rcities = self.game.gmap.get_reachable_cities(self.active_city)
            self.game.gmap.set_next_city(self.rcities[0])
        elif ev.key == pygame.K_b:
            existing_network = self.game.players.get_network(self.buyer)
            price = self.game.gmap.building_cost(self.active_city, existing_network)
            if price == sys.maxsize:
                self.status = "City can't be constructed"
            if price > self.game.players.get_cash(self.buyer):
                self.status = "P{} doesn't have enough cash[${}]".format(
                    self.buyer, price
                )
            else:
                self.status = "P{} pays ${} to construct on {}".format(
                    self.buyer,
                    price,
                    self.active_city.name
                )
                buyer_color = self.game.players.get_color(self.buyer)
                self.game.gmap.build(self.active_city, buyer_color)
                self.game.players.player_buys_city(self.buyer,
                                                   self.active_city.name,
                                                   price)
        elif ev.key == pygame.K_p:
            self.buyer = self.game.players.next(self.buyer)
            if not self.buyer:
                nh = HandlerPressEnter(
                    self.game,
                    "All players done buying cities"
                )
                return self.chain(ev, Handler.HANDLER_REPLACE, nh)

        self.set_statusprompt()
        return self.chain(ev, Handler.HANDLER_NOP)

class HandlerMain(Handler):
    def __init__(self, game):
        super().__init__(game)
        self.set_statusprompt()

    def __call__(self, ev):
        if ev.key == pygame.K_s:
            nh = HandlerAuctionStart(self.game)
            return self.chain(ev, Handler.HANDLER_PUSH, nh)

        return self.chain(ev, Handler.HANDLER_NOP)

    def reactivate(self):
        if self.game.stage == GameStatus.STAGE_AUCTION:
            return super().reactivate()
        elif self.game.stage == GameStatus.STAGE_RESOURCE:
            if self.game.turn == 1:
                self.game.players.recalculate_player_order()
            self.status = "Auction completed!"
            self.prompt = "Press enter to continue"
            nh = HandlerResBuyStart(self.game)
            return self.chain(None, Handler.HANDLER_PUSH, nh)
        elif self.game.stage == GameStatus.STAGE_CITIES:
            nh = HandlerCityBuy(self.game)
            return self.chain(None, Handler.HANDLER_PUSH, nh)

    def set_statusprompt(self):
        self.status = "EnergyNet v0.1 (tip: {})".format(
            self.game.get_random_tip()
        )
        self.prompt = (
            "Press (s) to start a game, (q) to quit at any point or " +
            "(t) for more tips"
        )
