from django.db import models
from django_enumfield import enum
from .user import User
from .vehicle import Vehicle
from .payment import Payment
from .location import Location


class BookingStatus(enum.Enum):
    PENDING = 0
    CONFIRMED = 1
    CANCELED = 2
    COMPLETED = 3
    NO_SHOW = 4
    IN_PROGRESS = 5
    REJECTED = 6
    EXPIRED = 7

    __labels__ = {
        PENDING: "In afwachting",
        CONFIRMED: "Bevestigd",
        CANCELED: "Geannuleerd",
        COMPLETED: "Voltooid",
        NO_SHOW: "Niet op komen dagen",
        IN_PROGRESS: "In uitvoering",
        REJECTED: "Afgewezen",
        EXPIRED: "Verlopen"
    }


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=None)
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.SET_DEFAULT, default=None)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='pickup_bookings')
    dropoff_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True,
                                         related_name='dropoff_bookings')
    status = enum.EnumField(BookingStatus, default=BookingStatus.PENDING)
    payment_id = models.ForeignKey(Payment, on_delete=models.SET_DEFAULT, default=None, null=True)

    def __str__(self):
        return f"Booking nr: {self.booking_id}, from {self.username}"
