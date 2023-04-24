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

    def __init__(self, weather, param: Parameter) -> None:
        self.size = len(weather)
        self.param = param

        # This ensures we are actually maintaining a copy of the value
        # and not the original
        for i in range(self.size):
            self.days.append(weather[i])

        self.orderHeap(param)

    def _reset(self) -> None:
        self.days.clear()
        self.size = None
        self.param = None

    # Called by frontend, given a list of days create a heap
    def create(self, param: Parameter, yearDays=[]) -> None:
        self.rebuildHeap(param, yearDays)

    # Called by frontend, returns the top value at current heap
    def find(self) -> json:
        return json.dumps(self.top())

        # Order the heap by specified parameter
    def orderHeap(self, parameter: Parameter) -> None:
        self.size = len(self.days)
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
        curr_data = self.days[index]

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
                                        index, 'average_temp', Comp.GREATER)
            case Parameter.COLD:
                index = self.comparator(float('inf'), left_child, right_child,
                                        index, 'average_temp', Comp.LESSER)
            case Parameter.SUNR:
                index = self.comparator(0, left_child, right_child,
                                        index, 'sunrise', Comp.GREATER)
            case Parameter.SUNS:
                index = self.comparator(86400, left_child, right_child,
                                        index, 'sunset', Comp.LESSER)

        if index == i:
            return

        self.days[i], self.days[index] = self.days[index], self.days[i]

        self.heapifyDown(parameter, i)

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
                    if param is Parameter.SUNR:
                        if start < left_data[param] % 86400:
                            start = left_data[param] % 86400
                            index = left
                    elif start < left_data[param]:
                        start = left_data[param]
                        index = left

                if param in right_data:
                    if param is Parameter.SUNR:
                        if start < right_data[param] % 86400:
                            start = right_data[param] % 86400
                            index = right
                    elif start < right_data[param]:
                        index = right
            case Comp.LESSER:
                if param in left_data:
                    if param is Parameter.SUNS:
                        if start > left_data[param] % 86400:
                            start = left_data[param] % 86400
                            index = left
                    elif start > left_data[param]:
                        start = left_data[param]
                        index = left

                if param in right_data:
                    if param is Parameter.SUNS:
                        if start > right_data[param] % 86400:
                            start = right_data[param] % 86400
                            index = right
                    elif start > right_data[param]:
                        index = right

        return index

    def top(self, number: int) -> list:
        result = []
        for i in range(number):
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
        self.__init__(weather, param)

    # def getKLargest(k):
    #     tempHeap = WeatherHeap()
    #     for i in range(k):
    #         pass

    # def insert(self, day):
    #     self.days.append(day)
    #     self.size += 1
    #     self.heapifyUp(self.size - 1)

    # def heapifyUp(self, i):
    #     if (i == 0):
    #         return
    #     parent = int((i - 1) / 2)


# # Testing Purposes

days = [{'id': 3, 'widget_title': 'top_result', 'date': 1578384000, 'location_id': 2, 'average_temp': 10, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 4, 'widget_title': 'top_result', 'date': 1578384000, 'location_id': 2, 'average_temp': 10, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 40, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 13, 'widget_title': 'top_result', 'date': 1679609699, 'location_id': 2, 'average_temp': 10, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 14, 'widget_title': 'search_results', 'date': 1677194099, 'location_id': 2, 'average_temp': 10, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 15, 'widget_title': 'search_results', 'date': 1674515699, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 16, 'widget_title': 'search_results', 'date': 1697494499, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {
    'id': 17, 'widget_title': 'search_results', 'date': 1697321699, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 18, 'widget_title': 'search_results', 'date': 1694729699, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 19, 'widget_title': 'search_results', 'date': 1692051299, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 20, 'widget_title': 'search_results', 'date': 1689372899, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 21, 'widget_title': 'search_results', 'date': 1686780899, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}, {'id': 22, 'widget_title': 'search_results', 'date': 1684102499, 'location_id': 2, 'average_temp': 0, 'feels_like': 1, 'pressure': 2, 'humidity': 3, 'wind_speed': 4, 'pop': 5, 'rain_levels': 6, 'sunrise': 1684059299, 'sunset': 1684106099, 'weather_name': 'Rain', 'icon': '10n'}]
#
#
# apiKey = '11d1d9e83f342ffd3863eec2bdabe3a8'
# date = 1618525688
# lat = '33.44'
# lon = '-94.04'

# Checking if API call works
# url = 'https://api.openweathermap.org/data/3.0/onecall?lat=' + \
#    lat + '&lon=' + lon + '&appid=' + apiKey
# https: // api.openweathermap.org/data/3.0/onecall/timemachine?lat = 39.099724 & lon = -94.578331 & dt = 1643803200 & appid = {API key}

# days = []
# for i in range(50):
#     # The next day is date + 86400
#     date += 86400
#     url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=' + \
#         lat + '&lon=' + lon + '&dt=' + str(date) + '&appid=' + apiKey
#     payload = {}
#     headers = {}
#     response = requests.request("GET", url, headers=headers, data=payload)
#     weatherDict = json.loads(response.text)
#     sunrise = weatherDict['data'][0]['sunrise'] % 86400
#     sunset = weatherDict['data'][0]['sunset'] % 86400
#     weatherDict['data'][0]['sunrise'] = sunrise
#     weatherDict['data'][0]['sunset'] = sunset
#     days.append(weatherDict)

heap = WeatherHeap(days, Parameter.SUNR)
print("\nSORTED BY LOCAL SUNRISE\n")
heap.print()

print("\n Top 5 Day\n")
print(heap.top(5))

print("\n Reset Heap \n")
heap.orderHeap(Parameter.HOT)
heap.print()
