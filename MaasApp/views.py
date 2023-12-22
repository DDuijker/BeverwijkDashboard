import matplotlib.pyplot as plt
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.conf import settings
from pathlib import Path
from django.templatetags.static import static

from .services.generate_color_service import GenerateColorService
from .services.graph_generator_service import GraphGeneratorService
from .templatetags import custom_filters
from .models import User, EnqueteResponse, Vehicle
from collections import Counter
from .static.scooterData import scooter_data

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

    # --------------------SCOOTER GRAPHS----------------------------
    bar_charts = []
    for data_set in scooter_data:
        chart = GraphGeneratorService.generate_bar_chart(
            data_set['categories'], data_set['values'],
            x_label=data_set['x_label'],
            y_label=data_set['y_label'],
            title=data_set['title']
        )
        bar_charts.append(chart)

    # ------------------------ENQUETE GRAPH-----------------------------
    all_answers = EnqueteResponse.objects.all()
    satisfaction = []
    considered_maas_options = []
    input_data = []

    for answer in all_answers:
        considered_maas_options.append(answer.consider_shared_mobility)
        satisfaction_value = answer.satisfaction_transport_modes.strip()
        input_data.append(answer.most_used_transport_modes)
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

    data_dict = {}

    for line in input_data:
        modes_and_percentages = [mode.strip() for mode in line.strip(';').split(';')]

        for index, mode in enumerate(modes_and_percentages):
            # Create a dictionary entry for each mode
            if mode not in data_dict:
                data_dict[mode] = 0

            # Accumulate rankings (in reverse order, so the most used gets the highest ranking)
            data_dict[mode] += len(modes_and_percentages) - index

    # Calculate the total count of all rankings
    total_rankings = sum(data_dict.values())

    # Convert rankings to percentages
    percentage_data_dict = {mode: (count / total_rankings) * 100 for mode, count in data_dict.items()}

    # Sort the dictionary by values (total percentages) in descending order
    sorted_percentage_data_dict = dict(sorted(percentage_data_dict.items(), key=lambda item: item[1], reverse=True))

    # Calculate y_ticks based on the range from the lowest to the highest percentage
    max_percentage = int(max(sorted_percentage_data_dict.values()))
    y_ticks = list(range(0, max_percentage + 10, 5))

    # Remove the parentheses from the keys
    keys = [GenerateColorService.remove_words_in_parentheses(key) for key in sorted_percentage_data_dict.keys()]

    chart_data = GraphGeneratorService.generate_bar_chart(
        categories=keys,
        values=list(sorted_percentage_data_dict.values()),
        x_label="Vervoerswijzen",
        y_label="Totaal gebruik (%)",
        title="Meest gebruikte vervoerswijzen",
        y_ticks=y_ticks,
        grid=True,
        grid_alpha=0.5,
        size=(12, 5),
        color='#F0F0F0'
    )
    context = {
        'line_graph': graph,
        'circle_chart': circle_chart,
        **{f'graph_{i + 1}': chart for i, chart in enumerate(bar_charts)},
        'avg_satisfaction': avg_satisfaction,
        'circle_diagram': circle_diagram,
        'chart_data': chart_data
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

    # Get all the bike data from vehicles
    all_bikes = Vehicle.objects.filter(type=0)

    # Pass the image data to the template
    context = {
        'graph': bar_chart,
        'all_bikes': all_bikes
    }

    return render(request, 'pages/bikes.html', context)


def cars(request):
    template = loader.get_template('./pages/cars.html')
    return HttpResponse(template.render())


def scooters(request):
    # Generate bar charts for all data sets
    bar_charts = []
    for data_set in scooter_data:
        chart = GraphGeneratorService.generate_bar_chart(
            data_set['categories'], data_set['values'],
            x_label=data_set['x_label'],
            y_label=data_set['y_label'],
            title=data_set['title']
        )
        bar_charts.append(chart)

    # Pass all image data to the template
    context = {

        f'graph_{i + 1}': chart for i, chart in enumerate(bar_charts)

    }

    return render(request, './pages/scooters.html', context)


def trains(request):
    template = loader.get_template('./pages/trains.html')
    return HttpResponse(template.render())


def busses(request):
    return render(request, './pages/other-ov.html')


def enquete(request):
    all_answers = EnqueteResponse.objects.all()
    satisfaction = []
    considered_maas_options = []
    input_data = []

    for answer in all_answers:
        considered_maas_options.append(answer.consider_shared_mobility)
        satisfaction_value = answer.satisfaction_transport_modes.strip()
        input_data.append(answer.most_used_transport_modes)
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

    data_dict = {}

    for line in input_data:
        modes_and_percentages = [mode.strip() for mode in line.strip(';').split(';')]

        for index, mode in enumerate(modes_and_percentages):
            # Create a dictionary entry for each mode
            if mode not in data_dict:
                data_dict[mode] = 0

            # Accumulate rankings (in reverse order, so the most used gets the highest ranking)
            data_dict[mode] += len(modes_and_percentages) - index

    # Calculate the total count of all rankings
    total_rankings = sum(data_dict.values())

    # Convert rankings to percentages
    percentage_data_dict = {mode: (count / total_rankings) * 100 for mode, count in data_dict.items()}

    # Sort the dictionary by values (total percentages) in descending order
    sorted_percentage_data_dict = dict(sorted(percentage_data_dict.items(), key=lambda item: item[1], reverse=True))

    # Calculate y_ticks based on the range from the lowest to the highest percentage
    max_percentage = int(max(sorted_percentage_data_dict.values()))
    y_ticks = list(range(0, max_percentage + 10, 5))

    # Remove the parentheses from the keys
    keys = [GenerateColorService.remove_words_in_parentheses(key) for key in sorted_percentage_data_dict.keys()]

    chart_data = GraphGeneratorService.generate_bar_chart(
        categories=keys,
        values=list(sorted_percentage_data_dict.values()),
        x_label="Vervoerswijzen",
        y_label="Totaal gebruik (%)",
        title="Meest gebruikte vervoerswijzen",
        y_ticks=y_ticks,
        grid=True,
        grid_alpha=0.5,
        size=(12, 5),
        color='#F0F0F0'
    )

    context = {
        'all_answers': all_answers,
        'avg_satisfaction': avg_satisfaction,
        'circle_diagram': circle_diagram,
        'chart_data': chart_data
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
