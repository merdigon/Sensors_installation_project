from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import SensorOption, SensorHistory, SensorRegistration, SensorType

def api_sensor_status_change(request, sensor_id, option, value):
    sensor = get_object_or_404(SensorOption, sensor__sensor_id=sensor_id, option=option)
    triggered = sensor.triggered
    if value == "true":
        sensor.triggered = True
    else:
        sensor.triggered = False
    sensor.save()
    sensor_history = SensorHistory()
    sensor_history.sensor_option = sensor
    if value == "true":
        sensor_history.triggered = True
    else:
        sensor_history.triggered = False
    sensor_history.date = timezone.now()
    sensor_history.save()
    return HttpResponse()


def api_sensor_value_change(request, sensor_id, option, value):
    sensor = get_object_or_404(SensorOption, sensor__sensor_id=sensor_id, option=option)
    sensor.integer_value = int(value)
    sensor.save()
    sensor_history = SensorHistory()
    sensor_history.triggered = False
    sensor_history.sensor_option = sensor
    sensor_history.integer_value = int(value)
    sensor_history.date = timezone.now()
    sensor_history.save()
    return HttpResponse()


def api_sensor_registration(request, sensor_id, sensor_type):
    sensor_type = get_object_or_404(SensorType, name=sensor_type)
    registration = SensorRegistration()
    registration.date = timezone.now()
    registration.sensor_type = sensor_type
    registration.sensor_id = sensor_id
    registration.registered = False
    registration.save()
    return HttpResponse()