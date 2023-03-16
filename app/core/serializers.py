from rest_framework import serializers
from .models import Package


class PackageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Package
        fields = ('title', 'data')
