from django.db import models


class SensorType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Sensor(models.Model):
    sensor_id = models.IntegerField()
    sensor_name = models.CharField(max_length=255)
    sensor_type = models.ForeignKey(SensorType)

    def __unicode__(self):
        return self.sensor_name


class SensorConstantOption(models.Model):
    sensor_type = models.ForeignKey(SensorType)
    option_name = models.CharField(max_length=255)
    is_warning = models.BooleanField(default=False)
    is_info = models.BooleanField(default=False)
    is_integer = models.BooleanField(default=False)

    def __unicode__(self):
        return self.option_name


class SensorOption(models.Model):
    sensor = models.ForeignKey(Sensor)
    option = models.CharField(max_length=255)
    is_warning = models.BooleanField(default=False)
    is_info = models.BooleanField(default=False)
    is_integer = models.BooleanField(default=False)
    triggered = models.BooleanField(default=False)
    integer_value = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.option)+"/"+unicode(self.sensor)


class SensorHistory(models.Model):
    date = models.DateTimeField()
    sensor_option = models.ForeignKey(SensorOption)
    integer_value = models.IntegerField(null=True, blank=True)
    triggered = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.sensor_option)


class SensorRegistration(models.Model):
    date = models.DateTimeField()
    sensor_id = models.IntegerField()
    sensor_type = models.ForeignKey(SensorType)
    registered = models.BooleanField(default=False)

