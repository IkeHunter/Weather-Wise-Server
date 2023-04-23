import json
import requests
from enum import Enum, auto

# General enumerator class for types of parameter to be searched


class Parameter(Enum):
    RAIN = auto()
    HOT = auto()
    COLD = auto()
    HUMID = auto()
    SUNR = auto()
    SUNS = auto()


class Comp(Enum):
    GREATER = 0
    LESSER = 1

# days[0]['data'][0]['dt'] This is the syntax to access the dt of the first
#  element in the array


class WeatherHeap:
    # Initialize an empty array
    days = []

    def __init__(self, weather, param: Parameter):
        self.size = len(weather)
        self.param = param

        # This ensures we are actually maintaining a copy of the value
        # and not the original
        for i in range(self.size):
            self.days.append(weather[i])

        # Add in local_sunrise and local_sunset attributes
        for i in range(self.size):
            local_sunrise = self.days[i]['data'][0]['sunrise'] % 86400
            local_sunset = self.days[i]['data'][0]['sunset'] % 86400
            self.days[i]['data'][0]['local_sunrise'] = local_sunrise
            self.days[i]['data'][0]['local_sunset'] = local_sunset

        self.buildHeap(param)

    def buildHeap(self, parameter):
        self.size = len(self.days)
        for i in range(int(self.size / 2), -1, -1):
            self.heapifyDown(parameter, i)

    # Returns the top value and removes it
    def pop(self):
        top = self.days[0]
        # Switch the first and last elements of the list
        self.days[0], self.days[-1] = self.days[-1], self.days[0]
        self.size - 1
        self.heapifyDown(self.param, 0)

        return top

    # Values will be 0-indexed
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
                                        index, 'temp', Comp.GREATER)
            case Parameter.COLD:
                index = self.comparator(float('inf'), left_child, right_child,
                                        index, 'temp', Comp.LESSER)
            case Parameter.SUNR:
                index = self.comparator(0, left_child, right_child,
                                        index, 'local_sunrise', Comp.GREATER)
            case Parameter.SUNS:
                index = self.comparator(86400, left_child, right_child,
                                        index, 'local_sunset', Comp.LESSER)

        if index == i:
            return

        self.days[i], self.days[index] = self.days[index], self.days[i]

        self.heapifyDown(parameter, i)

    # comparator will compare values and return an index of the element that satisfies the conditions given
    # comp will determine if we are checking for a max or min value
    def comparator(self, start, left, right, index, param, comp):

        if param in self.days[index]['data'][0]:
            start = self.days[index]['data'][0][param]

        # Create left and right child to be used later
        left_data = self.days[left]['data'][0]
        right_data = {}
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
            result.append(self.pop())

        self.buildHeap(self.param)
        return result

    # Change the ordering of the current heap
    def orderby(self, comp: Parameter) -> None:

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

    def print(self):
        for i in range(self.size):
            print(self.days[i])


# Testing Purposes
days = [{'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
         'data': [{'dt': 1644062400, 'sunrise': 1644066553, 'sunset': 1644105068, 'temp': 269.44, 'feels_like': 267.09,
                   'pressure': 1035, 'humidity': 83, 'dew_point': 267.26, 'clouds': 0, 'visibility': 10000, 'wind_speed': 1.54,
                   'wind_deg': 240,
                   'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]}]},

        {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
            'data': [{'dt': 1644321600, 'sunrise': 1644325606, 'sunset': 1644364441, 'temp': 274.04, 'feels_like': 272.35,
                      'pressure': 1025, 'humidity': 75, 'dew_point': 270.47, 'clouds': 0, 'visibility': 10000, 'wind_speed': 1.54,
                      'wind_deg': 200,
                      'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]}]},

        {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
            'data': [{'dt': 1643889600, 'sunrise': 1643893845, 'sunset': 1643932152, 'temp': 274.7, 'feels_like': 270.1,
                      'pressure': 1014, 'humidity': 95, 'dew_point': 273.99, 'clouds': 100, 'visibility': 10000, 'wind_speed': 5.14,
                      'wind_deg': 30,
                      'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'rain': {'1h': 1.98}}]},

        {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
            'data': [{'dt': 1644667200, 'sunrise': 1644670990, 'sunset': 1644710268, 'temp': 284.66, 'feels_like': 283.15,
                      'pressure': 1022, 'humidity': 49, 'dew_point': 274.33, 'clouds': 100, 'visibility': 10000, 'wind_speed': 4.63,
                      'wind_deg': 20, 'wind_gust': 7.72,
                      'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'rain': {'1h': 0.21}}]},

        {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
            'data': [{'dt': 1643803200, 'sunrise': 1643807488, 'sunset': 1643845693, 'temp': 287.67, 'feels_like': 287.63,
                      'pressure': 1009, 'humidity': 94, 'dew_point': 286.72, 'clouds': 100, 'visibility': 10000, 'wind_speed': 4.12,
                      'wind_deg': 210,
                      'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}]}]}
        ]


apiKey = '11d1d9e83f342ffd3863eec2bdabe3a8'
date = 1618525688
lat = '33.44'
lon = '-94.04'

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
heap.buildHeap(Parameter.SUNR)
heap.print()
