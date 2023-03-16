# from django.shortcuts import render

from rest_framework import viewsets

from .serializers import PackageSerializer
from .models import Package


class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all().order_by('title')
    serializer_class = PackageSerializer
