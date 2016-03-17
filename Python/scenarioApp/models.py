from django.db import models
from sensorApp.models import SensorOption


class Scenario(models.Model):
    date_created = models.DateTimeField()
    message = models.CharField(max_length=1000)
    scenario_name = models.CharField(max_length=255)
    is_warning = models.BooleanField(default=False)

    def __unicode__(self):
        return self.scenario_name


class ScenarioElement(models.Model):
    scenario = models.ForeignKey(Scenario)
    option = models.ForeignKey(SensorOption)
    integer_below = models.IntegerField(null=True, blank=True)
    integer_above = models.IntegerField(null=True, blank=True)
    trigger_when = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.scenario)