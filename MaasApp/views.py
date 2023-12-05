import numpy as np
from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from django.shortcuts import render
import matplotlib.pyplot as plt
from io import BytesIO
import base64

plt.switch_backend('Agg')


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


def generate_bar_chart(categories, values, special_bars=None, x_label=None, y_label=None, title=None,
                       y_ticks=None, grid=True, grid_alpha=0.5):
    # Set the background color
    plt.figure(facecolor='#F8F8F8')

    # Use a colormap to generate colors dynamically
    colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))

    # Plotting the bar chart with styling options
    bars = plt.bar(categories, values, color=colors, edgecolor='#B0B1C3', linewidth=1.2, alpha=0.7)

    # Set individual colors for specific bars
    if special_bars:
        for i in special_bars:
            bars[i].set_color('#B0B1C3')

    # Style the plot
    style_chart(x_label, y_label, title, y_ticks, grid, grid_alpha)

    # Save the plot to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    img_data = base64.b64encode(image_stream.read()).decode('utf-8')
    plt.close()  # Close the plot to free up resources

    return img_data


def style_chart(x_label, y_label, title, y_ticks, grid, grid_alpha):
    plt.xlabel(x_label, fontsize=12, color='#696A8F')
    plt.ylabel(y_label, fontsize=12, color='#696A8F')
    plt.title(title, fontsize=14, color='#696A8F')

    if grid:
        plt.grid(axis='y', linestyle='--', alpha=grid_alpha)

    if y_ticks is not None:
        plt.yticks(y_ticks)


def bikes(request):
    # Sample data
    categories = ['ma', 'di', 'wo', 'do', 'vr', 'za', 'zo']
    values = [100, 200, 150, 120, 180, 90, 160]

    # Generate bar chart
    img_data = generate_bar_chart(categories, values, special_bars=[1, 3, 5], y_ticks=[0, 50, 100, 150, 200, 250],
                                  x_label='Dagen van de week', y_label='Aantal ritten', title='Ritten per dag')

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
