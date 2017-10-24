import random
from lib.pplant import CoalPlant, OilPlant, HybridPlant
from lib.pplant import GarbagePlant, NuclearPlant, GreenPlant

class PowerPlantStackBase:
    class Stage3:
        def __init__(self):
            pass

    def __init__(self, s, stage3_cb):
        """
        The game rules state that the first 9 plants in the stack are
        predetermined, which includes the 8 initial plants on the market and
        the first draw.
        """
        shuffled_stack = s[9:]
        random.shuffle(shuffled_stack)
        self.stack = s[:9] + shuffled_stack
        self.stack.append(PowerPlantStackBase.Stage3())
        self.stage3_cb = stage3_cb

    def add_stage3(self):
        self.stack.append(PowerPlantStackBase.Stage3)

    def draw(self):
        draw = self.stack.pop(0)
        if isinstance(draw, PowerPlantStackBase.Stage3):
            self.stage3_cb()
            draw = self.stack.pop(0)
        return draw

    def addback(self, plant):
        self.stack.append(plant)

class PowerPlantStack(PowerPlantStackBase):
    DEFAULT_STACK = [
        OilPlant(3, 2, 1),
        CoalPlant(4, 2, 1),
        HybridPlant(5, 2, 1),
        GarbagePlant(6, 1, 1),
        OilPlant(7, 2, 2),
        CoalPlant(8, 3, 2),
        OilPlant(9, 1, 1),
        CoalPlant(10, 2, 2),
        GreenPlant(13, 0, 1),
        NuclearPlant(11, 1, 2),
        HybridPlant(12, 2, 2),
        GarbagePlant(14, 2, 2),
        CoalPlant(15, 2, 3),
        OilPlant(16, 2, 3),
        NuclearPlant(17, 1, 2),
        GreenPlant(18, 0, 2),
        GarbagePlant(19, 2, 3),
        CoalPlant(20, 3, 5),
        HybridPlant(21, 2, 4),
        GreenPlant(22, 0, 2),
        NuclearPlant(23, 1, 3),
        GarbagePlant(24, 2, 4),
        CoalPlant(25, 2, 5),
        OilPlant(26, 2, 5),
        GreenPlant(27, 0, 3),
        NuclearPlant(28, 1, 4),
        HybridPlant(29, 1, 4),
        GarbagePlant(30, 3, 6),
        CoalPlant(31, 3, 6),
        OilPlant(32, 3, 6),
        GreenPlant(33, 0, 4),
        NuclearPlant(34, 1, 5),
        OilPlant(35, 1, 5),
        CoalPlant(36, 3, 7),
        GreenPlant(37, 0, 4),
        GarbagePlant(38, 3, 7),
        NuclearPlant(39, 1, 6),
        OilPlant(40, 2, 6),
        CoalPlant(42, 2, 6),
        GreenPlant(44, 0, 6),
        HybridPlant(46, 3, 7),
        GreenPlant(50, 0, 6),
    ]

    def __init__(self, stage3_cb):
        super().__init__(PowerPlantStack.DEFAULT_STACK, stage3_cb)
