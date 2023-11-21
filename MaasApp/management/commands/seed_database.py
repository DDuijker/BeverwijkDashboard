from django.core.management.base import BaseCommand
from MaasApp.management.commands.seeding_data.location_data import locations_data
from MaasApp.management.commands.seeding_data.user_data import users_data
from MaasApp.management.commands.seeding_data.vehicle_data import vehicles_data
from MaasApp.models import Location
from MaasApp.models import User
from MaasApp.models import Vehicle


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        """This function fills the database with dummy data"""

        for user_data in users_data:
            # Check if the user already exists
            if not User.objects.filter(username=user_data['username']).exists():
                # Create the user
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                )

                self.stdout.write(self.style.SUCCESS(f'User {user.username} created successfully.'))
        for location_data in locations_data:
            # Check if the location already exists
            if not Location.objects.filter(name=location_data['name']).exists():
                # Create the location
                location = Location.objects.create(**location_data)

                self.stdout.write(self.style.SUCCESS(f'Location {location.name} created successfully.'))

        for vehicle_data in vehicles_data:
            # Check if the vehicle already exists
            if not Vehicle.objects.filter(license_plate=vehicle_data['license_plate']).exists():
                # Create the vehicle
                vehicle = Vehicle.objects.create(**vehicle_data)

                self.stdout.write(self.style.SUCCESS(f'Vehicle {vehicle.license_plate} created successfully.'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
