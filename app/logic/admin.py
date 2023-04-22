from django.contrib import admin
from .models import Page, Conditions, Forecast, ForecastRow, ForecastTable

class ConditionsInline(admin.StackedInline):
    model = Conditions

class ForecastRowInline(admin.TabularInline):
    model = ForecastRow

class ForecastTableInline(admin.TabularInline):
    model = ForecastTable


@admin.register(Page)
class SummaryAdmin(admin.ModelAdmin):
    inlines = [ ConditionsInline ]

@admin.register(ForecastTable)
class ForecastTableAdmin(admin.ModelAdmin):
    inlines = [ ForecastRowInline ]
    save_as = True

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    inlines = [ ForecastTableInline ]

# @admin.register(SearchResults)
# class SearchResultsAdmin(admin.ModelAdmin):
#     inlines = [ ConditionsInline ]

