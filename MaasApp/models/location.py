from django.db import models
from django_enumfield import enum


# Enum
class LocationType(enum.Enum):
    CAR_STATION = 0
    BIKE_STATION = 1
    SCOOTER_STATION = 2
    BUS_STOP = 3
    TRAIN_STATION = 4
    HUB = 5
    PARKING_AREA = 6
    DROP_OFF_POINT = 7
    PICK_UP_POINT = 8
    TRANSIT_CENTER = 9
    RANDOM_POINT = 10

    __labels__ = {
        CAR_STATION: "Auto station",
        BIKE_STATION: "Fietsenstalling",
        SCOOTER_STATION: "Scooterstation",
        BUS_STOP: "Bushalte",
        TRAIN_STATION: "Treinstation",
        HUB: "Mobiliteits hub",
        PARKING_AREA: "Parkeerplaats",
        DROP_OFF_POINT: "Uitstappunt",
        PICK_UP_POINT: "Ophaalpunt",
        TRANSIT_CENTER: "Transitcentrum",
        RANDOM_POINT: "Willekeurig punt"
    }


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150, null=True)
    capacity = models.IntegerField(null=True)
    type = enum.EnumField(LocationType, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
