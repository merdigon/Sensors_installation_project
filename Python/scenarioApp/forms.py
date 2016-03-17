# -*- coding: utf-8 -*-

from django import forms
from .models import ScenarioElement, Scenario


class ScenarioAddForm(forms.ModelForm):
    class Meta:
        model = Scenario
        fields = ['scenario_name', 'message', 'is_warning']


class SensorAddForm(forms.ModelForm):
    class Meta:
        model = ScenarioElement
        fields = ['option', 'integer_below', 'integer_above', 'trigger_when']
        help_texts = {
            'integer_below': 'trigger when value <= value in scenario (leave blank to ignore this option)',
            'integer_above': 'trigger when value >= value in scenario (leave blank to ignore this option)',
            'trigger_when': 'ticked - inform me when sensor is triggered (does not work for integer sensors, like thermometer)'
        }


SensorAddFormSet = forms.formset_factory(SensorAddForm)
