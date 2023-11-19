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


class PaymentMethod(enum.Enum):
    IDEAL = 0
    PAYPAL = 1
    CREDIT_CARD = 2
    BANK_TRANSFER = 3

    __labels__ = {
        IDEAL: "iDeal",
        PAYPAL: "PayPal",
        CREDIT_CARD: "Credit card",
        BANK_TRANSFER: "Overmaken naar bank"
    }


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField()
    payment_method = enum.EnumField(PaymentMethod, default=PaymentMethod.IDEAL)
    status = enum.EnumField(PaymentStatus, default=PaymentStatus.PENDING)

    def change_status(self, new_status):
        self.status = new_status
        self.save()
