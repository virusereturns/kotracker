"""kotracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tracker.views import *

urlpatterns = [
    path('', tournament_menu, name='main_menu'),
    path('rockyirs/', admin.site.urls),
    path('overview/<tournament>/', overview_tournament, name='overview'),
    path('overview_with_details/<tournament>/', overview_with_details, name='overview_with_details'),
    path('overview_pb_mode/<tournament>/', overview_pb_mode, name='overview_pb_mode'),
    path('tournament_details/<tournament>/', tournament_details, name='tournament_details'),
    path('view_round/<tournament>/<number>/', view_round, name='view_round'),
    path('view_last_round/<tournament>/', view_last_round, name='view_last_round'),
    path('edit_round/<tournament>/<number>/', edit_round, name='edit_round'),
    path('create_next_round/<tournament>/', create_next_round, name='create_next_round'),
    path('revive_racer/<racer_id>/', revive_racer, name='revive_racer')
]
