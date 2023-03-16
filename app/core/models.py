from django.db import models


class Package(models.Model):
    title = models.CharField(max_length=255)
    data = models.IntegerField()

    def __str__(self):
        return self.title + ': ' + str(self.data)
