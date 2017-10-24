#!/usr/bin/env python3
import sys
import time
import math
import pygame

from lib.game_status import GameStatus
from lib.map_germany import MapGermany
from lib.resmarket import ResourcesMarket
from lib.ppstack import PowerPlantStack
from lib.ppmarket import PowerPlantMarket
from lib.handler import Handler, HandlerMain
from lib.player import PlayerList
from lib.resources import Coal, Oil, Garbage, Nuclear
from lib.util import sin_variate, split_line
from lib.preprogrammed import PreProgrammedCommands

def draw_city(display, font, city, labels=True, active=False):
    color_a = (0, 0, 255)
    color_b = (0, 255, 0)
    color_c = (255, 0, 0)
    rect = pygame.Rect(city.pos[0] - 8, city.pos[1] - 8, 16, 16)
    pygame.draw.arc(display, color_a, rect, 0, 2*math.pi/3, 6)
    pygame.draw.arc(display, color_b, rect, 2*math.pi/3, 4*math.pi/3, 6)
    pygame.draw.arc(display, color_c, rect, 4*math.pi/3, 0, 6)

    if labels or active:
        g_comp = sin_variate(0, 255, 2000) if active else 255
        label_pos = (city.pos[0] - 10, city.pos[1] + 10)
        display.blit(font.render(city.name, 1, (255, g_comp, 0)), label_pos)

def draw_road(display, game, road):
    if road.cost <= 10:
        color = (206, 127, 50)
    elif road.cost <= 15:
        color = (192, 192, 192)
    else:
        color = (255, 215, 0)

    if road.cost == 0:
        width = 5
    else:
        width = 3

    highlight = False
    if game.gmap.active_city is not None:
        active_vcity = game.gmap.vlist[game.gmap.active_city]
        next_vcity = game.gmap.vlist[game.gmap.next_city]
        if active_vcity.name == road.fro.name and next_vcity.name != road.to.name:
            highlight = True
            (fro, to) = (road.fro, road.to)
        elif active_vcity.name == road.to.name and next_vcity.name != road.fro.name:
            highlight = True
            (fro, to) = (road.to, road.fro)

    if highlight:
        for l in split_line(fro.pos, to.pos):
            pygame.draw.line(display, color, l[0], l[1], width)
    else:
        pygame.draw.line(display, color, road.fro.pos, road.to.pos, width)

def draw_road_costs(display, font, road):
    if road.cost == 0:
        return

    label = font.render(str(road.cost), 1, (255, 255, 0))
    midpoint = (
        (road.fro.pos[0] + road.to.pos[0]) / 2,
        (road.fro.pos[1] + road.to.pos[1]) / 2
    )
    label_pos = (
        midpoint[0] - label.get_width() / 2,
        midpoint[1] - label.get_height() / 2
    )

    pygame.draw.rect(display, (0, 0, 255), (label_pos, label.get_size()))
    display.blit(label, label_pos)

def draw_resmarket(display, font, rmkt):
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    def draw_resource(resource, rect):
        # Keep track of how many resources is the player trying to buy
        if rmkt[resource].attempted_buy > drawn_amount[resource]:
            width = 3
        else:
            width = 0

        drawn_amount[resource] += 1
        pygame.draw.rect(display, rescolor[resource], rect, width)

    (cmkt, omkt) = (rmkt[Coal], rmkt[Oil])
    (gmkt, nmkt) = (rmkt[Garbage], rmkt[Nuclear])
    framecolor = (255, 255, 255)
    yoffset = 12

    rescolor = {
        Coal: (162, 82, 42),
        Oil: (64, 64, 64),
        Garbage: (255, 255, 0),
        Nuclear: (255, 0, 0)
    }
    drawn_amount = {
        Coal: 0,
        Oil: 0,
        Garbage: 0,
        Nuclear: 0,
    }

    pygame.draw.rect(display, (0, 0, 0), [1024 + 48, 12, 72, 768])
    for i in range(1, 9):
        xoffset = 1024 + 48
        pygame.draw.rect(display, framecolor, [xoffset, yoffset, 72, 72], 1)
        if cmkt.market[i] == 3:
            draw_resource(Coal, [xoffset, yoffset, 22, 22])
        if cmkt.market[i] >= 2:
            draw_resource(Coal, [xoffset, yoffset + 25, 22, 22])
        if cmkt.market[i] >= 1:
            draw_resource(Coal, [xoffset, yoffset + 50, 22, 22])

        display.blit(font.render(str(i), 1, (255, 255, 0)), (xoffset, yoffset))
        xoffset += 22 + 3
        if omkt.market[i] == 3:
            draw_resource(Oil, [xoffset, yoffset, 22, 16])
        if omkt.market[i] >= 2:
            draw_resource(Oil, [xoffset, yoffset + 18, 22, 16])
        if omkt.market[i] >= 1:
            draw_resource(Oil, [xoffset, yoffset + 36, 22, 16])

        if nmkt.market[i] == 1:
            draw_resource(Nuclear, [xoffset, yoffset + 54, 22, 18])

        xoffset += 22 + 3
        if gmkt.market[i] == 3:
            draw_resource(Garbage, [xoffset, yoffset, 22, 22])
        if gmkt.market[i] >= 2:
            draw_resource(Garbage, [xoffset, yoffset + 25, 22, 22])
        if gmkt.market[i] >= 1:
            draw_resource(Garbage, [xoffset, yoffset + 50, 22, 22])
        yoffset += 72 + 12

    xoffset = 1024 + 48
    pygame.draw.rect(display, framecolor, [xoffset, yoffset, 72, 72], 1)
    if nmkt.market[10] == 1:
        draw_resource(Nuclear, [xoffset, yoffset, 30, 30])
        cost_label = font.render(str(10), 1, (255, 255, 0))
        display.blit(cost_label, (xoffset, yoffset))
    if nmkt.market[12] == 1:
        draw_resource(Nuclear, [xoffset + 42, yoffset, 30, 30])
        cost_label = font.render(str(12), 1, (255, 255, 0))
        display.blit(cost_label, (xoffset + 42, yoffset))
    if nmkt.market[14] == 1:
        draw_resource(Nuclear, [xoffset, yoffset + 42, 30, 30])
        cost_label = font.render(str(14), 1, (255, 255, 0))
        display.blit(cost_label, (xoffset, yoffset + 42))
    if nmkt.market[16] == 1:
        draw_resource(Nuclear, [xoffset + 42, yoffset + 42, 30, 30])
        cost_label = font.render(str(16), 1, (255, 255, 0))
        display.blit(cost_label, (xoffset + 42, yoffset + 42))

def draw_ppmarket(display, font, ppmkt):
    yoffset = 12
    xoffset = 1024 + 48 + 72 + 12
    framecolor = (255, 255, 255)

    pygame.draw.rect(display, (0, 0, 0), (xoffset, yoffset, 156, 324))

    def draw_plant(xoff, yoff, active=False):
        rect = [xoff, yoff, 72, 72]
        if active:
            sinusoidal = sin_variate(0, 255, 2000)
            label_color = (255, sinusoidal, 0)
        else:
            label_color = (255, 255, 0)
        label_top = font.render(str(pplant), 1, label_color)
        label_bot = font.render(pplant.production_str(), 1, label_color)
        pygame.draw.rect(display, framecolor, rect, 1)

        label_top_xoffset = xoff + 36 - label_top.get_width() / 2
        display.blit(label_top, (label_top_xoffset, yoff))
        label_bot_xoffset = xoff + 36 - label_bot.get_width() / 2
        display.blit(label_bot, (label_bot_xoffset, yoff + 36))

    (in_auction, pindex) = ppmkt.in_auction
    for (n, pplant) in enumerate(ppmkt.actual):
        active = in_auction and pindex == n
        draw_plant(xoffset, yoffset + 84 * n, active=active)
    for (n, pplant) in enumerate(ppmkt.future):
        draw_plant(xoffset + 84, yoffset + 84 * n)

def draw_players(display, font, players):
    yoff = (12 + 72) * 4 + 12
    xoff = 1024 + 48 + 72 + 12

    label_color = (255, 255, 255)
    for p in players.list:
        l = font.render(str(p), 1, label_color)
        lh = l.get_height()
        lw = l.get_width()
        pygame.draw.rect(display, (0, 0, 0), ((xoff, yoff), (1366, lh)))
        if p.active:
            pygame.draw.rect(display, (255, 0, 0), ((xoff, yoff), (lw, lh)))
        display.blit(l, (xoff, yoff))
        yoff += l.get_height()

def draw_map(display, font, game):
    pygame.draw.rect(display, (0, 0, 0), (0, 0, 1024 + 48, 768))
    for groad in game.gmap.elist:
        draw_road(display, game, groad)
        if game.road_costs_visible:
            draw_road_costs(display, font, groad)
    for (n, gcity) in enumerate(game.gmap.vlist):
        active = (n == game.gmap.active_city)
        draw_city(display, font, gcity, game.city_labels_visible, active=active)

def draw_fps(display, font, game):
    update = time.time()
    diff = update - game.last_update
    fps = 1 / diff

    #if int(update) != int(game.last_update):
    l = font.render("{:.2f}".format(fps), 1, (255, 255, 0))
    pygame.draw.rect(display, (0, 0, 0), ((0, 0), l.get_size()))
    display.blit(l, (0, 0))

    game.last_update = update

class ConsoleWidget:
    def __init__(self, display, font, position):
        self.display = display
        self.font = font
        self.pos = position
        self.label_size = None

    def clear(self):
        if self.label_size:
            pygame.draw.rect(self.display, (0, 0, 0), (self.pos, self.label_size))

    def draw(self, buf):
        self.clear()
        label = self.font.render(buf, 1, (255, 255, 0))
        self.display.blit(label, self.pos)
        self.label_size = label.get_size()

def main():
    pstack = PowerPlantStack(stage3_cb=None)
    game = GameStatus(
        gmap=MapGermany((1024, 768), translated=(-30, 0), transposed=True),
        rmkt=ResourcesMarket(),
        pmkt=PowerPlantMarket(pstack),
        pstack=pstack,
        players=PlayerList(3)
    )
    pygame.init()
    display = pygame.display.set_mode((1366, 768), pygame.NOFRAME)
    font = pygame.font.SysFont("monospace", 16)

    # handler_stack is a stack that keeps the context nesting in the cli.  If
    # the handler returns False, it get popped.
    main_handler = HandlerMain(game)
    main_handler.post()
    handler_stack = [main_handler]
    prompt_widget = ConsoleWidget(display, font, (16, 736))
    status_widget = ConsoleWidget(display, font, (16, 720))

    current_handler = handler_stack[-1]
    status_widget.draw(current_handler.status)
    prompt_widget.draw(current_handler.prompt)

    preprogrammed = PreProgrammedCommands(sys.argv)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.NOEVENT:
            preprogrammed.run()

            # Draw animations here, no game state change.
            draw_map(display, font, game)
            draw_fps(display, font, game)
            status_widget.draw(current_handler.status)
            prompt_widget.draw(current_handler.prompt)

            draw_resmarket(display, font, game.rmkt)
            draw_ppmarket(display, font, game.pmkt)
            draw_players(display, font, game.players)
            pygame.display.update()

            continue

        current_handler = handler_stack[-1]

        if event.type == pygame.USEREVENT:
            (stack_op, new) = current_handler.reactivate()
        elif event.type == pygame.KEYDOWN:
            (stack_op, new) = current_handler(event)
        else:
            # Don't update anything if the event is not recognized
            continue

        print("{} {:>32} {}".format(stack_op, str(new), handler_stack))
        if stack_op == Handler.HANDLER_PUSH:
            assert new != None
            handler_stack.append(new)
        elif stack_op == Handler.HANDLER_POP:
            handler_stack.pop()
            current_handler.post()
        elif stack_op == Handler.HANDLER_REPLACE:
            assert new != None
            handler_stack.pop()
            handler_stack.append(new)

        current_handler = handler_stack[-1]

if __name__ == "__main__":
    main()
