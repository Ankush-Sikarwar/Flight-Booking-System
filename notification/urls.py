from django.urls import path
from notification import views

# app_name = 'home'
urlpatterns = [
    path(
        "show_user_notifications",
        views.show_user_notifications,
        name="show_user_notifications",
    ),
]
