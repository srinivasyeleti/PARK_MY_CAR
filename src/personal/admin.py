from django.contrib import admin
from .models import (
    Vehicle,
    Car,
    Bike,
    Person,
    parking_slot,
    Booking_model,
)

from .forms import parkingForm

# Register your models here.
class vehicleAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner', 'parked_slot_id', 'parked')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class bikeAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class carAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Vehicle, vehicleAdmin)
admin.site.register(Car, carAdmin)
admin.site.register(Bike, bikeAdmin)

class PersonAdmin(admin.ModelAdmin) :
    list_display = ('name', 'age', 'address')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# admin.site.register(Person, PersonAdmin)

class Booking_modelAdmin(admin.ModelAdmin) :
    list_display = ('booking_id', 'slot_id', 'vehicle_id', 'username', 'booked_time')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Booking_model, Booking_modelAdmin)

class parkingSlotAdmin(admin.ModelAdmin) :
    form = parkingForm
    list_display = ('slot_id', 'is_occupied', 'vehicle_id', 'booked_time', 'end_time', 'available_increment', 'parking_vehicle')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(parking_slot, parkingSlotAdmin)
