# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
import views


urlpatterns = patterns(
    views,
    url(r"^tasks_running/$", views.running_tasks_api, name="notification:tasks_running"),
    url(r"^tasks_waiting/$", views.waiting_tasks_api, name="notification:tasks_waiting"),
    url(r"^database_tasks/(?P<database_id>\d+)/?$", views.database_tasks, name="notification:database_tasks"),

)
