"""
Views for Logic api
"""
# from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import PageSerializer, SearchResultsSerializer
from .models import Conditions, Page
from django.db.models import Q

from .api import Summary
from .data import Archive

# from weather import bPlusTree
# from weather import heap

# tree = bPlusTree.BPlusTree()
# heap = heap.Heap()

summary = Summary()
archive = Archive()

def Initialize(request):
    latitude = request.GET.get('lat')
    longitude = request.GET.get('long')
    summary.set_location(latitude, longitude)
    
    summary.create_summary()
    archive.create_archive()
    return HttpResponse("Initialized")


class SummaryViewSet(viewsets.ModelViewSet):
    # queryset = Page.objects.all().order_by('location')
    # allDays = loadAllDays()  # Isaac
    yearDays = summary.get_past_year()

    # convetModels(yearDays, allDays) # Isaac

    # make api call to get data
    # heap.create(yearDays) # Kevin

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
        # test: http://localhost:8000/api/docs - POST - /weather/results/
        print("POST")
        print(request.data)
        # request.data: todate, fromdate, temperature, precipitation, humidity, location
        # function(request.data) -> list of days
        # functino(list of day) -> create models

        # selectedDays: json = filterDays(todate, fromdate) // Isaac
        # tree.create(selectedDays) // Kevin
        # filteredDays: json = tree.find(temperature, precipitation, humidity) // Kevin
        # return Response(filteredDays) // Kevin + Isaac

        queryset = Conditions.objects.filter(
            Q(widget_title="top_result") | Q(widget_title="search_results"),
        ).order_by('location').values()  # returns json
        print("queryset: ")
        print(queryset)
        serializer_class = SearchResultsSerializer
        return Response(queryset)

def get_list_of_days(request):
    # request: todate, fromdate, temperature, precipitation, humidity
    # functionality: take

    # days = bPlusTree.get_list_of_days(todate=request.data["todate"], fromdate=request.data["fromdate"], temperature=request.data["temperature"], precipitation=request.data["precipitation"], humidity=request.data["humidity"])

    # returns: dict of days
    pass



