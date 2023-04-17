"""
Weather API models
"""

from django.db import models


class Summary(models.Model):
    """Primary model for summary endpoint"""
    location = models.IntegerField()
    user = models.IntegerField()

    def __str__(self):
        return "Summary for " + self.location


class SearchResults(models.Model):
    """Primary model for search endpoint"""
    pass


class ConditionsList(models.Model):
    """Conditions model for individual day"""
    title = models.CharField(max_length=32)
    average_temp = models.IntegerField()
    feels_like = models.IntegerField()
    pressure = models.IntegerField()
    humidity = models.IntegerField()
    wind_speed = models.IntegerField()
    pop = models.IntegerField()
    rain_level = models.IntegerField()

    def __str__(self):
        return "Conditions for " + self.title


class Forecast(models.Model):
    """Main forecast data for summary endpoint"""
    date = models.BigIntegerField()
    sunrise = models.IntegerField()
    sunset = models.IntegerField()
    wind_speed = models.IntegerField()
    wind_deg = models.IntegerField()

    def __str__(self):
        return "Forecast for " + self.date


class ForecastTable(models.Model):
    """Forecast table model for summary endpoint"""
    RANGE_TYPES = [
        ("h", "hourly"),
        ("d", "daily")
    ]
    type = models.CharField(max_length=64)
    range = models.CharField(max_length=1, choices=RANGE_TYPES)

    def __str__(self):
        return "Forecast data of " + self.type + " : " + self.range



class ForecastRow(models.Model):
    """Row model for forecast table"""
    value = models.IntegerField()
    time = models.BigIntegerField()


