# Remember to pip install requests if you are getting an error for import requests
import requests
import json
from weatherHeap import Parameter, WeatherHeap


class mainTest:
    def __init__(self):
        print("test init")

    def test():
        print("module import works")
        return True

# Isaac will create the server

# Kevin and Khai will work on logic and data structures

# Connect API


def get_date(element):
    return element['data'][0]


def main():
    # main.py works
    print("weather works")

    apiKey = '11d1d9e83f342ffd3863eec2bdabe3a8'
    date = 1618525688
    lat = '33.44'
    lon = '-94.04'

    # Checking if API call works
    # url = 'https://api.openweathermap.org/data/3.0/onecall?lat=' + \
    #    lat + '&lon=' + lon + '&appid=' + apiKey

    # https: // api.openweathermap.org/data/3.0/onecall/timemachine?lat = 39.099724 & lon = -94.578331 & dt = 1643803200 & appid = {API key}
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

    for i in range(50):
        # The next day is date + 86400
        date += 86400
        url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=' + \
            lat + '&lon=' + lon + '&dt=' + str(date) + '&appid=' + apiKey
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        weatherDict = json.loads(response.text)
        sunrise = weatherDict['data'][0]['sunrise'] % 86400
        sunset = weatherDict['data'][0]['sunset'] % 86400
        weatherDict['data'][0]['sunrise'] = sunrise
        weatherDict['data'][0]['sunset'] = sunset
        days.append(weatherDict)

    heap = WeatherHeap(days)
    heap.print()
    heap.buildHeap(Parameter.HUMID)
    print("\nSORTED BY HUMIDITY\n")
    heap.print()

    print("\n Top 1 Day\n")
    print(heap.top(1))


if __name__ == "__main__":
    main()
