from enum import Enum
from functools import total_ordering


class LayoutStructure(Enum):
    # SOURCE_DATA_INPUT = 0
    LOCATION_PREFERENCE_PRIORITY = 0
    STANDARD_PREFERENCE_PRIORITY = 1
    ALL_PREFERENCE_PRIORITY = 2
    FLAT_COMPARISON_AMBIENT_NOISE = 3
    FLAT_COMPARISON_AVAILABILITY_OF_SHOPS = 4
    FLAT_COMPARISON_COMMUTE_TO_UNIVERSITY = 5
    FLAT_COMPARISON_DECORATION_LEVEL = 6
    FLAT_COMPARISON_INSOLATION = 7
    FLAT_COMPARISON_PRICE = 8
    FLAT_COMPARISON_PROXIMITY_TO_CITY_CENTER = 9
    FLAT_COMPARISON_ROOMMATE_NUMBER = 10
    FLAT_COMPARISON_SECURITY = 11
    FLAT_COMPARISON_SIZE_OF_THE_FLAT = 12
    FLAT_COMPARISON_SIZE_OF_THE_ROOM = 13
    DATA_CONFIRMATION = 14
    DATA_PROCESSING = 15
    RESULTS = 16

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
