from django import forms

from .models import parking_slot, Vehicle, Booking_model, SLOT_CHOICES
from account.models import Account

class parkingForm(forms.ModelForm) :
    # vehicle_id = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="(Nothing)", required=False)
    parking_vehicle = forms.ChoiceField(choices=SLOT_CHOICES)
    # booked_time = forms.TimeField(required=False)
    # end_time = forms.TimeField(required=False)
    class Meta :
        model = parking_slot
        fields = ('slot_id', 'parking_vehicle')

class SlotBookingForm(forms.ModelForm) :
    slot_id = forms.CharField(max_length=10, disabled=True)
    username = forms.CharField(max_length=20, disabled=True)
    end_time = forms.TimeField()
    # booking_id = forms.CharField(max_length=10, disabled=True)
    want_to_book_the_slot = forms.BooleanField(initial=False)   
    # the_owner = Account.objects.get(username="user1")

    class Meta :
        model = Booking_model
        # fields = ('booking_id', 'username', 'slot_id', 'want_to_book_the_slot', 'vehicle_id', 'end_time')
        fields = ('username', 'slot_id', 'want_to_book_the_slot', 'vehicle_id', 'end_time')


class add_bike_form(forms.ModelForm) :
    geared = forms.BooleanField(initial=False, required=False)
    class Meta :
        model = Vehicle
        fields = ('vehicle_id', 'company', 'vehicle_model', 'geared')

class add_car_form(forms.ModelForm) :
    auto_gear = forms.BooleanField(initial=False, required=False)
    auto_trans = forms.BooleanField(initial=False, required=False)
    class Meta :
        model = Vehicle
        fields = ('vehicle_id', 'company', 'vehicle_model', 'auto_trans', 'auto_gear')

class changeParkingForm(forms.ModelForm) :
    vehicle_id = forms.CharField(max_length=20, disabled=True)
    slot_id = forms.CharField(max_length=10, disabled=True)

    # vehicle_id = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="(Nothing)", required=False, dis)
    class Meta :
        model = parking_slot
        fields = ('slot_id', 'is_occupied', 'vehicle_id', 'end_time')

    def save(self) :
        print("saving")
        print(self.is_valid())