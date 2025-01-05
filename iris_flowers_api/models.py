from django.db import models

# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length = 100, primary_key = True)


class PlantSpecimen(models.Model):
    species = models.ForeignKey(Species, on_delete = models.CASCADE)
    sepalLength = models.FloatField()
    sepalWidth = models.FloatField()
    petalLength = models.FloatField()
    petalWidth = models.FloatField()
    
