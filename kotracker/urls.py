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
    path('rockyirs/', admin.site.urls),
    path('overview/<tournament>', overview_tournament, name='overview'),
    path('view_round/<tournament>/<number>/', view_round, name='view_round'),
    path('edit_round/<tournament>/<number>/', edit_round, name='edit_round'),
    path('create_next_round/<tournament>/', create_next_round, name='create_next_round'),
]
