"""
Test weather API models
"""
from django.test import TestCase
from logic.models import Summary, SearchResults, \
    ConditionsList, Forecast, ForecastTable, ForecastRow


class SummaryConfigTests(TestCase):
    def test_create_summary(self):
        location = "32608"
        user = 1

        summary = Summary.objects.create(
            location=location,
            user=user,
        )

        self.assertEqual(summary.location, location)
        self.assertEqual(summary.user, user)

    def test_create_conditions_list(self):
        title = "Current Conditions"
        average_temp = 0
        feels_like = 1
        pressure = 2
        humidity = 3
        wind_speed = 4
        pop = 5
        rain_level = 6

        conditions = ConditionsList.objects.create(
            title=title,
            average_temp=average_temp,
            feels_like=feels_like,
            pressure=pressure,
            humidity=humidity,
            wind_speed=wind_speed,
            pop=pop,
            rain_level=rain_level
        )

        self.assertEqual(conditions.title, title)
        self.assertEqual(conditions.average_temp, average_temp)
        self.assertEqual(conditions.feels_like, feels_like)
        self.assertEqual(conditions.pressure, pressure)
        self.assertEqual(conditions.humidity, humidity)
        self.assertEqual(conditions.wind_speed, wind_speed)
        self.assertEqual(conditions.pop, pop)
        self.assertEqual(conditions.rain_level, rain_level)

    def test_create_forecast(self):
        date = 1578384000
        sunrise = 0
        sunset = 1
        wind_speed = 2
        wind_deg = 3

        forecast = Forecast.objects.create(
            date=date,
            sunrise=sunrise,
            sunset=sunset,
            wind_speed=wind_speed,
            wind_deg=wind_deg
        )

        self.assertEqual(forecast.date, date)
        self.assertEqual(forecast.sunrise, sunrise)
        self.assertEqual(forecast.sunset, sunset)
        self.assertEqual(forecast.wind_speed, wind_speed)
        self.assertEqual(forecast.wind_deg, wind_deg)

    def test_create_forecast_table(self):
        type = "Temperature Forecast"
        range = "h"

        forecastTable = ForecastTable.objects.create(
            type=type,
            range=range
        )

        self.assertEqual(forecastTable.type, type)
        self.assertEqual(forecastTable.range, range)

    def test_create_forecast_row(self):
        value = 0
        time = 1578384000

        forecastRow = ForecastRow.objects.create(
            value=value,
            time=time
        )

        self.assertEqual(forecastRow.value, value)
        self.assertEqual(forecastRow.time, time)

    def test_create_search_results(self):
        pass

