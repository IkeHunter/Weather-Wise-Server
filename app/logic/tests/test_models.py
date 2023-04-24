"""
Test weather API models
"""
from django.test import TestCase
from logic.models import Page, \
    Conditions, Forecast, ForecastTable, ForecastRow


class SummaryConfigTests(TestCase):
    def test_create_page(self):
        location = "32608"
        user = 1
        page_title = "summary"

        summary = Page.objects.create(
            location=location,
            user=user,
            page_title=page_title,
        )

        self.assertEqual(summary.location, location)
        self.assertEqual(summary.user, user)
        self.assertEqual(summary.page_title, page_title)

    def test_create_conditions_list(self):
        widget_title = "Current Conditions"
        date = 1578384000
        location = Page()
        average_temp = 0
        feels_like = 1
        pressure = 2
        humidity = 3
        wind_speed = 4
        pop = 5
        rain_levels = 6

        location.save()

        conditions = Conditions.objects.create(
            average_temp=average_temp,
            feels_like=feels_like,
            pressure=pressure,
            humidity=humidity,
            wind_speed=wind_speed,
            pop=pop,
            rain_levels=rain_levels,
            date=date,
            widget_title=widget_title,
            location=location,
        )

        self.assertEqual(conditions.widget_title, widget_title)
        self.assertEqual(conditions.date, date)
        self.assertEqual(conditions.location.location, location.location)
        self.assertEqual(conditions.average_temp, average_temp)
        self.assertEqual(conditions.feels_like, feels_like)
        self.assertEqual(conditions.pressure, pressure)
        self.assertEqual(conditions.humidity, humidity)
        self.assertEqual(conditions.wind_speed, wind_speed)
        self.assertEqual(conditions.pop, pop)
        self.assertEqual(conditions.rain_levels, rain_levels)

    def test_create_forecast(self):
        date = 1578384000
        sunrise = 1578384001
        sunset = 1578384002
        wind_speed = 2
        wind_deg = 3
        location = Page.objects.create(
            location=32608,
            user=0
        )
        location.save()

        forecast = Forecast.objects.create(
            date=date,
            sunrise=sunrise,
            sunset=sunset,
            wind_speed=wind_speed,
            wind_deg=wind_deg,
            location=location
        )

        self.assertEqual(forecast.date, date)
        self.assertEqual(forecast.sunrise, sunrise)
        self.assertEqual(forecast.sunset, sunset)
        self.assertEqual(forecast.wind_speed, wind_speed)
        self.assertEqual(forecast.wind_deg, wind_deg)
        self.assertEqual(forecast.location.id, location.id)

    def test_create_forecast_table(self):
        location = Page(
            location=32608,
            user=0
        )
        location.save()
        forecast = Forecast(location=location)
        forecast.save()
        type = "Temperature Forecast"
        range = "h"

        forecastTable = ForecastTable.objects.create(
            type=type,
            range=range,
            forecast=forecast,
        )
        forecastTable.save()

        self.assertEqual(forecastTable.forecast.id, forecast.id)
        self.assertEqual(forecastTable.type, type)
        self.assertEqual(forecastTable.range, range)

    def test_create_forecast_row(self):
        value = 0
        time = 1578384000
        location = Page(
            location=32608,
            user=0
        )
        location.save()
        forecast=Forecast(location=location)
        forecast.save()
        forecastTable = ForecastTable(forecast=forecast)
        forecastTable.save()

        forecastRow = ForecastRow.objects.create(
            value=value,
            time=time,
            forecastTable=forecastTable,
        )

        self.assertEqual(forecastRow.value, value)
        self.assertEqual(forecastRow.time, time)

