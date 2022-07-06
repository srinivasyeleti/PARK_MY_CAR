from django.shortcuts import render

from .models import parking_slot, SLOT_COLUMN, SLOT_ROW, Vehicle, Booking_model, Bike, Car

from django.template.defaulttags import register

from .forms import SlotBookingForm, add_car_form, add_bike_form, changeParkingForm

from django.shortcuts import redirect

from account.models import Account

from datetime import datetime, date

import random

random_ids = []

# import tkinter
# from tkinter import messagebox

# import pyautogui as pag

# Create your views here.
# home view,
def home_view(request):
    return render(request, 'siteHome.html', {})

def user_home_view(request):
    context = {}

    if request.user.is_authenticated :
        the_vehicles = Vehicle.objects.filter(owner=request.user)
        context['the_vehicles'] = the_vehicles

        for the_vehicle in the_vehicles :
            if the_vehicle.parked :
                the_slot = parking_slot.objects.get(slot_id=the_vehicle.parked_slot_id)
                now = datetime.now().time()
                print("curr time : " + str(now))
                print("end time : " + str(the_slot.end_time))
                # when a slot is booked with wrong time, the_slot.end_time is initialized None and the_vehicle is parked,
                # when the user home page is refreshed the_slot in which the_vehicle is parked is checked but its end_time is None,
                # datetime object is compared with NoneType object and so error comes,
                if now > the_slot.end_time :
                    print("late ")
                    
                    the_vehicle.parked = False
                    the_vehicle.parked_slot_id = None
                    the_vehicle.save()
                    
                    the_slot.is_occupied = False
                    the_slot.vehicle_id = None
                    the_slot.available_increment = 60
                    the_slot.booked_time = None
                    the_slot.end_time = None
                    the_slot.save()
                else :
                    print("not late")

    return render(request, 'userHome.html', context)


def aboutus_view(request) :
    return render(request, 'aboutus.html', {})

def slot_status_view(request) :
    slots = parking_slot.objects.filter(parking_vehicle="car")
    for slot in slots :
        if Vehicle.objects.filter(vehicle_id=slot.vehicle_id).count() == 0 :
            slot.is_occupied = False
            slot.vehicle_id = None
            slot.save()
        
    context = {}
    context['slots'] = slots
    context['col'] = SLOT_COLUMN
    context['row'] = SLOT_ROW
    return render(request, 'personal/slot_status.html', context)

def bike_slot_status_view(request) :
    # slot = parking_slot.objects.get(slot_id="04")
    # print(slot.vehicle_id)
    # print(Vehicle.objects.filter(vehicle_id=slot.vehicle_id).count())

    slots = parking_slot.objects.filter(parking_vehicle="bike")
    for slot in slots :
        if Vehicle.objects.filter(vehicle_id=slot.vehicle_id).count() == 0 :
            slot.is_occupied = False
            slot.vehicle_id = None
            slot.save()

    context = {}
    context['slots'] = slots
    context['col'] = SLOT_COLUMN
    context['row'] = SLOT_ROW
    return render(request, 'personal/bike_slot_status.html', context)

@register.filter
def my_get(i, j) :
    slots = parking_slot.objects.all()
    ind1 = i - 1
    ind2 = j - 1
    slot_ind = ind1*8 + ind2
    return slots[slot_ind]

@register.filter
def my_get_2(i, j) :
    slots = parking_slot.objects.all()
    ind1 = i - 1
    ind2 = j - 1
    slot_ind = 32 + ind1*8 + ind2
    return slots[slot_ind]

def getSlotType(slot_id) :
    if slot_id[0] == '0' or slot_id[0] == '1' or slot_id[0] == '2' or slot_id[0] == '3' :
        type = "bike"
    else :
        type = "car"
    print("it is a slot for " + type)
    return type

def slot_booking_view(request, slot_id) :
    context = {}
    username = request.user.username
    # try :
    #     the_owner = Account.objects.get(username=username)
    # except Account.DoesNotExist :
    #     the_owner = None
    
    random_id = random.randint(1000, 9999)
    while(random_id in random_ids) :
        random_id = random.randint(1000, 9999)
    random_ids.append(random_id)

    now = datetime.now().time() # time object

    if request.POST :
        form = SlotBookingForm(request.POST, initial={'slot_id' : slot_id, 'username' : username})

        if form.is_valid() :
            form.save()

            vehicle_flag = False
            the_vehicle_id = request.POST['vehicle_id']
            the_vehicles = Vehicle.objects.filter(owner=request.user)
            the_slot = parking_slot.objects.get(slot_id=slot_id)

            type = getSlotType(slot_id)
            # type = the_slot.parking_vehicle
            # print(the_slot.parking_vehicle + "      " + type)

            if type == "bike" :
                the_bikes = Bike.objects.filter(owner=request.user)
                for bike in the_bikes :
                    if the_vehicle_id == bike.vehicle_id :
                        vehicle_flag = True
                        break
            if type == "car" :
                the_cars = Car.objects.filter(owner=request.user)
                for car in the_cars :
                    if the_vehicle_id == car.vehicle_id :
                        vehicle_flag = True
                        break

            if vehicle_flag :
                the_vehicle = Vehicle.objects.get(vehicle_id=the_vehicle_id)

                # check if this vehcile is not parked,
                if the_vehicle.parked :
                    print("vehicle already parked")
                    return redirect('userHome')
                else :
                    print("vehicle not parked")

                    # end_time_time = datetime.strptime(the_slot.end_time, '%H:%M').time()
                    end_time_time = datetime.strptime(request.POST['end_time'], '%H:%M').time()
                    if now > end_time_time :          # not supported operand,
                        print("not future time")
                        return redirect('userHome')
                    print("future time")
                    # update the_vehicle object,
                    the_vehicle.parked = True
                    the_vehicle.parked_slot_id = slot_id
                     # after updating save in DB,
                    the_vehicle.save()
                    print(the_vehicle.parked)

                    # update the user's 'booked_slot' field,
                    # the_slot = parking_slot.objects.get(slot_id=slot_id)
                    the_slot.booked_time = now
                    the_slot.is_occupied = True
                    the_slot.vehicle_id = the_vehicle_id
                    the_slot.end_time = request.POST['end_time']

                    print("availabe increment " + str(the_slot.available_increment))
                    the_slot.save()
                    print(the_slot.vehicle_id + " " + str(the_slot.end_time))

                    # create a new booking,
                    booking = Booking_model(
                        booking_id = "bkng" + str(random_id),
                        vehicle_id=the_slot.vehicle_id,
                        slot_id = slot_id,
                        booked_time = now,
                        # want_to_book_the_slot=True,
                        username=request.user.username,
                        # booked_time = now,
                    )
                    
                    # booking.booking_id = "bkng" + str(slot_id) + str(the_vehicle_id)
                    booking.save()

                    return redirect('userHome')
                    # return render(request, 'userHome.html', context)

            else :
                print("no vehicle (or) booking not compatible")
                # context['booking_form'] = form
                return redirect('userHome')

        else :
            print("not valid")
            print(form.errors)
            context['booking_form'] = form

    else :
        # form = SlotBookingForm(initial={'booking_id' : random_id, 'slot_id' : slot_id, 'username' : username})
        form = SlotBookingForm(initial={'slot_id' : slot_id, 'username' : username})
        context['booking_form'] = form
    
    return render(request, 'personal/slot_booking.html', context)


def add_bike_view(request) :
    context = {}

    if request.POST :
        form = add_bike_form(request.POST)

        if form.is_valid() :
            form.save()

            # there is some error in "on or off" Vs "True or False",
            if request.POST.get('geared') == 'on' :
                geared = True
            else :
                geared = False

            # print(Vehicle.objects.all().count())

            new_bike = Bike(
                vehicle_id = request.POST['vehicle_id'],
                company = request.POST['company'],
                vehicle_model = request.POST['vehicle_model'],
                owner = request.user,
                geared = geared,
            )

            new_bike.save()

            # print(Vehicle.objects.all().count())

            return redirect('userHome')

        else :
            print("not valid")
            print(form.errors)
            context['add_bike_form'] = form

    else :
        form = add_bike_form()
        context['add_bike_form'] = form

    return render(request, 'personal/add_bike.html', context)

def add_car_view(request) :
    context = {}

    if request.POST :
        form = add_car_form(request.POST)

        if form.is_valid() :
            form.save()

            # there is some error in "on or off" Vs "True or False",
            if request.POST.get('auto_gear') == 'on' :
                auto_gear = True
            else :
                auto_gear = False

            if request.POST.get('auto_trans') == 'on' :
                auto_trans = True
            else :
                auto_trans = False

            # print(Vehicle.objects.all().count())

            new_car = Car(
                vehicle_id = request.POST['vehicle_id'],
                company = request.POST['company'],
                vehicle_model = request.POST['vehicle_model'],
                owner = request.user,
                auto_gear = auto_gear,
                auto_trans = auto_trans,
            )

            new_car.save()

            # print(Vehicle.objects.all().count())

            return redirect('userHome')

        else :
            context['add_car_form'] = form

    else :
        form = add_car_form()
        context['add_car_form'] = form

    return render(request, 'personal/add_car.html', context)


def all_vehicles_view(request) :
    vehicles = Vehicle.objects.filter(owner=request.user)
    context = {}
    context['vehicles'] = vehicles
    # context['']

    return render(request, 'personal/all_vehicles.html', context)

def all_bookings_view(request) :
    bookings = Booking_model.objects.all()
    context = {}
    context['bookings'] = bookings

    return render(request, 'personal/all_bookings.html', context)


def changeParkingView(request, parked_slot_id) :
    context = {}
    context['icn'] = False
    the_vehicle = Vehicle.objects.get(parked_slot_id=parked_slot_id)
    the_slot = parking_slot.objects.get(slot_id=parked_slot_id)
    actual_end_time = the_slot.end_time
    now = datetime.now().time() # time object
    # the_vehicle = queryset.first()

    if request.POST :
        print("post")
        form = changeParkingForm(request.POST, instance = the_vehicle)
        print(request.POST.get('is_occupied') == None)
        print(request.POST.get('slt_id'))
        print(request.POST.get('end_time'))
        # print(request.POST.get('is_occupied'))
        # form.save()
        if request.POST.get('is_occupied') == None :
            # print(the_vehicle.parked)
            the_vehicle.parked = False
            # print(the_vehicle.parked)
            the_vehicle.parked_slot_id = None
            the_vehicle.save()

            
            # print(the_slot)
            the_slot.is_occupied = False
            the_slot.vehicle_id = None
            the_slot.available_increment = 60
            the_slot.booked_time = None
            the_slot.end_time = None
            # the_slot.slot_id = None
            the_slot.save()
            # print(the_slot.is_occupied)

        else :
            print("\nnot change occ")
            print("time of booking : " + str(the_slot.booked_time))
            changed_end_time = datetime.strptime(request.POST.get('end_time'), '%H:%M:%S').time()
            if changed_end_time < actual_end_time and changed_end_time > now :
                print("time ok")
                the_slot.end_time = changed_end_time
                the_slot.save()
            else :
                if changed_end_time > actual_end_time :
                    print("ooh increasing,,,")
                    delta = datetime.combine(date.today(), changed_end_time) - datetime.combine(date.today(), actual_end_time)

                    if the_slot.available_increment - delta.seconds/60 > 0 :
                        print("\nincrement available : " + str(the_slot.available_increment))
                        print("time diff in minutes : " + str(delta.seconds/60))
                        # upadte the available_increment,
                        the_slot.available_increment = the_slot.available_increment - delta.seconds/60
                        # print("remaining : " + str(the_slot.available_increment))

                        the_slot.end_time = changed_end_time

                        the_slot.save()

                    else :
                        context['icn'] = True
                        # return render(request, 'personal/icnMsg.html', {})
                        print("\nincrement not available")
                else :
                    print("\ntime not ok")
        print("remaining : " + str(the_slot.available_increment))
        print("now end time : " + str(the_slot.end_time))

        return redirect('userHome')

    else :
        print("else")
        form = changeParkingForm(
            initial= {
                "slot_id" : the_vehicle.parked_slot_id,
                "is_occupied" : the_vehicle.parked,
                "vehicle_id" : the_vehicle.vehicle_id,
                "end_time" : the_slot.end_time,
            }
        )
        context['changeParkingForm'] = form
    # print("icn : " + str(context['icn']))
    return render(request, 'personal/change_parking_status.html', context)