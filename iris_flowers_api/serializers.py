from rest_framework import serializers
from .models import *

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'

class PlantSpecimenSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer(read_only = True)

    class Meta:
        model = PlantSpecimen
        fields = ['species', 'sepalLength', 'sepalWidth', 'petalLength', 'petalWidth']