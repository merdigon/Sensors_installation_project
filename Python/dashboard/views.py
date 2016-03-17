from django.shortcuts import render
from sensorApp.models import SensorOption, SensorHistory, SensorRegistration, Sensor
from scenarioApp.models import Scenario
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from sensorApp.forms import SensorAddForm, SensorRegistrationForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .tools import send_status_change_signal_to_sensor, send_value_change_signal_to_sensor, send_add_sensor_signal, \
    register_sensor, scenario_triggered, send_remove_sensor_signal


@login_required
def home_view(request):
    sensors = SensorOption.objects.all().order_by('sensor')
    scenarios = Scenario.objects.all()
    scenarios_dct = []
    thermometers = SensorOption.objects.filter(sensor__sensor_type__name='Thermometer')
    time_24_hours_ago = timezone.now() - timezone.timedelta(days=1)
    thermometers_history = SensorHistory.objects.filter(sensor_option__in=thermometers, date__gte=time_24_hours_ago)
    no_problems = True
    warnings = 0
    errors = 0
    for scenario in scenarios:
        if scenario_triggered(scenario):
            scenarios_dct.append(scenario)
            if scenario.is_warning:
                warnings += 1
            else:
                errors += 1
    if warnings > 0 or errors > 0:
        no_problems = False
    return render(request, "dashboard.html", {"no_problems": no_problems, "warnings": warnings, "errors": errors,
                                              "sensors": sensors, "thermometers": thermometers,
                                              "thermometers_history": thermometers_history,
                                              "scenarios": scenarios_dct})


@login_required
def registration_view(request):
    time_5_minutes_ago = timezone.now() - timezone.timedelta(minutes=5)
    registration = SensorRegistration.objects.filter(registered=False, date__gte=time_5_minutes_ago).order_by('-date').first()
    if request.method == "POST":
        form = SensorRegistrationForm(request.POST)
        if form.is_valid():
            register_sensor(registration.sensor_type, registration.sensor_id, form.cleaned_data['sensor_name'])
            registration.registered = True
            messages.success(request, 'Sensor registered')
            HttpResponseRedirect("/")
    else:
        form = SensorRegistrationForm()
    return render(request, "registration.html", {'registration': registration, 'form': form})


@login_required
def sensor_control_view(request):
    sensors = SensorOption.objects.all().order_by('sensor')
    if request.method == "POST":
        add_form = SensorAddForm(request.POST)
        if add_form.is_valid():
            if send_add_sensor_signal(unicode(add_form.cleaned_data['sensor_type'])):
                messages.success(request, 'Signal sent')
            else:
                messages.error(request, 'Error while sending signal')
                add_form = SensorAddForm(request.POST)
    else:
        add_form = SensorAddForm()
    return render(request, "sensor_control.html", {"sensors": sensors, "add_form": add_form})


@csrf_exempt
def sensor_change_signal(request, sensor_id, option):
    if send_status_change_signal_to_sensor(sensor_id, option):
        return HttpResponse()
    else:
        return HttpResponse(status=500)


@csrf_exempt
def sensor_change_value_signal(request, sensor_id, option, value):
    if send_value_change_signal_to_sensor(sensor_id, option, value):
        return HttpResponse()
    else:
        return HttpResponse(status=500)


@login_required
def sensor_history_view(request):
    sensors_history = SensorHistory.objects.all().order_by('-date')
    return render(request, "sensor_history.html", {"sensors_history": sensors_history})


@login_required
def sensor_remove_view(request):
    sensors = Sensor.objects.all()
    return render(request, "sensor_remove.html", {"sensors": sensors})


@login_required
def sensor_remove_id_view(request, sensor_id):
    if send_remove_sensor_signal(sensor_id):
        Sensor.objects.filter(sensor_id=sensor_id).delete()
    else:
        messages.error(request, 'Error while sending remove signal')
    return HttpResponseRedirect('/sensor_remove/')

