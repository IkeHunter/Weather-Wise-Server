"""
Locic API Urls
"""
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'summary', views.SummaryViewSet)
router.register(r'results', views.ResultsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='weather_framework'))
]

