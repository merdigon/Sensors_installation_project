from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from dashboard.views import home_view, registration_view, sensor_control_view, sensor_change_signal, \
    sensor_change_value_signal, sensor_history_view, sensor_remove_view, sensor_remove_id_view

from sensorApp.api_views import api_sensor_status_change, api_sensor_value_change, api_sensor_registration

from scenarioApp.views import scenario_list_view, scenario_add_view

urlpatterns = patterns('',
    url(r'^$', home_view, name='home_view'),
    url(r'^sensor_registration/$', registration_view, name='registration_view'),
    url(r'^sensor_control/$', sensor_control_view, name='sensor_control_view'),
    url(r'^sensor_history/$', sensor_history_view, name='sensor_history_view'),
    url(r'^sensor_remove/$', sensor_remove_view, name='sensor_remove_view'),
    url(r'^sensor_remove/(?P<sensor_id>.*)/$', sensor_remove_id_view, name='sensor_remove_id_view'),
    url(r'^sensor_control/send_signal/(?P<sensor_id>.*)/(?P<option>.*)/$', sensor_change_signal, name='sensor_change_signal'),
    url(r'^sensor_control/send_value/(?P<sensor_id>.*)/(?P<option>.*)/(?P<value>.*)/$', sensor_change_value_signal, name='sensor_change_value_signal'),

    url(r'^api/status_change/(?P<sensor_id>.*)/(?P<option>.*)/(?P<value>.*)/$', api_sensor_status_change, name='api_sensor_status_change'),
    url(r'^api/value_change/(?P<sensor_id>.*)/(?P<option>.*)/(?P<value>.*)/$', api_sensor_value_change, name='api_sensor_value_change'),
    url(r'^api/sensor_register/(?P<sensor_id>.*)/(?P<sensor_type>.*)/$', api_sensor_registration, name='api_sensor_registration'),

    url(r'^scenarios/$', scenario_list_view, name='scenario_list_view'),
    url(r'^scenarios/scenario_add/$', scenario_add_view, name='scenario_add_view'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^fonts/glyphicons-halflings-regular.ttf$', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.ttf')),
    url(r'^fonts/glyphicons-halflings-regular.woff$', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.woff')),
    url(r'^fonts/glyphicons-halflings-regular.woff2$', RedirectView.as_view(url='/static/fonts/glyphicons-halflings-regular.woff2')),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)