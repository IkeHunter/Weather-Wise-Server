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
from .models import Conditions, Page, SearchLog
from django.db.models import Q

from .api import Summary
from .data import Archive

from .weather import BPlusTree, WeatherHeap, Parameter as heap_type
# from .weather import heap

ORDER = 30

summary = Summary()
archive = Archive()
# heap = WeatherHeap()
btree = BPlusTree()

def Initialize(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')
    # print(request.GET)
    # print(latitude, " ", longitude)
    summary.set_location(latitude, longitude)
    postal_code = summary.get_postal_code()
    if not SearchLog.objects.filter(location=summary.get_postal_code()).exists():
        summary.create_summary()
        yearDays = summary.get_past_year()
        create_mini_widgets(yearDays)



    archive.create_archive()
    package = {
        "success": "true",
        "postal_code": summary.get_postal_code(),
    }
    return HttpResponse(json.dumps(package), content_type="application/json")
    # return Response(package.json())


class SummaryViewSet(viewsets.ModelViewSet):
    """
    # TODO: create current_conditions, last_year, forecast data in db
    # TODO: get past year days as json in Conditions format
    # TODO: send past year json to heap, return json
    # TODO: create model for widgets from json result
    """

    # yearDays = summary.get_past_year()


    queryset = Page.objects.filter(
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
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # content = body['content']
        content = body
        print(content)
        allDays = archive.get_time_period(start=content["start"], end=content["end"])
        btree.create(allDays, ORDER)

        results: json = btree.find(average_temp=int(content["temperature"]), precipitation=int(content["precipitation"]), humidity=int(content["humidity"]))
        results = json.dumps(results)
        # queryset = Conditions.objects.filter(
        #     Q(widget_title="top_result") | Q(widget_title="search_results"),
        # ).order_by('location').values()  # returns json

        # serializer_class = SearchResultsSerializer
        # return Response(results)
        return HttpResponse(results, content_type="application/json")

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
    heap = WeatherHeap()
    # print(yearDays)
    heap.create(yearDays=yearDays, param=heap_type.HOT)
    widgets = {
        "hottest_day": json,
        "coldest_day": json,
        "rainiest_day": json,
        "latest_sunrise": json,
        "muggiest_day": json,
        # "earliest_sunset": json,
        # "latest_sunrise": json,
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
    # heap.orderHeap(heap_type.SUNS)
    # widgets["earliest_sunset"] = heap.find(1)
    # heap.orderHeap(heap_type.SUNR)
    # widgets["latest_sunrise"] = heap.find(1)

    for [widget, data] in widgets.items():
        # print("data: ")
        # data = json.dumps(data)
        data = json.loads(data)[0]

        condition = Conditions.objects.create(
            widget_title=widget,
            location=summary.get_location(),
            date=int(data["date"]),
            average_temp=int(data["average_temp"]),
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




