# myapp/management/commands/import_data.py
import csv
from django.core.management.base import BaseCommand
from MaasApp.models import EnqueteResponse


class Command(BaseCommand):
    help = 'Import data from CSV file into EnqueteResponse model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                respondent_id = row['ID'],
                start_time = row['Begintijd']
                completion_time = row['Tijd van voltooien']
                email = row['E-mail']
                name = row['Naam']
                last_modified_time = row['Tijd van laatste wijziging']
                origin = row['Waar komt u vandaan?']
                age = row['Wat is uw leeftijd?']
                travel_frequency = [
                    'Hoe vaak reist u momenteel met verschillende vervoerswijzen (bv fiets naar station, vervolgens trein naar Amsterdam en tot slot OV-fiets naar bestemming) in ��n enkele reis?']
                available_transportation = row['Welke vervoersmiddelen heeft u zelf tot uw beschikking?']
                most_used_transport_modes = row['''Welke vervoerswijzen gebruikt u het meeste in het dagelijks leven?�
Selecteer op plaats 1 welk vervoerswijze u het vaakst gebruikt en op plek 10 welke u het minst vaak gebruikt.�''']
                consider_shared_mobility = row[
                    'Welke vorm van deelmobiliteit die u nog niet gebruikt, zou u het snelst overwegen?']
                maas_app_used = row['''Heeft u bij het plannen van uw reizen weleens gebruik gemaakt van een MaaS-applicatie?�

Een MaaS-applicatie verzamelt de�verschillende transportmiddelen op ��n platform. Denk hierbij aan alle tra...''']
                maas_usage_frequency = row['''Hoe vaak heeft u in het verleden van een MaaS-applicatie gebruik gemaakt?
''']
                maas_app_advantages = row[
                    '''Via een MaaS-applicatie krijgt u direct inzicht hoe u het snelst op uw locatie kan komen doordat alle vervoersmiddelen in ��n applicatie gebundeld zijn om uw reis te plannen. U kan het zien als ee...''']
                cost_overview_value_added = row['''Nog een voordeel van MaaS is dat alle kosten die u maakt aan reizen in kaart worden gebracht.
Heeft dit een toegevoegde waarde voor u om deze kosten in ��n overzicht te kunnen overzien?�''']
                satisfaction_transport_modes = row['''Hoe tevreden bent u met de beschikbaarheid van de verschillende aangeboden vervoerwijzen binnen de gemeente Beverwijk?
''']
                survey_comments = row['''Heeft u nog op- of aanmerking over deze enquete/ dit onderzoek?
''']

                # Create an instance of the model and save it
                response = EnqueteResponse(
                    respondent_id=respondent_id,
                    start_time=start_time,
                    completion_time=completion_time,
                    email=email,
                    name=name,
                    last_modified_time=last_modified_time,
                    origin=origin,
                    age=age,
                    travel_frequency=travel_frequency,
                    available_transportation=available_transportation,
                    most_used_transport_modes=most_used_transport_modes,
                    consider_shared_mobility=consider_shared_mobility,
                    maas_app_used=maas_app_used,
                    maas_usage_frequency=maas_usage_frequency,
                    maas_app_advantages=maas_app_advantages,
                    cost_overview_value_added=cost_overview_value_added,
                    satisfaction_transport_modes=satisfaction_transport_modes,
                    survey_comments=survey_comments
                )
                response.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
