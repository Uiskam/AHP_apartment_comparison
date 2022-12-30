from enum import Enum
from functools import total_ordering

class LayoutStructure(Enum):
    #SOURCE_DATA_INPUT = 0
    FLAT_COMPARISON_AMBIENT_NOISE = 0
    FLAT_COMPARISON_AVAILABILITY_OF_SHOPS = 1
    FLAT_COMPARISON_COMMUTE_TO_UNIVERSITY = 2
    FLAT_COMPARISON_DECORATION_LEVEL = 3
    FLAT_COMPARISON_INSOLATION = 4
    FLAT_COMPARISON_PRICE = 5
    FLAT_COMPARISON_PROXIMITY_TO_CITY_CENTER = 6
    FLAT_COMPARISON_ROOMMATE_NUMBER = 7
    FLAT_COMPARISON_SECURITY = 8
    FLAT_COMPARISON_SIZE_OF_THE_FLAT = 9
    FLAT_COMPARISON_SIZE_OF_THE_ROOM = 10
    DATA_CONFIRMATION = 11
    DATA_PROCESSING = 12
    RESULTS = 13

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
