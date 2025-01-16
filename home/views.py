from django.shortcuts import render
from .models import Schedule, Route
from django.db.models import Q
from datetime import datetime
# Create your views here.
def homeView(request):
    routes = Route.objects.all()
    schedules = Schedule.objects.all().order_by("source_departure_datetime")
    context = {
        "AllSchedules": schedules,
        "routes": routes,
    }
    return render(request, "home/index.html", context)


def AllRoutes(request):
    query = request.GET.get('q')
    source_location = request.GET.get('source_location')
    destination_location = request.GET.get('destination_location')

    routes = Route.objects.all()
    filters = Q()
    if source_location:
        filters &= Q(departure_location__icontains=source_location)
    if destination_location:
        filters &= Q(arrival_location__icontains=destination_location)
    
    print(filters)

    routes = routes.filter(filters).order_by("departure_location")
    context = {
        "AllRoutes": routes,
    }
    return render(request, "home/all_routes.html", context)


def allSchedules(request, pk):
    route = Route.objects.get(id=pk)
    AllSchedules = Schedule.objects.filter(route=route).order_by("source_departure_datetime")

    context = {
        "AllSchedules": AllSchedules,
        "route": route,
    }
    return render(request, "home/all_schedules.html", context)

def search(request):
    query = request.GET.get('q')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    source_location = request.GET.get('source_location')
    destination_location = request.GET.get('destination_location')

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    except ValueError:
        start_date, end_date = None, None

    schedules = Schedule.objects.all()
    filters = Q()
    if start_date:
        filters &= Q(source_departure_datetime__date__gte=start_date)
    if end_date:
        filters &= Q(source_departure_datetime__date__lte=end_date)
    if source_location:
        filters &= Q(route__departure_location__icontains=source_location)
    if destination_location:
        filters &= Q(route__arrival_location__icontains=destination_location)
    
    print(filters)

    schedules = schedules.filter(filters).order_by("source_departure_datetime")

    context = {
        "AllSchedules": schedules,
        "query": query,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "source_location": source_location,
        "destination_location": destination_location,
    }

    return render(request, "home/index.html", context)
