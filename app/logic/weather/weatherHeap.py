from enum import Enum


# General enumerator class for types of parameter to be searched
class Parameter(Enum):
    RAIN = 0
    HOT = 1
    COLD = 2
    HUMID = 3
    SUNR = 4
    SUNS = 5


class Comp(Enum):
    GREATER = 0
    LESSER = 1

# days[0]['data'][0]['dt'] This is the syntax to access the dt of the first
#  element in the array


class WeatherHeap:
    # Initialize an empty array
    days = []
    size = 0

    def __init__(self, weather):
        self.days = weather
        self.size = len(self.days)

    def buildHeap(self, parameter):
        for i in range(int(self.size / 2), -1, -1):
            self.heapifyDown(parameter, i)

    # Values will be 1-indexed
    def heapifyDown(self, parameter, i):
        # left and right child
        left_child = 2 * i + 1
        right_child = 2 * i + 2

        # Check if leaf
        if left_child >= self.size:
            return

        index = i
        curr_data = self.days[index]['data'][0]

        # Find node with smallest value within context
        match parameter:
            case Parameter.RAIN:
                index = self.comparator(0, left_child, right_child,
                                        index, 'rain', Comp.GREATER)
            case Parameter.HUMID:
                index = self.comparator(0, left_child, right_child,
                                        index, 'humidity', Comp.GREATER)
            case Parameter.HOT:
                index = self.comparator(float('-inf'), left_child, right_child,
                                        index, 'temperature', Comp.GREATER)
            case Parameter.COLD:
                index = self.comparator(float('inf'), left_child, right_child,
                                        index, 'temperature', Comp.LESSER)
            case Parameter.SUNR:
                index = self.comparator(0, left_child, right_child,
                                        index, 'sunrise', Comp.GREATER)
            case Parameter.SUNS:
                index = self.comparator(86400, left_child, right_child,
                                        index, 'sunset', Comp.LESSER)

        if index == i:
            return

        temp = self.days[i]
        self.days[i] = self.days[index]
        self.days[index] = temp

        self.heapifyDown(parameter, i)

    # comparator will compare values and return an index of the element that satisfies the conditions given
    # comp will determine if we are checking for a max or min value
    def comparator(self, start, left, right, index, param, comp):

        if param in self.days[index]['data'][0]:
            start = self.days[index]['data'][0][param]

        # Create left and right child to be used later
        left_data = self.days[left]['data'][0]
        if right < self.size:
            right_data = self.days[right]['data'][0]

        match comp:
            case Comp.GREATER:
                if param in left_data:
                    if start < left_data[param]:
                        start = left_data[param]
                        index = left

                if param in right_data:
                    if start < right_data[param]:
                        index = right
            case Comp.LESSER:
                if param in left_data:
                    if start > left_data[param]:
                        start = left_data[param]
                        index = left

                if param in right_data:
                    if start > right_data[param]:
                        index = right

        return index

    def top(self, number):
        result = []
        for i in range(number):
            result.append(self.days[i])
        return result

    def getKLargest(k):
        tempHeap = WeatherHeap()
        for i in range(k):
            pass

    def insert(self, day):
        self.days.append(day)
        self.size += 1
        self.heapifyUp(self.size - 1)

    def heapifyUp(self, i):
        if (i == 0):
            return
        parent = int((i - 1) / 2)

    def print(self):
        for i in self.days:
            print(i)
