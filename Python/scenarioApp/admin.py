from django.contrib import admin

from .models import Scenario, ScenarioElement


class ScenarioElementInLine(admin.TabularInline):
    model = ScenarioElement


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'scenario_name')
    list_filter = ('date_created', )
    search_fields = ('scenario_name', )
    ordering = ('scenario_name', )
    inlines = (ScenarioElementInLine, )


