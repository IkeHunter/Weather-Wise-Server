"""
Views for Logic api
"""
# from django.shortcuts import render
from rest_framework import viewsets

from .serializers import SummarySerializer
from .models import Summary


class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all().order_by('location')
    serializer_class = SummarySerializer



