from django.db import models
from .location import Location
from django_enumfield import enum


class VehicleType(enum.Enum):
    BIKE = 0
    CAR = 1
    SCOOTER = 2
    BUS = 3
    TRAIN = 4

    __labels__ = {
        BIKE: "Deelfiets",
        CAR: "Deelauto",
        SCOOTER: "Deelscooter",
        BUS: "Bus",
        TRAIN: "Trein"
    }


class Status(enum.Enum):
    AVAILABLE = 0
    BOOKED = 1
    IN_USE = 2
    IN_MAINTENANCE = 3
    OUT_OF_SERVICE = 4
    LOST = 5

    __labels__ = {
        AVAILABLE: "Beschikbaar",
        BOOKED: "Gereserveerd",
        IN_USE: "In gebruik",
        IN_MAINTENANCE: "In onderhoud",
        OUT_OF_SERVICE: "Buiten dienst",
        LOST: "Verloren"
    }


class Condition(enum.Enum):
    GOOD = 0
    FAIR = 1
    POOR = 2

    __labels__ = {
        GOOD: "Goed",
        FAIR: "Prima",
        POOR: "Slecht"
    }


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, to_field='location_id')
    type = enum.EnumField(VehicleType)
    model = models.CharField(max_length=100, null=True)
    license_plate = models.CharField(max_length=6)
    status = enum.EnumField(Status, null=True)
    info = models.TextField(null=True)
    condition = enum.EnumField(Condition, null=True)
    charging_level = models.IntegerField(null=True)
    capacity = models.IntegerField(null=True)
    date_of_purchase = models.DateField(null=True)
    insurance_info = models.TextField(null=True)
    maintenance_history = models.TextField(null=True)

    def update_status(self, new_status):
        self.status = new_status
        self.save()

    def update_condition(self, new_condition):
        self.condition = new_condition
        self.save()

    def __str__(self):
        return f"{self.vehicle_id}. A {self.type}  "


