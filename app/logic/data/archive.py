import environ
import json
from logic.models import Page, Conditions, Forecast, ForecastTable, ForecastRow
# from logic.data import 'gainesville.json'
import importlib.resources

env = environ.Env()
environ.Env.read_env()

class Archive:
    def __init__(self):
        self.global_start = 283996800  # 1/1/1979
        self.global_end = 1682290800  # 4/23/2023
        self.skip = 4*3600 # 4 hours, sets data to 13:00 ET same day

    def _fetch_all_days(self):
        pass

    def _convert_raw_day(self, data: dict):
        # result = []
        try:
            day = {
                "widget_title": "search_result",
                "date": int(data["dt"]),
                "average_temp": int(data["main"]["temp"]),
                "feels_like": int(data["main"]["feels_like"]),
                "pressure": int(data["main"]["pressure"]),
                "humidity": int(data["main"]["humidity"]),
                "wind_speed": int(data["wind"]["speed"]),
                "pop": 0,
                "rain_levels": 0 if not "rain" in data else (int(data["rain"][list(data["rain"].keys())[0]])),
                "sunrise": 0,
                "sunset": 0,
                "weather_name": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"],
            }
            return day
            # result.append(day)
        except:
            print("Error converting day, skipping...")
            return {}

    def _get_all_days(self, limit: int = 1000):
        with importlib.resources.open_text('logic.data', 'gainesville.json') as file:
            data = json.load(file)
            result = []
            for i in range(len(data)-1-self.skip, len(data)-limit, -1):
                if(i % 24 == 0):
                    if self._convert_raw_day(data[i]):
                        result.append(self._convert_raw_day(data[i]))
                    else:
                        pass
            return result

    def get_time_period(self, start: int, end: int, limit: int = 8000):
        start = int(start)
        end = int(end)
        start_index = (int)((self.global_end - start) / 3600)  # hours from global end
        end_index = (int)((self.global_end - end) / 3600)  # hours from global end

        with importlib.resources.open_text('logic.data', 'gainesville.json') as file:
            data = json.load(file)
            result = []
            loop_start = len(data) - start_index + 16
            loop_end = len(data) - end_index + 16

            print("loop start: ", loop_start, " loop end: ", loop_end)
            for i in range(loop_end, loop_start, -1):
                if limit == 0:
                    break
                limit -= 1

                if(i % 24 == 0):
                    if self._convert_raw_day(data[i]):
                        print("Query: ", data[i]["dt_iso"])
                        result.append(self._convert_raw_day(data[i]))
                    else:
                        pass
            print("result length: ", len(result))
            return result

