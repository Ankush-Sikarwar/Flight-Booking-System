from django.shortcuts import render, redirect, reverse, HttpResponse
from home.models import Route, Seat, Schedule, Flight
from booking.models import Booking, Payment
from django.contrib import messages
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import get_user
from django.utils import timezone

# Create your views here.
def booking(request, route_id, schedule_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission outside this window is not allowed 😎")
    route = Route.objects.get(pk=route_id)
    schedule = Schedule.objects.get(pk=schedule_id)
    allSeats = Seat.objects.filter(flight=schedule.flight, is_available=True).order_by(
        "seat_number"
    )
    if request.method == "POST":
        user = request.user
        
        total_price = request.POST.get("total_price")
        travel_date = request.POST.get("travel_date")

        seat_ids = request.POST.getlist("seat_ids")
        seats = Seat.objects.filter(id__in=seat_ids)
        print(seats)

        booking = Booking.objects.create(
            user=user,
            schedule=schedule,
            total_seats=seats.count(),
            amount=total_price,
            travel_date=travel_date,
        )
        booking.seats.set(seats)
        for seat in seats:
            seat.is_available = False
            seat.save()
        booking.save()

        messages.success(request, "Success  😎")
        return redirect(makePayment, booking.pk)
    context = {
        "route": route,
        "allSeats": allSeats,
        "schedule": schedule,
    }
    return render(request, "booking/booking.html", context)


def makePayment(request, booking_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission without login is not allowed ")
    
    book = Booking.objects.get(id=booking_id)
    if request.method == "POST":
        method = request.POST.get("method")
        upi_id = request.POST.get("upi_id")
        card_holder_name = request.POST.get("card_holder_name")
        card_number = request.POST.get("card_number")
        expiry_date = request.POST.get("expiry_date")
        cvv = request.POST.get("cvv")
        status = "paid"
        if upi_id or (card_holder_name and card_number and expiry_date and cvv):
            payment = Payment.objects.create(
                booking_id=booking_id, method=method, amount=book.amount, status=status
            )
            payment.save()
            book.status = "confirmed"
            book.save()
            messages.success(request, "confirmed  😎")
            return redirect(bookingConfirmation, book.pk)
    method_choices = Payment.METHOD_CHOICES
    context = {
        "book": book,
        "method_choices": method_choices,
    }
    return render(request, "booking/payment.html", context)


def cancelBookingRefund(request, booking_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission without login is not allowed ")
    
    booking = Booking.objects.get(id=booking_id)
    payment = Payment.objects.get(booking=booking)
    context = {
        'booking': booking,
        'payment': payment,
    }
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')
        context = {
            'booking': booking,
            'payment': payment,
            'bank_name': bank_name,
            'account_number': account_number,
            'ifsc_code': ifsc_code,
        }
        # Perform the refund process here using the bank details provided.
        # For this example, we'll just update the booking status to "cancelled".
        booking.status = 'cancelled'
        booking.save()

        return render(request, "booking/refund.html", context)
    
    return render(request, "booking/cancel.html", context)

def cancelBooking(request, booking_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission without login is not allowed ")
    
    booking = Booking.objects.get(id=booking_id)
    
    if request.method == 'POST':
        return redirect('cancelBookingRefund', booking_id)

    context = {
        'booking': booking,
    }
    return render(request, "booking/cancel.html", context)



def bookingConfirmation(request, booking_id):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission without login is not allowed ")
    
    book = Booking.objects.get(id=booking_id)
    context = {
        "book": book,
    }
    return render(request, "booking/confirm.html", context)


def allBookings(request):
    middleware = AuthenticationMiddleware(get_user)
    middleware.process_request(request)
    if not request.user.is_authenticated:
        return HttpResponse("Submission without login is not allowed ")
   
    user= request.user
    allBookings=Booking.objects.filter(user=user)
    context = {"allBookings":allBookings,
               'current_time': timezone.now()
               }
    return render(request, "booking/all_booking.html", context)
