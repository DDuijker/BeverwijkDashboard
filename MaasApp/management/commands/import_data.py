import csv
from django.core.management.base import BaseCommand
from MaasApp.models import EnqueteResponse
from datetime import datetime


class Command(BaseCommand):
    help = 'Import data from a CSV file into the EnqueteResponse model'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']

        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file, delimiter=';')  # Adjust delimiter if necessary

            for row in csv_reader:
                start_time_str = row.get('begintijd', None)
                completion_time_str = row.get('eindtijd', None)
                last_modified_time_str = row.get('laatste_wijziging', None)

                # Convert string to datetime
                start_time = datetime.strptime(start_time_str, '%m-%d-%y %H:%M:%S') if start_time_str else None
                completion_time = datetime.strptime(completion_time_str,
                                                    '%m-%d-%y %H:%M:%S') if completion_time_str else None
                last_modified_time = datetime.strptime(last_modified_time_str,
                                                       '%m-%d-%y %H:%M:%S') if last_modified_time_str else None

                # Create an EnqueteResponse instance and populate fields from the CSV
                enquete_response = EnqueteResponse(
                    respondent_id=row.get('ID', None),
                    start_time=start_time,
                    completion_time=completion_time,
                    email=row.get('email', None),
                    name=row.get('naam', None),
                    last_modified_time=last_modified_time,
                    origin=row.get('afkomst', None),
                    age=row.get('leeftijd', None),
                    travel_frequency=row.get('frequentie_vervoersmiddelen', None),
                    available_transportation=row.get('bezit_vervoerswijzen', None),
                    most_used_transport_modes=row.get('vervoerswijzen_frequentie_volgorde', None),
                    consider_shared_mobility=row.get('deelmobiliteit_wil_gebruiken', None),
                    maas_app_used=row.get('maas_app_gebruikt', None),
                    maas_usage_frequency=row.get('eerder_gebruikt_maas', None),
                    maas_app_advantages=row.get('maas_app_gebruikt', None),
                    cost_overview_value_added=row.get('behoefte_kosten_overzicht', None),
                    satisfaction_transport_modes=row.get('tevredenheid', None),
                    survey_comments=row.get('opmerkingen', None),
                )

                # Save the EnqueteResponse instance to the database
                enquete_response.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully imported data for respondent {row.get("ID")}'))
