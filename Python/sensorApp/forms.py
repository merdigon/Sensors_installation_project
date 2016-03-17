# -*- coding: utf-8 -*-

from django import forms
from .models import Sensor


class SensorAddForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['sensor_type']


class SensorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ['sensor_name']
