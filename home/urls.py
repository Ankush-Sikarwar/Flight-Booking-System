from django.urls import path
from home import views

# app_name = 'home'
urlpatterns = [
    path("", views.homeView, name="homeView"),
    path("all_routes/", views.AllRoutes, name="all_routes"),
    path("all_schedules/<int:pk>", views.allSchedules, name="all_schedules"),
    path('search/', views.search, name='search'),
]
