"""
Views for Logic api
"""
# from django.shortcuts import render
from rest_framework import viewsets

from .serializers import PageSerializer, SearchResultsSerializer
from .models import Page


class SummaryViewSet(viewsets.ModelViewSet):
    # queryset = Page.objects.all().order_by('location')
    queryset = Page.objects.filter(
        page_title="summary"
    ).order_by('location')
    serializer_class = PageSerializer

class ResultsViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.filter(
        page_title="search"
    ).order_by('location')
    serializer_class = SearchResultsSerializer



