from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register the models
admin.site.register(User, UserAdmin)
admin.site.register(Booking)
# admin.site.register(BookingStatus)
admin.site.register(Location)
# admin.site.register(LocationType)
admin.site.register(Vehicle)
# admin.site.register(VehicleType)
# admin.site.register(Status)
# admin.site.register(Condition)
admin.site.register(Payment)
# admin.site.register(PaymentStatus)


