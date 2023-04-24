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
    """
    TODO: create current_conditions, last_year, forecast data in db
    TODO: get past year days as json in Conditions format
    TODO: send past year json to heap, return results
    TODO: create model for widgets from json result
    """
    yearDays = summary.get_past_year()

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

        @param request: todate, fromdate, temperature, precipitation, humidity, location
        @return: list of days
        """
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



