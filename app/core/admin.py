"""Admin file, add config options for admin view"""
from django.contrib import admin
from .models import Package

# this is required to edit Package in admin view
admin.site.register(Package)


