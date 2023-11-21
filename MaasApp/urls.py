from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gebruikers/', views.all_users, name='users'),
    path('gebruikers/details/<int:request_id>', views.user_details, name='details'),
    path('deelfietsen', views.bikes, name='bikes'),
    path('deelautos', views.cars, name='cars'),
    path('deelscooters', views.scooters, name='scooters'),
    path('treinen', views.trains, name='trains'),
    path('overig-ov', views.busses, name='busses'),
    path('testing/', views.testing, name='testing'),
]
