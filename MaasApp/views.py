import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .services.graph_generator_service import GraphGeneratorService
from .templatetags import custom_filters
from .models import User, EnqueteResponse
from collections import Counter
plt.switch_backend('Agg')


def index(request):
    """Loads the index page"""

    # Define your data for the categories and values
    categories = ['Jan', 'Feb', 'Mrt', 'Apr', 'Mei', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov',
                  'Dec']  # Days of the week in Dutch
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
    # Sample data for all charts
    categories_and_values = [
        {
            'categories': ['Haarlem', 'Alkmaar', 'Zandvoort'],
            'values': [0.8, 0.2, 0.1],
            'x_label': 'Gemeente',
            'y_label': '% ritten dat is gestart in de gemeente\nmaar eindigt in een andere gemeente',
            'title': 'Ritten over de gemeentelijke grens'
        },
        {
            'categories': ['Beverwijk', 'Wijk aan Zee', 'Haarlem', 'Heemskerk'],
            'values': [92.7, 6.5, 0.5, 0.3],
            'x_label': 'Gemeente',
            'y_label': '% ritten dat is gestart in de gemeente\nmaar eindigt in een andere gemeente',
            'title': 'Ritten over de gemeentelijke grens'
        },
        {
            'categories': ['Q2', 'Q3'],
            'values': [36, 37],
            'x_label': 'kwartalen',
            'y_label': 'aantal voertuigen',
            'title': 'Aantal voertuigen in de gemeente'
        },
        {
            'categories': ['Q2', 'Q3'],
            'values': [87.5, 84],
            'x_label': 'kwartalen',
            'y_label': 'gemiddelde percentage operationele scooters',
            'title': 'Operationele voertuigen'
        },
        {
            'categories': ['April', 'Mei', 'Juni', 'Juli', 'Augustus', "September"],
            'values': [1490, 1500, 1919, 1582, 1629, 953],
            'x_label': 'maanden',
            'y_label': 'aantal ritten',
            'title': 'totaal aantal ritten dat er in de gemeente is gemaakt '
        },
        {
            'categories': ['April', 'Mei', 'Juni', 'Juli', 'Augustus', "September"],
            'values': [1.64, 1.55, 2.2, 2.0, 1.9, 1.3],
            'x_label': 'maanden',
            'y_label': 'gemiddelde gebruikersratio van de scooters',
            'title': 'Gebruikersratio'
        },
        {
            'categories': ['Q2', 'Q3'],
            'values': [3820, 3877],
            'x_label': 'kwartalen',
            'y_label': 'aantal klanten',
            'title': 'totaal aantal klanten'
        },
        {
            'categories': ['Q2', 'Q3'],
            'values': [503, 413],
            'x_label': 'kwartalen',
            'y_label': 'aantal nieuwe klanten',
            'title': 'totaal aantal nieuwe klanten'
        },
        {
            'categories': ['April', 'Mei', 'Juni', 'Juli', 'Augustus', "September"],
            'values': [517, 489, 609, 561, 544, 359],
            'x_label': 'maanden',
            'y_label': 'totaal aantal actieve gebruikers',
            'title': 'Actieve gebruikers'
        }
    ]

    # Generate bar charts for all data sets
    bar_charts = []
    for data_set in categories_and_values:
        chart = GraphGeneratorService.generate_bar_chart(
            data_set['categories'], data_set['values'],
            x_label=data_set['x_label'],
            y_label=data_set['y_label'],
            title=data_set['title']
        )
        bar_charts.append(chart)

    # Pass all image data to the template
    context = {f'graph_{i+1}': chart for i, chart in enumerate(bar_charts)}

    return render(request, 'pages/scooters.html', context)

def trains(request):
    template = loader.get_template('./pages/trains.html')
    return HttpResponse(template.render())


def busses(request):
    return render(request, './pages/other-ov.html')


def enquete(request):
    all_answers = EnqueteResponse.objects.all()
    satisfaction = []
    considered_maas_options = []

    for answer in all_answers:
        considered_maas_options.append(answer.consider_shared_mobility)
        satisfaction_value = answer.satisfaction_transport_modes.strip()
        if satisfaction_value:
            try:
                rating = int(float(satisfaction_value))
                satisfaction.append(rating)
            except ValueError:
                # Handle the case when the value is not a valid number
                pass

    avg_satisfaction = round((float(sum(satisfaction) / len(satisfaction)) if satisfaction else 0.0), 2)

    # Count occurrences of each maas_option
    maas_options_counts = Counter(considered_maas_options)

    # Extract categories and values for the pie chart
    maas_options = list(maas_options_counts.keys())
    maas_options_counts = Counter(considered_maas_options)

    # Remove Nvt from option counts
    for key in list(maas_options_counts):
        if key == 'Nvt':
            del maas_options_counts[key]
    print(maas_options_counts)

    maas_options_values = [count for option, count in maas_options_counts.items() if option != 'Nvt']

    circle_diagram = GraphGeneratorService.generate_pie_chart(
        categories=maas_options_counts,
        values=maas_options_values,
        title="Meeste interesse in deelmobiliteit:"
    )

    context = {
        'all_answers': all_answers,
        'avg_satisfaction': avg_satisfaction,
        'circle_diagram': circle_diagram
    }
    template = loader.get_template('./pages/enquete_answers.html')
    return HttpResponse(template.render(context, request))



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
