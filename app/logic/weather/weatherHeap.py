import json
from enum import Enum, auto

# General enumerator class for types of parameter to be searched


class Parameter(Enum):
    POP = auto()
    RAIN_LEVEL = auto()
    HOT = auto()
    COLD = auto()
    HUMID = auto()
    SUNR = auto()
    SUNS = auto()
    PRESS = auto()
    W_SPEED = auto()


class Comp(Enum):
    GREATER = 0
    LESSER = 1

# days[i] This is the syntax to access the data of the first


class WeatherHeap:
    # Initialize an empty array
    days = []
    param: Parameter
    size: int

    def __init__(self) -> None:
        pass

    def _reset(self) -> None:
        self.days.clear()
        self.size = None
        self.param = None

    # Called by frontend, given a list of days create a heap
    def create(self, yearDays, param: Parameter) -> None:
        self.rebuildHeap(yearDays, param)

    # Called by frontend, returns the top value at current heap
    def find(self, number: int) -> json:
        return json.dumps(self.top(number))

    # Order the heap by specified parameter
    def orderHeap(self, parameter: Parameter) -> None:
        self.size = len(self.days)
        self.param = parameter
        for i in range(int(self.size / 2), -1, -1):
            self.heapifyDown(parameter, i)

    # Returns the top value and removes it
    def pop(self):
        top = self.days[0]
        # Switch the first and last elements of the list
        self.days[0], self.days[-1] = self.days[-1], self.days[0]
        self.size = self.size - 1
        self.heapifyDown(self.param, 0)

        return top

    # Values will be 0-indexed, organizes the element at index i by the parameter type
    def heapifyDown(self, parameter: Parameter, i: int) -> None:
        # left and right child
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        # Check if leaf
        if left_child >= self.size:
            return

        index = i

        # Find node with smallest value within context
        match parameter:
            case Parameter.RAIN_LEVEL:
                index = self.comparator(0, left_child, right_child,
                                        index, 'rain_level', Comp.GREATER)
            case Parameter.HUMID:
                index = self.comparator(0, left_child, right_child,
                                        index, 'humidity', Comp.GREATER)
            case Parameter.HOT:
                index = self.comparator(float('-inf'), left_child, right_child,
                                        index, "average_temp", Comp.GREATER)
            case Parameter.COLD:
                index = self.comparator(float('inf'), left_child, right_child,
                                        index, "average_temp", Comp.LESSER)
            case Parameter.SUNR:
                index = self.comparator(0, left_child, right_child,
                                        index, 'sunrise', Comp.GREATER)
            case Parameter.SUNS:
                index = self.comparator(86400, left_child, right_child,
                                        index, 'sunset', Comp.LESSER)

        if index is i:
            return

        self.days[i], self.days[index] = self.days[index], self.days[i]

        self.heapifyDown(parameter, index)

    # Compare values and returns an index of the element that satisfies the conditions given
    # comp will determine if we are checking for a max or min value
    def comparator(self, start, left: int, right: int, index: int, param: str, comp: Comp) -> int:

        if param in self.days[index]:
            start = self.days[index][param]

        # Create left and right child to be used later
        left_data = self.days[left]
        right_data = {}
        if right < self.size:
            right_data = self.days[right]

        match comp:
            case Comp.GREATER:
                if param in left_data:
                    if self.param is Parameter.SUNR:
                        if start < left_data[param] % 86400:
                            start = left_data[param] % 86400
                            index = left
                    if left_data[param] > start:
                        start = left_data[param]
                        index = left

                if right < self.size and param in right_data:
                    if self.param is Parameter.SUNR:
                        if start < right_data[param] % 86400:
                            start = right_data[param] % 86400
                            index = right
                    if right_data[param] > start:
                        index = right

            case Comp.LESSER:
                if param in left_data:
                    if self.param is Parameter.SUNS:
                        if start > left_data[param] % 86400:
                            start = left_data[param] % 86400
                            index = left
                    if start > left_data[param]:
                        start = left_data[param]
                        index = left

                if right < self.size and param in right_data:
                    if param is Parameter.SUNS:
                        if start > right_data[param] % 86400:
                            start = right_data[param] % 86400
                            index = right
                    if start > right_data[param]:
                        index = right

        return index

    def top(self, number: int) -> list:
        result = []
        for _ in range(number):
            result.append(self.pop())

        self.orderHeap(self.param)
        return result

    def print(self) -> None:
        for i in range(self.size):
            print(self.days[i]['date'])

    # Only use if the location has changed
    # Destroys current heap and creates new heap
    def rebuildHeap(self, weather, param: Parameter) -> None:
        self._reset()
        self.size = len(weather)
        self.param = param

        # This ensures we are actually maintaining a copy of the value
        # and not the original
        for i in range(self.size):
            self.days.append(weather[i])

        self.orderHeap(param)
