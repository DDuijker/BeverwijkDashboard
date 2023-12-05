from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64


def index(request):
    """Loads the index page"""
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def all_users(request):
    """Loads the all_users template with an object containing the users object"""
    users = User.objects.all().values()
    template = loader.get_template('./pages/users.html')
    context = {
        'users': users
    }
    return HttpResponse(template.render(context, request))


def bikes(request):
    # Sample data
    categories = ['ma', 'di', 'wo', 'do', 'vr', 'za', 'zo']
    values = [100, 200, 150, 120, 180, 90, 160]

    # Set the background color
    plt.figure(facecolor='#F8F8F8')

    # Plotting the bar chart with styling options
    bars = plt.bar(categories, values,
                   color=['#696A8F', '#696A8F', '#696A8F', '#696A8F', '#696A8F', '#696A8F', '#696A8F'],
                   edgecolor='#B0B1C3', linewidth=1.2, alpha=0.7)

    # Set individual colors for each bar
    bars[1].set_color('#B0B1C3')
    bars[3].set_color('#B0B1C3')
    bars[5].set_color('#B0B1C3')

    plt.xlabel('Dagen van de week', fontsize=12, color='#696A8F')
    plt.ylabel('aantal ritten', fontsize=12, color='#696A8F')
    plt.title('Ritten per dag', fontsize=14, color='#696A8F')
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Set static values on the y-axis
    static_y_values = [0, 50, 100, 150, 200, 250]
    plt.yticks(static_y_values)

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    img_data = base64.b64encode(image_stream.read()).decode('utf-8')

    plt.close()  # Close the plot to free up resources

    # Pass the image data to the template
    context = {
        'graph': img_data,
    }

    return render(request, 'pages/bikes.html', context)

def cars(request):
    template = loader.get_template('./pages/cars.html')
    return HttpResponse(template.render())


def scooters(request):
    template = loader.get_template('./pages/scooters.html')
    return HttpResponse(template.render())


def trains(request):
    template = loader.get_template('./pages/trains.html')
    return HttpResponse(template.render())


def busses(request):
    return render(request, './pages/other-ov.html')


def testing(request):
    template = loader.get_template('template.html')
    context = {
        'fruits': ['Apple', 'Banana', 'Cherry'],
    }
    return HttpResponse(template.render(context, request))


def user_details(request, request_id):
    user = User.objects.get(id=request_id)
    template = loader.get_template('./pages/user_details.html')
    context = {
        'user': user
    }
    return HttpResponse(template.render(context, request))

