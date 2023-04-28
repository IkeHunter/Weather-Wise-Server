"""
Views for Logic api
"""

import json
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import PageSerializer, SearchResultsSerializer
from .models import Conditions, Page, SearchLog
from django.db.models import Q

from .api import Summary
from .data import Archive

from .weather import BPlusTree, WeatherHeap, Parameter as heap_type


ORDER = 30

# summary = Summary()
archive = Archive()
btree = BPlusTree()

def Initialize(request):
    summary = Summary()
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')

    summary.set_location(latitude, longitude)
    postal_code = summary.get_postal_code()
    print("initializing for " + str(postal_code))
    if not SearchLog.objects.filter(location=postal_code).exists():
        print("Creating new SearchLog for " + str(postal_code))
        summary.create_summary()
        yearDays = summary.get_past_year()
        create_mini_widgets(yearDays, summary)

    package = {
        "success": "true",
        "postal_code": summary.get_postal_code(),
    }
    return HttpResponse(json.dumps(package), content_type="application/json")

def ChangeLocation(request):
    postal_code = request.GET.get('postal-code')
    summary = Summary()
    summary.set_location_postal(postal_code)
    if not SearchLog.objects.filter(location=postal_code).exists():
        print("Creating new SearchLog for " + str(postal_code))
        summary.create_summary()
        yearDays = summary.get_past_year()
        create_mini_widgets(yearDays, summary)
    package = {
        "success": "true",
        "latitude": summary.get_lat(),
        "longitude": summary.get_long(),
        "postal_code": summary.get_postal_code(),
    }
    return HttpResponse(json.dumps(package), content_type="application/json")

class SummaryViewSet(viewsets.ModelViewSet):
    """
    # TODO: create current_conditions, last_year, forecast data in db
    # TODO: get past year days as json in Conditions format
    # TODO: send past year json to heap, return json
    # TODO: create model for widgets from json result
    """

    queryset = Page.objects.filter(
        page_title="summary"
    ).order_by('location')
    # print(queryset)
    serializer_class = PageSerializer

class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.filter(
            page_title="search"
        ).order_by('location')
    serializer_class = SearchResultsSerializer


    def create(self, request, *args, **kwargs):
        """
        TODO: get search parameters
        TODO: Create b+ tree
        TODO: get filtered days by date
        TODO: b+ tree search with prameters
        TODO: return json results without creating model

        @param request: start, end, temperature, precipitation, humidity, location
        @return: list of days
        """
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        content = body
        allDays = archive.get_time_period(start=content["start"], end=content["end"])
        btree.create(allDays, ORDER)

        results: json = btree.find(average_temp=int(content["temperature"]), precipitation=int(content["precipitation"]), humidity=int(content["humidity"]))
        results = json.dumps(results)

        return HttpResponse(results, content_type="application/json")

def create_mini_widgets(yearDays, summary: Summary):
    """
    Widgets:
        hottest_day, coldest_day, rainiest_day, latest_sunrise,
        muggiest_day, earliest_sunrise, latest_sunset, earliest_sunset
    """
    heap = WeatherHeap()
    print("year days: " + str(len(yearDays)))

    heap.create(yearDays=yearDays, param=heap_type.HOT)
    widgets = {
        "hottest_day": json,
        "coldest_day": json,
        "rainiest_day": json,
        "latest_sunrise": json,
        "muggiest_day": json,
    }

    widgets["hottest_day"] = heap.find(1)
    heap.orderHeap(heap_type.COLD)
    widgets["coldest_day"] = heap.find(1)
    heap.orderHeap(heap_type.RAIN_LEVEL)
    widgets["rainiest_day"] = heap.find(1)
    heap.orderHeap(heap_type.SUNR)
    widgets["latest_sunrise"] = heap.find(1)
    heap.orderHeap(heap_type.HUMID)
    widgets["muggiest_day"] = heap.find(1)

    for [widget, data] in widgets.items():
        data = json.loads(data)[0]
        # print(data)

        condition = Conditions.objects.create(
            widget_title=widget,
            location=summary.get_location(),
            date=int(data["date"]),
            average_temp=int(data["average_temp"]),
            feels_like=int(data["feels_like"]),
            pop=int(data["pop"]),
            humidity=int(data["humidity"]),
            sunrise=int(data["sunrise"]),
            sunset=int(data["sunset"]),
            pressure=int(data["pressure"]),
            wind_speed=int(data["wind_speed"]),
            weather_name=data["weather_name"],
            icon=data["icon"],
        )
        condition.save()
        # print(condition)




