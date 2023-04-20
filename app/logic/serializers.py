"""
Weather API Serializers
"""
from rest_framework import serializers
from django.db.models import QuerySet
# from drf_queryfields import QueryFieldsMixin
from .models import Summary, ConditionsList, Forecast, ForecastTable, ForecastRow


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

    def get_table(self, obj):
        forecast = Forecast.objects.get(location=obj.id)
        table = ForecastTable.objects.filter(
            forecast_id=forecast.id,
        ).values()
        tableSerial = ForecastTableSerializer(table, many=True, context={table: obj})
        return tableSerial.data


class SummarySerializer(serializers.ModelSerializer):
    current_conditions = serializers.SerializerMethodField()
    last_year = serializers.SerializerMethodField()
    forecast = serializers.SerializerMethodField()

    class Meta:
        model = Summary
        fields = ('__all__')
        depth = 3

    def get_forecast(self, obj: Summary):
        return ForecastSerializer(obj, many=False).data

    def get_current_conditions(self, obj: Summary) -> QuerySet:
        current_conditions: QuerySet = ConditionsList.objects.filter(
            location_id=obj.id,
            widget_title="Current Conditions"
        ).values()
        return current_conditions[0]
    def get_last_year(self, obj: Summary) -> QuerySet:
        last_year: QuerySet = ConditionsList.objects.filter(
            location_id=obj.id,
            widget_title="Last Year"
        ).values()
        return last_year[0]
