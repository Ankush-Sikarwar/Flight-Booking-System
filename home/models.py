from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class Flight(models.Model):
    flight_no = models.CharField(max_length=50, unique=True)
    flight_TYPES = [
        ("low cost carrier", "low cost carrier"),
        ("full service", "full service"),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=flight_TYPES)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.flight_no}"


class Seat(models.Model):
    SEAT_CATEGORIES = [
        ("window_seat", "window_seat"),
        ("aisle_seat", "aisle_seat"),
    ]
    FLIGHT_CLASS = [
        ("economy", "economy"),
        ("premium_economy", "premium_economy"),
        ("business", "business"),
        ("first", "first"),
    ]
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seat_set")
    seat_number = models.CharField(max_length=10)
    flight_class = models.CharField(max_length=20, choices=FLIGHT_CLASS)
    category = models.CharField(max_length=20, choices=SEAT_CATEGORIES)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["flight", 'flight_class', "seat_number"]

    def __str__(self):
        return f"{self.seat_number} - {self.flight.name} - ({self.flight_class})"

    def save(self, *args, **kwargs):
        if self.flight_class == "economy":
            self.price = 100.0
        elif self.flight_class == "premium_economy":
            self.price = 150.0
        elif self.flight_class == "business":
            self.price = 200.0
        elif self.flight_class == "first":
            self.price = 250.0 

        super().save(*args, **kwargs)


@receiver(post_save, sender=Flight)
def create_seats(sender, instance, created, **kwargs):
    if created or instance.capacity != instance.seat_set.count():
        Seat.objects.filter(flight=instance).delete()
        economy_percentage = 0.4
        premium_economy_percentage = 0.3
        business_percentage = 0.2
        first_percentage = 0.1
        economy_seats = int(instance.capacity * economy_percentage)
        premium_economy_seats = int(instance.capacity * premium_economy_percentage)
        business_seats = int(instance.capacity * business_percentage)
        first_seats = int(instance.capacity * first_percentage)
        for i in range(economy_seats):
            Seat.objects.create(
                flight=instance,
                seat_number=str(i + 1),
                flight_class="economy",
                category="aisle_seat" if i % 2 == 0 else "window_seat",
            )
        for i in range(economy_seats, economy_seats + premium_economy_seats):
            Seat.objects.create(
                flight=instance,
                seat_number=str(i + 1),
                flight_class="premium_economy",
                category="aisle_seat" if i % 2 == 0 else "window_seat",
            )
        for i in range(economy_seats + premium_economy_seats, economy_seats + premium_economy_seats + business_seats):
            Seat.objects.create(
                flight=instance,
                seat_number=str(i + 1),
                flight_class="business",
                category="aisle_seat" if i % 2 == 0 else "window_seat",
            )
        for i in range(economy_seats + premium_economy_seats + business_seats, instance.capacity):
            Seat.objects.create(
                flight=instance,
                seat_number=str(i + 1),
                flight_class="first",
                category="aisle_seat" if i % 2 == 0 else "window_seat",
            )


class Route(models.Model):
    departure_location = models.CharField(max_length=100)
    arrival_location = models.CharField(max_length=100)
    distance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.departure_location} - {self.arrival_location}"


class Schedule(models.Model):
    flight = models.OneToOneField(Flight, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    source_departure_datetime = models.DateTimeField()
    destination_arrival_datetime = models.DateTimeField()
    duration = models.DurationField(null=True, blank=True)
    total_seats_on_flight = models.IntegerField(null=True, blank=True)
    total_available_seats_on_flight = models.IntegerField(null=True, blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["source_departure_datetime"]

    def __str__(self):
        return f"{self.flight.name} - {self.route.departure_location} to {self.route.arrival_location} - {self.source_departure_datetime} - {self.destination_arrival_datetime}"

    def clean(self):
        if (
            self.destination_arrival_datetime
            and self.source_departure_datetime
            and self.source_departure_datetime >= self.destination_arrival_datetime
        ):
            raise ValidationError("Departure datetime must be less than Arival datetime.")

    def get_duration(self):
        """
        Returns the duration between the arrival time and the departure time
        as a timedelta object.
        """
        if self.destination_arrival_datetime and self.source_departure_datetime:
            # arrival = datetime.combine(datetime.today(), self.arrival_time)
            # departure = datetime.combine(datetime.today(), self.departure_time)
            # duration = arrival - departure
            duration = self.destination_arrival_datetime - self.source_departure_datetime
            return duration

    def save(self, *args, **kwargs):
        """
        Overrides the save method to calculate and set the duration field
        based on the arrival and departure times.
        """
        self.total_seats_on_flight = self.flight.capacity
        self.total_available_seats_on_flight = self.flight.seat_set.filter(
            is_available=True
        ).count()
        self.duration = self.get_duration()
        super().save(*args, **kwargs)
