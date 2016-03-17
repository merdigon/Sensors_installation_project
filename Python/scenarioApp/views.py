from django.shortcuts import render
from .models import Scenario
from .forms import SensorAddFormSet, ScenarioAddForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required


@login_required
def scenario_list_view(request):
    scenarios = Scenario.objects.all()
    return render(request, "scenario_list.html", {'scenarios': scenarios})


@login_required
def scenario_add_view(request):
    if request.method == 'POST':
        scenarioform = ScenarioAddForm(request.POST)
        formset = SensorAddFormSet(request.POST, prefix='form')
        if formset.is_valid() and scenarioform.is_valid():
            scenario = scenarioform.save(commit=False)
            scenario.date_created = timezone.now()
            scenario.save()
            scenario_obj = Scenario.objects.filter(id=scenario.id).first()
            for form in formset:
                if form.is_valid():
                    ob = form.save(commit=False)
                    ob.scenario = scenario_obj
                    ob.save()
                else:
                    scenario_obj.delete()
                    break
            messages.success(request, 'Scenario added')
            return HttpResponseRedirect('/scenarios')
    else:
        scenarioform = ScenarioAddForm()
        formset = SensorAddFormSet()
    return render(request, "scenario_add.html", {"formset": formset, 'scenarioform': scenarioform})