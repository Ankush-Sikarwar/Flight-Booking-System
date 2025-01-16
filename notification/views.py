from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from notification.models import Notification


def show_user_notifications(request):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorize user 😎")
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by("-created_at")
    count = notifications.count()
    context = {
        "notifications": notifications,
        "count": count,
    }
    html = render_to_string("notification/notifications.html", context)
    return HttpResponse(html)
