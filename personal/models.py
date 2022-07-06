from django.db import models

from account.models import Account

SLOT_COLUMN = 8
SLOT_ROW = 4

SLOT_CHOICES = (
                    ("bike", "bike"),
                    ("car", "car"),
            )

# Create your models here.
class Vehicle(models.Model) :
    vehicle_id = models.CharField(primary_key=True, max_length=20, unique=True)
    company = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=20)
    price = models.IntegerField(blank=True, null=True)
    parked = models.BooleanField(default=False)
    parked_slot_id = models.CharField(max_length=10, null=True)

    # many vehicles can be owned by one owner,
    owner = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.company + " " + self.vehicle_model + "[" + self.vehicle_id + "]"


class Car(Vehicle) :
    auto_gear = models.BooleanField(default=False)
    auto_trans = models.BooleanField(default=False)

    def __str__(self):
        return self.vehicle_model + "[" + self.vehicle_id + "]"

class Bike(Vehicle) :
    geared = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle_model + "[" + self.vehicle_id + "]"

class Person(models.Model) :
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=30)
    # gender = models.

    def __str__(self):
        return self.name

class parking_slot(models.Model) :
    parking_vehicle = models.CharField(max_length=5, null=True)
    booked_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    slot_id = models.CharField(max_length=10, primary_key=True)
    is_occupied = models.BooleanField(default=False)
    # parked_vehicle = models.ForeignKey(Vehicle, default=None, blank=True, on_delete=models.CASCADE)
    available_increment = models.PositiveSmallIntegerField(default=60)
    vehicle_id = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return "slot " + "[" + self.slot_id + "]"

class Booking_model(models.Model) :
    booking_id = models.CharField(max_length=10, null=True)
    slot_id = models.CharField(max_length=10)
    # want_to_book_the_slot = models.BooleanField(default=False)    
    vehicle_id = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=20, null=True)
    expired = models.BooleanField(default=False)
    booked_time = models.TimeField(null=True)
    # end_time = models.TimeField(null=True)

    def __str__(self):
        return str(self.booking_id) + "[" + self.username + "]"

    
