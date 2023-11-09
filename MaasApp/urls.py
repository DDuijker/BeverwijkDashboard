from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.all_users, name='users'),
    path('users/details/<int:request_id>', views.user_details, name='details'),
    path('testing/', views.testing, name='testing'),
]
