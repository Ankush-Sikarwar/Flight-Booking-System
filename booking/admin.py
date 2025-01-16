from django.contrib import admin
from booking.models import Booking, Payment

# Register your models here.
class BookingAdmin(admin.ModelAdmin):
    search_fields=('schedule', 'status', 'travel_date', 'source_location',)
    list_filter=('user', 'travel_date', 'source_location','destination_location','schedule', 'status','amount','total_seats','seats', )
class PaymentAdmin(admin.ModelAdmin):
    search_fields=('booking', 'status', 'amount',)
    list_filter=('booking', 'status', 'created_at', 'amount', 'method',)


admin.site.register(Booking, BookingAdmin)
admin.site.register(Payment, PaymentAdmin)
# admin.site.register(Cancellation)
