import logging

from rest_framework import serializers
from .models import *

logger = logging.getLogger(__name__)


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'

class PlantSpecimenSerializer(serializers.ModelSerializer):
    species = SpeciesSerializer(read_only = True)

    def create(self, validated_data) -> PlantSpecimen:
        logger.debug(f"Validated data: {validated_data}")

        speciesObject = Species.objects.filter(name = validated_data.get("speciesId")).first()

        logger.debug(f"Found species: {speciesObject}")

        del validated_data["speciesId"]

        newSpecimen = PlantSpecimen(**validated_data)
        newSpecimen.species = speciesObject
        newSpecimen.save()
        return newSpecimen

    class Meta:
        model = PlantSpecimen
        fields = ['id', 'species', 'sepalLength', 'sepalWidth', 'petalLength', 'petalWidth']