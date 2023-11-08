from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def all_users(request):
    """Loads the all_users template with an object containing the users object"""
    users = User.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'users': users
    }
    return HttpResponse(template.render(context, request))
