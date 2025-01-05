import logging
import requests

from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, QueryDict
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from iris_flowers_api.models import *
from iris_flowers_api.serializers import *
from iris_flowers_api.util import *
from rest_framework.renderers import JSONRenderer

logger = logging.getLogger(__name__)
CONTENT_TYPE_JSON = "application/json"
DATASET_URL = "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"


class FlowerSpecimen(APIView):

    def get(self, request) -> Response:
        allSpecimens = PlantSpecimen.objects.all()
        serializer = PlantSpecimenSerializer(allSpecimens, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe = False)
    
    def post(self, request) -> Response:
        serializer = PlantSpecimenSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
        serializer.save(speciesId = serializer.initial_data["species"])

        return Response(status = status.HTTP_201_CREATED)
        

class Species(APIView):

    def get(self, request) -> Response:
        """
        Returns some statistic metrics for each of the Plant species
        """
        return JsonResponse({}, status = status.HTTP_200_OK, safe = False)

class InitData(APIView):

    def get(self, request) -> Response:
        """
        Downloads the Iris dataset, replaces any existing data in the DB with it
        and removes outliers (flower specimen which have a measurement outside 
        3 standard deviations of its species' mean value)        
        """

        # Delete all flower species and specimen from the database
        # PlatSpecimen will be deleted because of the cascading deletion on the foreign key
        Species.objects.all().delete()

        responseData = requests.get(DATASET_URL)
        dataString = responseData.text
        
        lines = dataString.split('\n')
        existingSpecies = list(Species.objects.all())
        flowers = []
        for i in range(1, len(lines)):

            if len(lines[i]) == 0:
                break

            segments = lines[i].split(',')

            # If the Iris species has not yet been added, add it
            if (not segments[4] in map(lambda species: species.name, existingSpecies)):
                newSpecies = Species(name = segments[4])
                newSpecies.save()
                existingSpecies.append(newSpecies)
            
            newSpecimen = PlantSpecimen(
                species = next(filter(lambda species: species.name == segments[4], existingSpecies)),
                sepalLength = float(segments[0]),
                sepalWidth = float(segments[1]),
                petalLength = float(segments[2]),
                petalWidth = float(segments[3])
            )

            newSpecimen.save()

        # Remove all flower specimen with measurements outside 3 standard deviations
        # of the species' mean
        removeOutlyingFlowerSpecimen()

        return Response(status = status.HTTP_204_NO_CONTENT)