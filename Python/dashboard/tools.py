import json, socket
from django.conf import settings
from sensorApp.models import Sensor, SensorConstantOption, SensorType, SensorOption
from scenarioApp.models import ScenarioElement


def send_status_change_signal_to_sensor(sensor_id, option):
    try:
        json_message = json.dumps({'signal': 'change_status', 'sensor_id': sensor_id, 'option': option})
        send_message(json_message)
        return True
    except:
        return False


def send_value_change_signal_to_sensor(sensor_id, option, value):
    try:
        json_message = json.dumps({'signal': 'change_status', 'sensor_id': sensor_id, 'option': option, 'value': value})
        send_message(json_message)
        return True
    except:
        return False


def send_add_sensor_signal(sensor_type):
    try:
        json_message = json.dumps({'signal': 'add_sensor', 'sensor_type': sensor_type})
        send_message(json_message)
        return True
    except:
        return False


def send_remove_sensor_signal(sensor_id):
    try:
        json_message = json.dumps({'signal': 'kill_sensor', 'sensor_id': sensor_id})
        send_message(json_message)
        return True
    except:
        return False


def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.replace(" ", ""), (settings.SENSOR_SERVER_IP, settings.SENSOR_SERVER_PORT))
    print message


def register_sensor(sensor_type, sensor_id, sensor_name):
    sensor_to_register = Sensor()
    sensor_type_obj = SensorType.objects.filter(name=sensor_type).first()
    sensor_options = SensorConstantOption.objects.filter(sensor_type=sensor_type_obj)
    sensor_to_register.sensor_name = sensor_name
    sensor_to_register.sensor_type = sensor_type_obj
    sensor_to_register.sensor_id = sensor_id
    sensor_to_register.save()
    for option in sensor_options:
        sensor_to_register_option = SensorOption()
        sensor_to_register_option.is_info = option.is_info
        sensor_to_register_option.is_warning = option.is_warning
        sensor_to_register_option.is_integer = option.is_integer
        sensor_to_register_option.sensor = sensor_to_register
        sensor_to_register_option.option = option.option_name
        sensor_to_register_option.save()


def scenario_triggered(scenario):
    scenario_elements = ScenarioElement.objects.filter(scenario=scenario)
    for element in scenario_elements:
        sensor_option = SensorOption.objects.filter(id= element.option.id).first()
        if sensor_option.is_integer:
            if element.integer_below and element.integer_above:
                if sensor_option.integer_value <= element.integer_below and sensor_option.integer_value >= element.integer_above:
                    pass
                else:
                    return False
            elif element.integer_above:
                if sensor_option.integer_value >= element.integer_above:
                    pass
                else:
                    return False
            elif element.integer_below:
                if sensor_option.integer_value <= element.integer_below:
                    pass
                else:
                    return False
        else:
            if sensor_option.triggered == element.trigger_when:
                pass
            else:
                return False
    if scenario_elements:
        return True
    else:
        return False