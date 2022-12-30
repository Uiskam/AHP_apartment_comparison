from enum import Enum
from functools import total_ordering

class LayoutStructure(Enum):
    SOURCE_DATA_INPUT = 0
    FLAT_COMPARISON_AMBIENT_NOISE = 1
    FLAT_COMPARISON_AVAILABILITY_OF_SHOPS = 2
    FLAT_COMPARISON_COMMUTE_TO_UNIVERSITY = 3
    FLAT_COMPARISON_DECORATION_LEVEL = 4
    FLAT_COMPARISON_INSOLATION = 5
    FLAT_COMPARISON_PRICE = 6
    FLAT_COMPARISON_PROXIMITY_TO_CITY_CENTER = 7
    FLAT_COMPARISON_ROOMMATE_NUMBER = 8
    FLAT_COMPARISON_SECURITY = 9
    FLAT_COMPARISON_SIZE_OF_THE_FLAT = 10
    FLAT_COMPARISON_SIZE_OF_THE_ROOM = 11
    DATA_CONFIRMATION = 12
    DATA_PROCESSING = 13
    RESULTS = 14

    @total_ordering
    def next(self):
        return LayoutStructure(self.value + 1)

    def previous(self):
        return LayoutStructure(self.value - 1)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, LayoutStructure):
            return self is other
        return False

    def __lt__(self, other):
        if isinstance(other, int):
            return self.value < other

        if isinstance(other, LayoutStructure):
            return self.value < other.value

        return False
