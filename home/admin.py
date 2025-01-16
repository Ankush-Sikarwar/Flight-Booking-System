from django.contrib import admin
from home.models import (
    Flight,
    Route,
    Schedule,
    Seat,
)

class FlightAdmin(admin.ModelAdmin):
    list_display=('name','flight_no',)
    list_filter=('capacity', 'type', 'name', 'flight_no',)
    
class SeatAdmin(admin.ModelAdmin):
    search_fields=('flight__flight_no',)
    list_filter=('flight_class','flight__name',"is_available",)
    
class RouteAdmin(admin.ModelAdmin):
    list_filter=('arrival_location','departure_location',)
    
class ScheduleAdmin(admin.ModelAdmin):
    search_fields=('flight__name', 'flight__flight_no', 'route__departure_location', 'route__arrival_location',)
    list_filter=('flight__name', 'flight__flight_no','route__departure_location','route__arrival_location','total_available_seats_on_flight','destination_arrival_datetime', 'source_departure_datetime','duration',)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Seat, SeatAdmin)
