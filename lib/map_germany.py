# pylint: disable=too-many-statements
from lib.map import Map

class MapGermany(Map):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.city("Schwerin", (468, 205))
        self.city("Rostock", (514, 121))
        self.city("Hamburg", (351, 202))
        self.city("Hannover", (350, 362))
        self.city("Bremen", (270, 262))
        self.city("Munchen", (492, 936))
        self.city("Dresden", (671, 548))
        self.city("Passau", (640, 870))
        self.city("Regensburg", (517, 815))
        self.city("Augsburg", (410, 880))
        self.city("Nurnberg", (453, 752))
        self.city("Erfurt", (454, 542))
        self.city("Aachen", (44, 589))
        self.city("Koln", (122, 568))
        self.city("Trier", (77, 710))
        self.city("Wiesbaden", (211, 671))
        self.city("Frankfurt-M", (250, 646))
        self.city("Fulda", (347, 603))
        self.city("Wurzburg", (363, 709))
        self.city("Mannheim", (252, 767))
        self.city("Saarbruken", (146, 788))
        self.city("Stuttgart", (227, 851))
        self.city("Freiburg", (184, 931))
        self.city("Konstanz", (278, 977))
        self.city("Flensburg", (313, 36))
        self.city("Kiel", (355, 101))
        self.city("Lubeck", (415, 146))
        self.city("Torgelow", (662, 201))
        self.city("Berlin", (616, 337))
        self.city("Frankfurt-O", (701, 366))
        self.city("Leizpig", (558, 504))
        self.city("Halle", (510, 474))
        self.city("Magdeburg", (499, 371))
        self.city("Kassel", (311, 504))
        self.city("Dortmund", (177, 486))
        self.city("Dusseldorf", (69, 517))
        self.city("Essen", (107, 458))
        self.city("Duisburg", (56, 439))
        self.city("Munster", (164, 411))
        self.city("Osnabruck", (209, 347))
        self.city("Wilhelmshaven", (204, 201))
        self.city("Cuxhaven", (260, 161))

        self.road("Flensburg", "Kiel", 4)
        self.road("Kiel", "Lubeck", 4)
        self.road("Lubeck", "Hamburg", 6)
        self.road("Hamburg", "Kiel", 8)
        self.road("Hamburg", "Cuxhaven", 11)
        self.road("Cuxhaven", "Bremen", 8)
        self.road("Bremen", "Wilhelmshaven", 11)
        self.road("Wilhelmshaven", "Osnabruck", 14)
        self.road("Osnabruck", "Bremen", 11)
        self.road("Bremen", "Hamburg", 11)
        self.road("Osnabruck", "Hannover", 16)
        self.road("Hannover", "Hamburg", 17)
        self.road("Hannover", "Schwerin", 19)
        self.road("Schwerin", "Lubeck", 6)
        self.road("Schwerin", "Hamburg", 8)
        self.road("Hannover", "Bremen", 10)
        self.road("Rostock", "Torgelow", 19)
        self.road("Rostock", "Schwerin", 6)
        self.road("Torgelow", "Berlin", 15)
        self.road("Torgelow", "Schwerin", 19)
        self.road("Schwerin", "Berlin", 18)
        self.road("Berlin", "Frankfurt-O", 6)
        self.road("Berlin", "Magdeburg", 10)
        self.road("Berlin", "Halle", 17)
        self.road("Magdeburg", "Halle", 11)
        self.road("Frankfurt-O", "Leizpig", 21)
        self.road("Halle", "Leizpig", 0)
        self.road("Frankfurt-O", "Dresden", 16)
        self.road("Osnabruck", "Munster", 7)
        self.road("Munster", "Essen", 6)
        self.road("Essen", "Duisburg", 0)
        self.road("Essen", "Dusseldorf", 2)
        self.road("Dortmund", "Munster", 2)
        self.road("Dusseldorf", "Koln", 4)
        self.road("Essen", "Dortmund", 4)
        self.road("Koln", "Dortmund", 10)
        self.road("Kassel", "Erfurt", 15)
        self.road("Kassel", "Hannover", 15)
        self.road("Kassel", "Dortmund", 18)
        self.road("Kassel", "Osnabruck", 20)
        self.road("Kassel", "Fulda", 8)
        self.road("Kassel", "Frankfurt-M", 13)
        self.road("Hannover", "Magdeburg", 15)
        self.road("Magdeburg", "Schwerin", 16)
        self.road("Aachen", "Dusseldorf", 9)
        self.road("Aachen", "Koln", 7)
        self.road("Aachen", "Trier", 19)
        self.road("Dortmund", "Frankfurt-M", 20)
        self.road("Frankfurt-M", "Wiesbaden", 0)
        self.road("Wiesbaden", "Koln", 21)
        self.road("Trier", "Koln", 20)
        self.road("Trier", "Wiesbaden", 18)
        self.road("Frankfurt-M", "Wurzburg", 13)
        self.road("Frankfurt-M", "Fulda", 8)
        self.road("Erfurt", "Hannover", 19)
        self.road("Erfurt", "Halle", 6)
        self.road("Erfurt", "Dresden", 19)
        self.road("Leizpig", "Dresden", 13)
        self.road("Erfurt", "Nurnberg", 21)
        self.road("Nurnberg", "Wurzburg", 8)
        self.road("Fulda", "Wurzburg", 11)
        self.road("Fulda", "Erfurt", 13)
        self.road("Trier", "Saarbruken", 11)
        self.road("Saarbruken", "Wiesbaden", 10)
        self.road("Saarbruken", "Mannheim", 11)
        self.road("Saarbruken", "Stuttgart", 17)
        self.road("Mannheim", "Wiesbaden", 11)
        self.road("Mannheim", "Wurzburg", 10)
        self.road("Mannheim", "Stuttgart", 6)
        self.road("Wurzburg", "Stuttgart", 12)
        self.road("Wurzburg", "Augsburg", 19)
        self.road("Augsburg", "Stuttgart", 15)
        self.road("Augsburg", "Regensburg", 13)
        self.road("Augsburg", "Nurnberg", 18)
        self.road("Nurnberg", "Regensburg", 12)
        self.road("Passau", "Regensburg", 12)
        self.road("Passau", "Munchen", 14)
        self.road("Munchen", "Regensburg", 10)
        self.road("Munchen", "Augsburg", 6)
        self.road("Freiburg", "Stuttgart", 16)
        self.road("Freiburg", "Konstanz", 14)
        self.road("Konstanz", "Augsburg", 17)
        self.road("Konstanz", "Stuttgart", 16)
