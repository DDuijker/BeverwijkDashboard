from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User


def index(request):
    """Loads the index page"""
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def all_users(request):
    """Loads the all_users template with an object containing the users object"""
    users = User.objects.all().values()
    template = loader.get_template('users.html')
    context = {
        'users': users
    }
    return HttpResponse(template.render(context, request))


def bikes(request):
    template = loader.get_template('bikes.html')
    return HttpResponse(template.render())


def cars(request):
    template = loader.get_template('cars.html')
    return HttpResponse(template.render())


def scooters(request):
    template = loader.get_template('scooters.html')
    return HttpResponse(template.render())


def trains(request):
    template = loader.get_template('trains.html')
    return HttpResponse(template.render())


def busses(request):
    template = loader.get_template('busses.html')
    return HttpResponse(template.render())


def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))


def user_details(request, request_id):
    user = User.objects.get(id=request_id)
    template = loader.get_template('user_details.html')
    context = {
        'user': user
    }
    return HttpResponse(template.render(context, request))
