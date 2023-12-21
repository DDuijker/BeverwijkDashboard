import matplotlib.pyplot as plt
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from .services.generate_color_service import GenerateColorService
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
    # Sample data
    categories = ['Beverwijk', 'Wijk aan Zee', 'Haarlem', 'Heemskerk']
    values = [92.7, 6.5, 0.5, 0.3]

    # Generate bar chart
    bar_chart = GraphGeneratorService.generate_bar_chart(
        categories, values, x_label="Gemeente",
        y_label="% ritten dat is gestart in de gemeente\nmaar eindigt in een andere gemeente",
        title="Ritten over de gemeentelijke grens"
    )

    # Pass the image data to the template
    context = {
        'graph': bar_chart,
    }
    return render(request, 'pages/scooters.html', context)
    # template = loader.get_template('./pages/scooters.html')
    # return HttpResponse(template.render())


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

    for line in input_data:  # Replace 'your_data' with the actual variable containing your data
        modes_and_percentages = [mode.strip() for mode in line.strip(';').split(';')]

        for index, mode in enumerate(modes_and_percentages):
            # Create a dictionary entry for each mode
            if mode not in data_dict:
                data_dict[mode] = 0

            # Accumulate rankings (in reverse order, so the most used gets the highest ranking)
            data_dict[mode] += len(modes_and_percentages) - index

    # Sort the dictionary by values (total rankings) in descending order
    sorted_data_dict = dict(sorted(data_dict.items(), key=lambda item: item[1], reverse=True))

    # Calculate y_ticks based on the range from the lowest to the highest value
    min_value = min(sorted_data_dict.values())
    max_value = max(sorted_data_dict.values())
    y_ticks = list(range(50, max_value + 10, 25))

    # remove the parentheses from the keys
    keys = []
    for key in list(sorted_data_dict.keys()):
        keys.append(GenerateColorService.remove_words_in_parentheses(key))

    chart_data = GraphGeneratorService.generate_bar_chart(
        categories=keys,
        values=list(sorted_data_dict.values()),
        x_label="Vervoerswijzen",
        y_label="Totaal gebruik",
        title="Meest gebruikte vervoerswijzen",
        y_ticks= y_ticks,
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
