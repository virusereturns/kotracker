from django.db import models
from django.db.models import Avg
from datetime import timedelta


MODE_CHOICES = (
    (1, 'Normal'),
    (2, 'PB'),
)

FONT_CHOICES = (
    ('Mandela', 'Mandela'),
    ('Bradley_Gratis', 'Bradley_Gratis'),
    ('Tecmo_1', 'Tecmo_1'),
    ('Tecmo_2', 'Tecmo_2'),
)


def ordinal(n):
    return "{}{}".format(n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def duration(td):
    # Converts a timedelta to MM:SS
    seconds = td.seconds
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if seconds < 10:
        seconds = "0" + str(seconds)
    return "{}:{}".format(minutes, seconds)


class Tournament(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=150)
    date = models.DateField(null=True, blank=True)
    game = models.CharField(max_length=150)
    mode = models.PositiveSmallIntegerField(default=1, choices=MODE_CHOICES)
    font = models.CharField(max_length=100, default='Mandela', choices=FONT_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date']

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

    def get_average_time(self):
        return RacerRound.objects.filter(racer=self, time__isnull=False).aggregate(Avg('time'))['time__avg']

    def knockout_finish(self):
        count = self.tournament.racer_set.count()
        if self.elimination_round:
            n = count - self.elimination_round + 1
            return ordinal(n)
        else:
            return None

    def get_pb(self):
        if self.pb:
            return duration(self.pb)
        else:
            return '???'

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
    position_in_round = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return "{}'s round {} on {} {}".format(
            self.racer.name, self.round_number.number, self.round_number.tournament, self.time or '')

    class Meta:
        pass

    def get_last_round_time(self):
        return RacerRound.objects.get(racer=self.racer, round_number__number=self.round_number.number - 1).time or '-'

    def get_difference_with_last_round(self):
        if self.round_number.number == 1:
            return ''
        elif self.position_in_round is None:
            return ''
        else:
            try:
                previous_round = RacerRound.objects.get(
                    racer=self.racer, round_number__number=self.round_number.number - 1)
            except RacerRound.DoesNotExist:
                return ''
            previous_round_position = previous_round.position_in_round
            if previous_round_position is None:
                return ''
            this_round_position = self.position_in_round
            difference = previous_round_position - this_round_position
            if difference == 0:
                return '<span style="color:orange">-</span>'
            elif difference < 0:
                return '<span style="color:red">▼{}</span>'.format(abs(difference))
            elif difference > 0:
                return '<span style="color:green">▲{}</span>'.format(abs(difference))
