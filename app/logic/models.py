"""
Weather API models
"""
from django.db import models


class Summary(models.Model):
    """Primary model for summary endpoint"""
    location = models.IntegerField(default=32608)
    user = models.IntegerField(default=0)

    def __str__(self):
        return "Summary for " + str(self.location)

class SearchResults(models.Model):
    """Primary model for search endpoint"""
    pass


class ConditionsList(models.Model):
    """Conditions model for individual day"""
    widget_title = models.CharField(max_length=64, default='Conditions')
    date = models.BigIntegerField(default=1578384000)
    location = models.ForeignKey(Summary, on_delete=models.CASCADE)

    average_temp = models.IntegerField(default=0)
    feels_like = models.IntegerField(default=1)
    pressure = models.IntegerField(default=2)
    humidity = models.IntegerField(default=3)
    wind_speed = models.IntegerField(default=4)
    pop = models.IntegerField(default=5)
    rain_level = models.IntegerField(default=6)

    def __str__(self):
        return "Conditions for " + str(self.widget_title)


class Forecast(models.Model):
    """Main forecast data for summary endpoint"""
    date = models.BigIntegerField(default=1578384000)
    sunrise = models.BigIntegerField(default=1578384000)
    sunset = models.BigIntegerField(default=1578384000)
    wind_speed = models.IntegerField(default=0)
    wind_deg = models.IntegerField(default=1)

    def __str__(self):
        return "Forecast for " + str(self.date)


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


