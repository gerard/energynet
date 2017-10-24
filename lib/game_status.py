import random

class GameStatus:   # pylint: disable=too-many-instance-attributes
    """
    Not more than a struct to share the game state
    """
    STAGE_AUCTION = 1
    STAGE_RESOURCE = 2
    STAGE_CITIES = 3

    def __init__(self, **kwargs):
        self.rmkt = kwargs.get("rmkt", None)
        self.pmkt = kwargs.get("pmkt", None)
        self.gmap = kwargs.get("gmap", None)
        self.players = kwargs.get("players", None)
        self.pstack = kwargs.get("pstack", None)
        self.road_costs_visible = False
        self.city_labels_visible = True
        self.last_update = 0

        self.stage = GameStatus.STAGE_AUCTION
        self.turn = 1
        self.step = 1

        self.tip_count = 0
        self.tips = [
            "Press F1 to toggle the connection costs",
            "Press F2 to toggle the city labels",
            "Press F10 for a random tip at any time during the game",
            "Pass a sequence of keystrokes as arguments to script the game",
        ]

        random.shuffle(self.tips)

    def next_stage(self):
        self.stage += 1

    def toggle_city_labels(self):
        self.city_labels_visible = not self.city_labels_visible
        return self.city_labels_visible

    def toggle_road_costs(self):
        self.road_costs_visible = not self.road_costs_visible
        return self.road_costs_visible

    def get_random_tip(self):
        self.tip_count += 1
        return self.tips[self.tip_count % len(self.tips)]
