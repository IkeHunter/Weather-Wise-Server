"""
Models
These determine the way data is stored in the database,
and how they are presented in the JSON response
"""

from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=255)
    data = models.IntegerField()

    def __str__(self):
        return self.title + ': ' + str(self.data)
