"""
Views for Logic api
"""
# from django.shortcuts import render
import json
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import PageSerializer, SearchResultsSerializer
from .models import Conditions, Page
from django.db.models import Q

from .api import Summary
from .data import Archive

from .weather import BPlusTree as btree, WeatherHeap as heap, Parameter as heap_type
# from .weather import heap

tree = btree.BPlusTree()
heap = heap.Heap()

ORDER = 30

summary = Summary()
archive = Archive()

def Initialize(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')
    summary.set_location(latitude, longitude)
    summary.create_summary()
    yearDays = summary.get_past_year()
    create_mini_widgets(yearDays)


    archive.create_archive()
    package = {
        "success": "true",
        "postal_code": summary.get_location(),
    }
    return Response(package.json())


class SummaryViewSet(viewsets.ModelViewSet):
    """
    TODO: create current_conditions, last_year, forecast data in db
    TODO: get past year days as json in Conditions format
    TODO: send past year json to heap, return json
    TODO: create model for widgets from json result
    """

    # yearDays = summary.get_past_year()


    queryset = Page.objects.filter(
        location=summary.get_location(),
        page_title="summary"
    ).order_by('location')
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
        # allDays = archive.get_all_days()
        allDays = archive.get_time_period(request.data["start"], request.data["end"])
        btree.create(allDays, ORDER)

        results: json = btree.find(request.data["temperature"], request.data["precipitation"], request.data["humidity"], request.data["location"])

        # queryset = Conditions.objects.filter(
        #     Q(widget_title="top_result") | Q(widget_title="search_results"),
        # ).order_by('location').values()  # returns json

        # serializer_class = SearchResultsSerializer
        return Response(results)

def get_list_of_days(request):
    # request: todate, fromdate, temperature, precipitation, humidity
    # functionality: take

    # days = bPlusTree.get_list_of_days(todate=request.data["todate"], fromdate=request.data["fromdate"], temperature=request.data["temperature"], precipitation=request.data["precipitation"], humidity=request.data["humidity"])

    # returns: dict of days
    pass

def create_mini_widgets(yearDays):
    """
    Widgets:
        hottest_day, coldest_day, rainiest_day, latest_sunrise,
        muggiest_day, earliest_sunrise, latest_sunset, earliest_sunset
    """

    heap.create(yearDays, heap_type.HOT)
    widgets = {
        "hottest_day": json,
        "coldest_day": json,
        "rainiest_day": json,
        "latest_sunrise": json,
        "muggiest_day": json,
        "earliest_sunset": json,
        "latest_sunrise": json,
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
    heap.orderHeap(heap_type.SUNS)
    widgets["earliest_sunset"] = heap.find(1)
    heap.orderHeap(heap_type.SUNR)
    widgets["latest_sunrise"] = heap.find(1)

    for [widget, data] in widgets:
        condition = Conditions.objects.create(
            widget_title=widget,
            location=summary.get_location(),
            date=data["date"],
            average_temp=data["average_temp"],
            pop=data["precipitation"],
            humidity=data["humidity"],
            sunrise=data["sunrise"],
            sunset=data["sunset"],
            pressure=data["pressure"],
            wind_speed=data["wind_speed"],
            weather_name=data["weather_name"],
            icon=data["icon"],
        )
        condition.save()




