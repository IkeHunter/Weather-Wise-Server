"""
Weather API models
"""
from django.db import models


class Page(models.Model):
    """Primary model for summary endpoint"""
    location = models.IntegerField(default=32608)
    user = models.IntegerField(default=0)
    page_title = models.CharField(max_length=64, default='Summary')

    def __str__(self):
        return self.page_title + " for " + str(self.location)

class Forecast(models.Model):
    """Main forecast data for summary endpoint"""
    date = models.BigIntegerField(default=1578384000)
    sunrise = models.BigIntegerField(default=1578384000)
    sunset = models.BigIntegerField(default=1578384000)
    wind_speed = models.IntegerField(default=0)
    wind_deg = models.IntegerField(default=1)
    location = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return "Forecast for " + str(self.date)

class Conditions(models.Model):
    """Conditions model for individual day"""
    widget_title = models.CharField(max_length=64, default='Conditions')
    date = models.BigIntegerField(default=1578384000)
    location = models.ForeignKey(Page, on_delete=models.CASCADE)

    average_temp = models.IntegerField(default=0)
    feels_like = models.IntegerField(default=1)
    pressure = models.IntegerField(default=2)
    humidity = models.IntegerField(default=3)
    wind_speed = models.IntegerField(default=4)
    pop = models.IntegerField(default=5)
    rain_levels = models.IntegerField(default=6)

    weather_name = models.CharField(max_length=64, default="Rain")
    icon = models.CharField(max_length=32, default="10n")

    def __str__(self):
        return "Conditions for " + str(self.widget_title)

class ForecastTable(models.Model):
    """Forecast table model for summary endpoint"""
    RANGE_TYPES = [
        ("h", "hourly"),
        ("d", "daily")
    ]
    type = models.CharField(max_length=64, default="Temperature Forecast")
    range = models.CharField(max_length=1, choices=RANGE_TYPES, default="h")
    forecast = models.ForeignKey(Forecast, on_delete=models.CASCADE)

    def __str__(self):
        return "Forecast data of " + self.type + " : " + self.range

class ForecastRow(models.Model):
    """Row model for forecast table"""
    value = models.IntegerField()
    time = models.BigIntegerField()
    forecastTable = models.ForeignKey(ForecastTable, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time) + " : " + str(self.value)


# class SearchResults(models.Model):
#     """Primary model for search endpoint"""
#     location = models.ForeignKey(Page, on_delete=models.CASCADE)
#     count = models.IntegerField(default=0)

#     def __str__(self):
#         return "Search results for " + str(self.location)
