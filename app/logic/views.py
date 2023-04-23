"""
Views for Logic api
"""
# from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

from .serializers import PageSerializer, SearchResultsSerializer
from .models import Conditions, Page
from django.db.models import Q

# from weather import bPlusTree
# from weather import heap

# tree = bPlusTree.BPlusTree()
# heap = heap.Heap()

class SummaryViewSet(viewsets.ModelViewSet):
    # queryset = Page.objects.all().order_by('location')

    # make api call to get data
    # heap.create(data)
    # tree.create(data)

    queryset = Page.objects.filter(
        page_title="summary"
    ).order_by('location')
    serializer_class = PageSerializer

class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.filter(
            page_title="search"
        ).order_by('location')
    serializer_class = SearchResultsSerializer
    def list(self, request):
        queryset = Page.objects.filter(
            page_title="search"
        ).order_by('location')
        serializer_class = SearchResultsSerializer
        return Response(serializer_class.data)

    def create(self, request, *args, **kwargs):
        print("POST")
        print(request.data)
        # request.data: todate, fromdate, temperature, precipitation, humidity, location
        # function(request.data) -> list of days
        # functino(list of day) -> create models
        queryset = Conditions.objects.filter(
            Q(widget_title="top_result") | Q(widget_title="search_results"),
        ).order_by('location')
        serializer_class = SearchResultsSerializer
        return Response(queryset.values())

# @csrf_exempt
# def post_search(request, Pk=None):
#     if request.method == "POST":
#         print("POST")

def get_list_of_days(request):
    # request: todate, fromdate, temperature, precipitation, humidity
    # functionality: take

    # days = bPlusTree.get_list_of_days(todate=request.data["todate"], fromdate=request.data["fromdate"], temperature=request.data["temperature"], precipitation=request.data["precipitation"], humidity=request.data["humidity"])

    # returns: dict of days
    pass



