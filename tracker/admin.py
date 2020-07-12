from django.contrib import admin
from .models import *


class RacerInline(admin.TabularInline):
    model = Racer
    pass


class TournamentAdmin(admin.ModelAdmin):
    model = Tournament
    inlines = [RacerInline]


# Register your models here.
admin.site.register(Racer)
admin.site.register(RacerRound)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Round)
