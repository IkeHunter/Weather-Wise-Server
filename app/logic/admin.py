from django.contrib import admin
from .models import Summary, ConditionsList, Forecast, ForecastRow, ForecastTable

class ConditionsListInline(admin.TabularInline):
    model = ConditionsList

class ForecastRowInline(admin.TabularInline):
    model = ForecastRow

class ForecastTableInline(admin.TabularInline):
    model = ForecastTable

@admin.register(Summary)
class SummaryAdmin(admin.ModelAdmin):
    inlines = [ ConditionsListInline ]

@admin.register(ForecastTable)
class ForecastTableAdmin(admin.ModelAdmin):
    inlines = [ ForecastRowInline ]

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    inlines = [ ForecastTableInline ]

