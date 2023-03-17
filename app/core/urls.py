"""
URLs
These are the urls managed by this app, they are appended to the
base determined in app/urls.py
"""
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'packages', views.PackageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework'))
]
