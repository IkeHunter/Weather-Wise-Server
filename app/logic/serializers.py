"""
Weather API Serializers
"""
from rest_framework import serializers
# from django.db.models import QuerySet
# from drf_queryfields import QueryFieldsMixin
from .models import Summary, ConditionsList, Forecast, ForecastTable, ForecastRow


# class ConditionsListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ConditionsList
#         fields = ('__all__')
#         # fields = ('title', 'average_temp', 'feels_like', 'pressure', \
#         #           'humidity', 'wind_speed', 'pop', 'rain_level')
# class ForecastRowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ForecastRow
#         fields = ('value', 'time')

# class ForecastTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ForecastTable
#         fields = ('__all__')

#     values = ForecastRowSerializer(many=True)


# class ForecastSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Forecast
#         fields = ('__all__')

#     table = ForecastTableSerializer(many=False)

# class SummarySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Summary
#         fields = ('__all__')

    # currentConditions = ConditionsListSerializer(many=False)
    # lastYear = ConditionsListSerializer(many=False)
    # forecast = ForecastSerializer(many=False)

    # current_conditions = serializers.SerializerMethodField()
    # last_year = serializers.SerializerMethodField()
    # forecast = serializers.SerializerMethodField()

    # def get_current_conditions(self, obj: Summary) -> QuerySet:



