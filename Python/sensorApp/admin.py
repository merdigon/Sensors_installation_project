from django.contrib import admin
from .models import SensorType, SensorOption, Sensor, SensorConstantOption, SensorHistory

@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

# @admin.register(SensorOption)
# class SensorOptionAdmin(admin.ModelAdmin):
#     list_display = ('sensor', 'get_sensor_type', 'option', 'triggered', 'is_integer', 'is_info', 'integer_value')
#     list_filter = ('sensor', 'option', 'triggered', 'is_integer')
#     search_fields = ('name', )
#     ordering = ('sensor', )
#
#     def get_sensor_type(self, obj):
#         return obj.sensor.sensor_type
#
#     get_sensor_type.short_description = 'Sensor type'
#     get_sensor_type.admin_order_field = 'sensor__sensor_type'


class SensorOptionInLine(admin.TabularInline):
    model = SensorOption

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('sensor_id', 'sensor_name', 'sensor_type')
    list_filter = ('sensor_type', )
    search_fields = ('sensor_id', 'sensor_name')
    ordering = ('sensor_id', )
    inlines = (SensorOptionInLine, )

@admin.register(SensorConstantOption)
class SensorConstantOptionAdmin(admin.ModelAdmin):
    list_display = ('sensor_type', 'option_name', 'is_warning', 'is_integer', 'is_info')
    list_filter = ('sensor_type', 'option_name', 'is_warning', 'is_integer', 'is_info')
    search_fields = ('sensor_type', )
    ordering = ('sensor_type', )


@admin.register(SensorHistory)
class SensorHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'sensor_option', 'integer_value', 'triggered')
    search_fields = ('sensor_option', 'integer_value')
    list_filter = ('date', 'triggered')
    ordering = ('date', )

