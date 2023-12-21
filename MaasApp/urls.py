from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.all_users, name='users'),
    path('users/details/<int:request_id>', views.user_details, name='details'),
    path('deelfietsen', views.bikes, name='bikes'),
    path('deelautos', views.cars, name='cars'),
    path('deelscooters', views.scooters, name='scooters'),
    path('treinen', views.trains, name='trains'),
    path('overig-ov', views.busses, name='busses'),
    path('testing/', views.testing, name='testing'),
    path('enquete/', views.enquete, name='enquete'),
    path('components/gismap/roadmap/roadmap/index.html', TemplateView.as_view(template_name='components/gismap/roadmap/roadmap/index.html'), name='roadmap_index')
]
