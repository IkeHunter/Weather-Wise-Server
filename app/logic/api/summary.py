import requests
import json
import environ
import time
import datetime
from django.contrib.postgres.search import SearchQuery
from logic.models import Page, Conditions, Forecast, ForecastTable, ForecastRow, SearchLog

env = environ.Env()
environ.Env.read_env()

class Summary:
    def __init__(self):
        self.lat = 0
        self.long = 0
        self.key = env('API_KEY')
        self.maps_key = env('MAPS_KEY')
        self.summary: Page
        self.forecast_limit = 12
        # self.widget_period = 28944000

    def _request(self, url, params="") -> json:
        url = url + f"?lat={self.lat}&lon={self.long}{params}&appid={self.key}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def _fetch_current_conditions(self):
        url = "https://pro.openweathermap.org/data/2.5/weather"
        hourlyUrl = "https://pro.openweathermap.org/data/2.5/forecast"

        data = self._request(url)
        hourly = self.request(hourlyUrl)

        current_conditions = Conditions(
            location = self.summary,
            widget_title = "current_conditions",
            date = data["dt"],
            average_temp = data["main"]["temp"],
            feels_like = data["main"]["feels_like"],
            pressure = data["main"]["pressure"],
            humidity = data["main"]["humidity"],
            wind_speed = data["wind"]["speed"],
            pop = hourly["list"][0]["pop"],
            rain_levels = -1,
            sunrise = data["sys"]["sunrise"],
            sunset = data["sys"]["sunset"],
        )
        current_conditions.save()
        print(data)


    def _fetch_past_year(self) -> json:
        url = "https://history.openweathermap.org/data/2.5/aggregated/year"
        data = self._request(url)
        result = []
        for day in data["result"]:
            result.append({
                "date": day["dt"],
                "average_temp": day["temp"],
                "feels_like": day["feels_like"],
                "pressure": day["pressure"],
                "humidity": day["humidity"],
                "wind_speed": day["wind_speed"],
                "pop": day["pop"],
                "rain_levels": day["rain_levels"],
                "sunrise": day["sunrise"],
                "sunset": day["sunset"],
                "weather_name": day["weather_name"],
                "icon": day["icon"],
            })

        return result


    def _fetch_forecast(self):
        url = "https://pro.openweathermap.org/data/2.5/forecast"
        forecastHourly = self._request(url)

        forecast = Forecast(
            location = self.summary,
            date = forecastHourly["list"][0]["dt"],
            sunrise = forecastHourly["city"]["sunrise"],
            sunset = forecastHourly["city"]["sunset"],
            wind_speed = forecastHourly["list"][0]["wind"]["speed"],
            wind_deg = forecastHourly["list"][0]["wind"]["deg"],
        )
        forecast.save()

        forecast_hourly_list = forecastHourly["list"]

        forecast_h_temp = ForecastTable(
            forecast = forecast,
            type = "Temperature Forecast",
            range = "h",
        )
        forecast_h_temp.save()
        forecast_h_pop = ForecastTable(
            forecast = forecast,
            type = "Precipitation Forecast",
            range = "h",
        )
        forecast_h_pop.save()
        forecast_h_wind = ForecastTable(
            forecast = forecast,
            type = "Wind Forecast",
            range = "h",
        )
        forecast_h_wind.save()
        forecast_h_humidity = ForecastTable(
            forecast = forecast,
            type = "Humidity Forecast",
            range = "h",
        )
        forecast_h_humidity.save()

        for i in range(self.forecast_limit):
            hour = forecast_hourly_list[i]
            forecast_h_temp_row = ForecastRow(
                value = hour["main"]["temp"],
                forecast_table = forecast_h_temp,
                time = hour["dt"],
            )
            forecast_h_temp_row.save()
            forecast_h_pop_row = ForecastRow(
                value = hour["pop"],
                forecast_table = forecast_h_pop,
                time = hour["dt"],
            )
            forecast_h_pop_row.save()
            forecast_h_wind_row = ForecastRow(
                value = hour["wind"]["speed"],
                forecast_table = forecast_h_wind,
                time = hour["dt"],
            )
            forecast_h_wind_row.save()
            forecast_h_humidity_row = ForecastRow(
                value = hour["main"]["humidity"],
                forecast_table = forecast_h_humidity,
                time = hour["dt"],
            )
            forecast_h_humidity_row.save()

        url = "https://pro.openweathermap.org/data/2.5/forecast/daily"
        params = f"&cnt={self.forecast_limit}"
        forecastDaily = self._request(url, params)

        forecastDailyList = forecastDaily["list"]

        forecast_d_temp = ForecastTable(
            forecast = forecast,
            type = "Temperature Forecast",
            range = "d",
        )
        forecast_d_temp.save()
        forecast_d_pop = ForecastTable(
            forecast = forecast,
            type = "Precipitation Forecast",
            range = "d",
        )
        forecast_d_pop.save()
        forecast_d_wind = ForecastTable(
            forecast = forecast,
            type = "Wind Forecast",
            range = "d",
        )
        forecast_d_wind.save()
        forecast_d_humidity = ForecastTable(
            forecast = forecast,
            type = "Humidity Forecast",
            range = "d",
        )
        forecast_d_humidity.save()

        for i in range(self.forecast_limit):
            day = forecastDailyList[i]
            forecast_d_temp_row = ForecastRow(
                value = day["temp"]["day"],
                forecast_table = forecast_d_temp,
                time = day["dt"],
            )
            forecast_d_temp_row.save()
            forecast_d_pop_row = ForecastRow(
                value = day["pop"],
                forecast_table = forecast_d_pop,
                time = day["dt"],
            )
            forecast_d_pop_row.save()
            forecast_d_wind_row = ForecastRow(
                value = day["wind"]["speed"],
                forecast_table = forecast_d_wind,
                time = day["dt"],
            )
            forecast_d_wind_row.save()
            forecast_d_humidity_row = ForecastRow(
                value = day["humidity"],
                forecast_table = forecast_d_humidity,
                time = day["dt"],
            )
            forecast_d_humidity_row.save()


    def _save_to_db(self):
        log = SearchLog(
            location = self._get_postal_code(),
        )
        log.save()

    def _get_postal_code(self) -> str:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={self.lat},{self.long}&key={self.maps_key}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()["results"][0]["address_components"][6]["long_name"]

    def set_location(self, lat, long):
        self.lat = lat
        self.long = long
        self.summary = Page(
            location = self._get_postal_code(),
            page_title="summary"
        )
        self.summary.save()

    def create_summary(self):
        # check if summary with same location exists
        # if Page.objects.filter(location=self._get_postal_code(), page_title="summary").exists():
        #     return
        if SearchLog.objects.filter(location=self._get_postal_code()).exists():
            return
        self._fetch_current_conditions()
        self._fetch_forecast()
        self._save_to_db()


    def change_location(self, lat, long):
        pass
    def get_past_year(self):
        pass


