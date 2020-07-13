from django.db import models
from datetime import timedelta


class Tournament(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=150)
    date = models.DateField(null=True, blank=True)
    game = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        pass

    def current_round(self):
        return self.round_set.count()


class Racer(models.Model):
    """
    Contains all the racers that are defined at the beginning of each race
    """
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    pb = models.DurationField(null=True, blank=True)
    eliminated = models.BooleanField(default=False)
    elimination_round = models.PositiveSmallIntegerField(null=True, blank=True)
    dropped = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(null=True, blank=True)
    best_time_in_race = models.DurationField(null=True, blank=True)
    average_time_in_race = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        pass


class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Round {} of {}".format(self.number, self.tournament)

    class Meta:
        pass


class RacerRound(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE)
    round_number = models.ForeignKey(Round, on_delete=models.CASCADE)
    time = models.DurationField(null=True, blank=True)
    dnf = models.BooleanField(default=False)
    eliminated = models.BooleanField(default=False)
    dropped = models.BooleanField(default=False)

    def __str__(self):
        return "{}'s round {} on {} {}".format(
            self.racer.name, self.round_number.number, self.round_number.tournament, self.time or '')

    class Meta:
        pass

    def get_last_round_time(self):
        return RacerRound.objects.get(racer=self.racer, round_number__number=self.round_number.number - 1).time or '-'
