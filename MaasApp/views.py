import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .services.graph_generator_service import GraphGeneratorService
from .models import User

plt.switch_backend('Agg')


def index(request):
    """Loads the index page"""

    # Define your data for the categories and values
    categories = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt',  'Nov', 'Dec']  # Days of the week in Dutch
    values = [120, 150, 180, 200, 230, 170, 190, 120, 40, 400, 430, 380]  # Example number of rides per day

    graph = GraphGeneratorService.make_line_graph(
        x_values=categories, y_values=values,
        x_label="Maanden",
        y_label="Aantal ritten",
        title="MaaS gebruik per maand",
        y_ticks=[0, 50, 100, 200, 300, 400, 500]
    )

    circle_categories = ['Auto', 'Fiets', 'Scooters', 'Treinen', 'Overig ov']
    circle_values = [200, 180, 10, 150, 100]

    circle_chart = GraphGeneratorService.generate_pie_chart(
        circle_categories, circle_values, "Verdeling vervoersmiddelen"
    )
    context = {
        'line_graph': graph,
        'circle_chart': circle_chart
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


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

    # Generate bar chart
    bar_chart = GraphGeneratorService.generate_bar_chart(
        categories, values, x_label="Dag", y_label="Ritten", title="Ritten per dag"
    )

    # Pass the image data to the template
    context = {
        'graph': bar_chart,
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

def enquete(request):
    template = loader.get_template('./pages/enquete_answers.html')
    return HttpResponse(template.render())

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
