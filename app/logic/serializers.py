"""
Weather API Serializers
"""
from rest_framework import serializers
from django.db.models import QuerySet
# from drf_queryfields import QueryFieldsMixin
from .models import Page, Conditions, Forecast, ForecastTable, ForecastRow
from django.db.models import Q


class ForecastRowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastRow
        fields = ('__all__')

class ForecastTableSerializer(serializers.ModelSerializer):
    values = serializers.SerializerMethodField()
    class Meta:
        model = ForecastTable
        fields = ('__all__')
        depth = 1

    def get_values(self, obj):
        rows = ForecastRow.objects.filter(
            forecastTable_id=obj['id']
        ).values()
        return rows

class ForecastSerializer(serializers.ModelSerializer):
    table = serializers.SerializerMethodField()

    class Meta:
        model = Forecast
        fields = ('__all__')
        depth = 2

    def get_table(self, obj: Forecast):
        table = ForecastTable.objects.filter(
            forecast_id=obj["id"],
        ).values()

        tableSerial = ForecastTableSerializer(table, many=True)
        return tableSerial.data

class PageSerializer(serializers.ModelSerializer):
    current_conditions = serializers.SerializerMethodField()
    last_year = serializers.SerializerMethodField()
    forecast = serializers.SerializerMethodField()
    widgets = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ('__all__')
        depth = 3

    def get_forecast(self, obj: Page):
        forecast: QuerySet = Forecast.objects.filter(
            location_id=obj.id,
        ).values().first()

        return ForecastSerializer(instance=forecast, many=False).data

    def get_current_conditions(self, obj: Page) -> QuerySet:
        current_conditions: QuerySet = Conditions.objects.filter(
            location_id=obj.id,
            widget_title="current_conditions"
        ).values().first()
        return current_conditions
    def get_last_year(self, obj: Page) -> QuerySet:
        last_year: QuerySet = Conditions.objects.filter(
            location_id=obj.id,
            widget_title="last_year"
        ).values().first()
        return last_year
    def get_widgets(self, obj: Page) -> QuerySet:
        widgets: QuerySet = Conditions.objects.filter(
            ~Q(widget_title="current_conditions") & ~Q(widget_title="last_year"),
            location_id=obj.id,

        ).values()
        return widgets

class SearchResultsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()
    class Meta:
        model = Page
        fields = ('__all__')
        depth = 1

    def get_data(self, obj):
        results: QuerySet = Conditions.objects.filter(
            location_id=obj.id,
        ).values()
        return results