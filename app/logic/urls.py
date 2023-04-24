"""
Locic API Urls
"""
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'summary', views.SummaryViewSet)
router.register(r'search', views.ResultsViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
    path(r'initialize', views.Initialize, name='initialize'),
    path('api-auth/',
         include('rest_framework.urls', namespace='weather_framework')),
]

