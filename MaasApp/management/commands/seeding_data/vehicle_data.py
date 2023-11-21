import random
from datetime import datetime, timedelta
from ..seeding_data.location_data import locations_data
from MaasApp.models.vehicle import Status, Condition, VehicleType
from MaasApp.models.location import LocationType, Location

vehicles_data = [
    {
        'type': VehicleType.CAR,
        'model': 'Tesla Model 3',
        'license_plate': 'AB-123-CD',
        'status': Status.AVAILABLE,
        'info': 'Electric car with autopilot feature.',
        'condition': Condition.GOOD,
        'charging_level': 100,
        'capacity': 5,
        'date_of_purchase': datetime.now() - timedelta(days=365),
        'insurance_info': 'Insured by XYZ Insurance.',
        'maintenance_history': 'Last maintenance on ' + str(datetime.now() - timedelta(days=60)),
    },
    {
        'type': VehicleType.BIKE,
        'model': 'VanMoof S3',
        'license_plate': 'BIKE-456',
        'status': Status.IN_USE,
        'info': 'Electric bike with automatic electronic shifting.',
        'condition': Condition.FAIR,
        'charging_level': 75,
        'capacity': 1,
        'date_of_purchase': datetime.now() - timedelta(days=180),
        'insurance_info': 'Insured by ABC Insurance.',
        'maintenance_history': 'Last maintenance on ' + str(datetime.now() - timedelta(days=30)),
    },
    {
        'type': VehicleType.SCOOTER,
        'model': 'Segway Ninebot',
        'license_plate': 'SCOOT-789',
        'status': Status.IN_MAINTENANCE,
        'info': 'Electric scooter with a range of up to 40 miles.',
        'condition': Condition.POOR,
        'charging_level': 20,
        'capacity': 1,
        'date_of_purchase': datetime.now() - timedelta(days=90),
        'insurance_info': 'Insured by DEF Insurance.',
        'maintenance_history': 'Last maintenance on ' + str(datetime.now() - timedelta(days=15)),
    },
    {
        'type': VehicleType.BUS,
        'model': 'Mercedes-Benz Citaro',
        'license_plate': 'BUS-012',
        'status': Status.OUT_OF_SERVICE,
        'info': 'City bus with a capacity of up to 100 passengers.',
        'condition': Condition.FAIR,
        'charging_level': None,
        'capacity': 100,
        'date_of_purchase': datetime.now() - timedelta(days=730),
        'insurance_info': 'Insured by GHI Insurance.',
        'maintenance_history': 'Last maintenance on ' + str(datetime.now() - timedelta(days=120)),
    },
    {
        'type': VehicleType.TRAIN,
        'model': 'NS Sprinter Lighttrain',
        'license_plate': 'TRAIN-345',
        'status': Status.AVAILABLE,
        'info': 'Local train with a capacity of up to 300 passengers.',
        'condition': Condition.GOOD,
        'charging_level': None,
        'capacity': 300,
        'date_of_purchase': datetime.now() - timedelta(days=1460),
        'insurance_info': 'Insured by JKL Insurance.',
        'maintenance_history': 'Last maintenance on ' + str(datetime.now() - timedelta(days=180)),
    },
]

