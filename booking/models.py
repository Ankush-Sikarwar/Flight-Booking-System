from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from notification.models import Notification

# Create your models here.
from django.db import models
from home.models import Schedule, Seat
from accounts.models import User

from django.core.mail import send_mail
from flight_booking import settings

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_location = models.CharField(max_length=100)
    destination_location = models.CharField(max_length=100)
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True)
    seats = models.ManyToManyField(Seat)
    total_seats = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    travel_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to set the departure_location
        and arrival_location.
        """
        self.source_location = self.schedule.route.departure_location
        self.destination_location = self.schedule.route.arrival_location
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.username} - {self.source_location} to {self.destination_location}"


@receiver(pre_delete, sender=Booking)
def set_seats_available(sender, instance, **kwargs):
    for seat in instance.seats.all():
        seat.is_available = True
        seat.save()

@receiver(post_save, sender=Booking)
def create_notification(sender, instance, created, **kwargs):
    if created and instance.status == "confirmed":
        # New booking was created with confirmed status
        message = f"Your booking ({instance.id}) has been confirmed."
        subject = f"Booking confirmation ({instance.id})"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]
        notification_type = "booking_confirmed"
        send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                # fail_silently=False,
            )
        
    elif not created and instance.status == "confirmed":
        # Booking status was updated to confirmed
        message = f"Your booking ({instance.id}) has been confirmed."
        subject = f"Booking confirmation ({instance.id})"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]
        notification_type = "booking_confirmed"
        send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                # fail_silently=False,
            )
        
    elif not created and instance.status == "pending":
        # Booking status was updated to pending
        message = f"Your payment is {instance.status}"
        notification_type = "booking_updated"
        
    elif not created and instance.status == "cancelled":
        # Booking status was updated to cancelled
        message = f"Your booking ({instance.id}) has been cancelled."
        notification_type = "booking_cancelled"
        send_mail(
                f"Booking cancelation ({instance.id})",
                message,
                settings.EMAIL_FROM,
                [instance.user.email],
                fail_silently=False,
            )
    else:
        # No new notification needed
        return
    
    # Create the notification object
    Notification.objects.create(
        user=instance.user,
        message=message,
        notification_type=notification_type
    )

@receiver(post_save, sender=Booking)
def update_schedule_total_available_seats_on_flight(sender, instance, **kwargs):
    schedule = instance.schedule
    total_available_seats_on_flight = schedule.flight.seat_set.filter(
        is_available=True
    ).count()
    schedule.total_available_seats_on_flight = total_available_seats_on_flight
    schedule.save()


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    )

    METHOD_CHOICES = (
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("upi", "UPI"),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking.user.username} - {self.booking.schedule.route.departure_location} to {self.booking.schedule.route.arrival_location} - {self.amount}"


