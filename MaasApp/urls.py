from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.all_users, name='users'),
    path('users/details/<int:request_id>', views.user_details, name='details'),
    path('bikes', views.bikes, name='bikes'),
    path('cars', views.cars, name='cars'),
    path('scooters', views.scooters, name='scooters'),
    path('trains', views.trains, name='trains'),
    path('busses', views.busses, name='busses'),
    path('testing/', views.testing, name='testing'),
]
