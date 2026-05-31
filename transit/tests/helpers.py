import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from transit.models import Bus, Chofer, Ruta, Viaje, Cooperativa


def create_user(username='user', email=None, password='Pass1234!', **kwargs):
    email = email or f'{username}_{random.randint(1000, 9999)}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, **kwargs
    )


def create_staff(username='staff', email=None, password='Admin1234!'):
    email = email or f'{username}_{random.randint(1000, 9999)}@test.com'
    return User.objects.create_user(
        username=username, email=email, password=password, is_staff=True
    )


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def auth_client(user):
    client = APIClient()
    access, _ = get_tokens(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return client


def create_cooperativa(name=None, is_active=True):
    if name is None:
        name = f"Cooperativa-{random.randint(100, 999)}"
    return Cooperativa.objects.create(
        name=name, is_active=is_active
    )


def create_ruta(name=None, origin='Quito', destination='Guayaquil', base_fare=15.00, is_active=True):
    if name is None:
        name = f"Ruta-{random.randint(1000, 9999)}"
    return Ruta.objects.create(
        name=name, origin=origin, destination=destination, base_fare=base_fare, is_active=is_active
    )


def create_bus(unit_number=None, plate=None, model='Mercedes', status='ACTIVE', capacity=40):
    if unit_number is None:
        unit_number = f"C-{random.randint(1000, 9999)}"
    if plate is None:
        plate = f"PBA-{random.randint(1000, 9999)}"
    return Bus.objects.create(
        unit_number=unit_number, plate=plate, model=model, status=status, capacity=capacity
    )


def create_chofer(first_name='Juan', last_name='Pérez', license_number=None, is_active=True, daily_rate=35.00):
    if license_number is None:
        license_number = f"{random.randint(1000000000, 9999999999)}"
    return Chofer.objects.create(
        first_name=first_name, last_name=last_name, license_number=license_number, is_active=is_active, daily_rate=daily_rate
    )


def create_viaje(bus=None, chofer=None, ruta=None, status='scheduled', passenger_count=0, departure_time=None, estimated_arrival=None):
    if bus is None: bus = create_bus()
    if chofer is None: chofer = create_chofer()
    if ruta is None: ruta = create_ruta()
    
    if departure_time is None:
        departure_time = timezone.now()
    if estimated_arrival is None:
        estimated_arrival = departure_time + timedelta(hours=2)
        
    return Viaje.objects.create(
        bus=bus,
        chofer=chofer,
        ruta=ruta,
        status=status,
        passenger_count=passenger_count,
        departure_time=departure_time,
        estimated_arrival=estimated_arrival
    )