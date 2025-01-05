import logging
import pandas as pd

from django.db.models import Q
from iris_flowers_api.models import *

logger = logging.getLogger(__name__)


def removeOutlyingFlowerSpecimen() -> None:
    """
    Calculates the mean and standard deviation values of the specimen properties of all iris species
    and removes the outliers (3 or more standard deviations from the mean)
    """
    allFlowerSpecies = Species.objects.all()

    deletedSpecimenCount = 0

    for flowerSpecies in allFlowerSpecies:
        
        flowerSpecimenInThisSpecies = PlantSpecimen.objects.filter(species = flowerSpecies).values()

        # Load all iris flower specimen of this species into a Pandas DataFrame
        df = pd.DataFrame(flowerSpecimenInThisSpecies)

        std = df.std(numeric_only = True)
        mean = df.mean(numeric_only = True)

        specimenToBeDeleted = PlantSpecimen.objects.filter(
            Q(species = flowerSpecies),
            Q(sepalLength__gte = mean["sepalLength"] + 3 * std["sepalLength"]) | Q(sepalLength__lte = mean["sepalLength"] - 3 * std["sepalLength"]) |
            Q(sepalWidth__gte = mean["sepalWidth"] + 3 * std["sepalWidth"]) | Q(sepalWidth__lte = mean["sepalWidth"] - 3 * std["sepalWidth"]) |
            Q(petalLength__gte = mean["petalLength"] + 3 * std["petalLength"]) | Q(petalLength__lte = mean["petalLength"] - 3 * std["petalLength"]) |
            Q(petalWidth__gte = mean["petalWidth"] + 3 * std["petalWidth"]) | Q(petalWidth__lte = mean["petalWidth"] - 3 * std["petalWidth"])
        )

        deletedSpecimenCount += specimenToBeDeleted.count()
        specimenToBeDeleted.delete()
    
    logger.info(f"Removed {deletedSpecimenCount} flower specimen with measurements outside 3 standard deviations from the mean")