from django.db import models
from .user import User
from django_enumfield import enum


class PaymentStatus(enum.Enum):
    PENDING = 0
    SUCCESS = 1
    FAILED = 2
    REFUNDED = 3

    __labels__ = {
        PENDING: "Afwachtend voor betaling",
        SUCCESS: "Succesvol",
        FAILED: "Gefaald",
        REFUNDED: "Terugbetaling"
    }


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField()
    status = enum.EnumField(PaymentStatus, default=PaymentStatus.PENDING)

    def change_status(self, new_status):
        self.status = new_status
        self.save()
