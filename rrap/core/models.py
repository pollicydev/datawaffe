from django.db import models
from django.contrib.gis.db.models import PolygonField


# used Location as identifier but initially represents districts. Could scale to have counties and subcounties
class Location(models.Model):
    name = models.CharField(max_length=100)
    geom = PolygonField(srid=4326)
    population = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
