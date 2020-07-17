from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.db.models import Max
from django.http import HttpResponseRedirect
from .models import *


def view_round(request, tournament, number):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    round_object = get_object_or_404(Round, tournament=tournament, number=number)
    racer_rounds = RacerRound.objects.filter(
        racer__tournament=tournament_object, round_number=round_object).order_by('-racer__elimination_round', 'time')
    return render(request, 'view_round.html', {
        'racer_rounds': racer_rounds, 'round': round_object, 'tournament': tournament_object})


@login_required
def edit_round(request, tournament, number):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    round_object = get_object_or_404(Round, tournament=tournament, number=number)
    racer_rounds = RacerRound.objects.filter(
        racer__tournament=tournament_object, round_number=round_object,
        racer__eliminated=False, racer__dropped=False).order_by('time')
    eliminated_racers = Racer.objects.filter(
        Q(eliminated=True) | Q(dropped=True), tournament=tournament_object).order_by('-elimination_round')
    if int(number) > 1:
        sort = True
        for racer_round in racer_rounds:
            if racer_round.time:
                sort = False
                break
        racer_rounds = sorted(racer_rounds, key=lambda a: a.get_last_round_time()) if sort else racer_rounds
    if request.POST:
        # Process eliminates
        for name, value in request.POST.items():
            if name.startswith('e'):
                bits = name.split('-')
                racer = bits[1]
                round = bits[2]
                # tournament = bits[3]
                racer = Racer.objects.get(pk=racer)
                racer.eliminated = True
                racer.elimination_round = round
                racer.save()
            elif name.startswith('d'):
                bits = name.split('-')
                racer = bits[1]
                round = bits[2]
                # tournament = bits[3]
                racer = Racer.objects.get(pk=racer)
                racer.dropped = True
                racer.elimination_round = round
                racer.save()
            elif name.startswith('time') and value:
                bits = name.split('-')
                racer_round_id = bits[1]
                racer_round = RacerRound.objects.get(pk=racer_round_id)
                racer_round.time = "00:" + value
                racer_round.save()
                # Next we'll see if this was the fastest run for this racer, get it again so the time is converted
                racer_round = RacerRound.objects.get(pk=racer_round_id)
                racer = racer_round.racer
                if racer.best_time_in_race is None or racer.best_time_in_race and \
                        racer.best_time_in_race > racer_round.time:
                    racer.best_time_in_race = racer_round.time
                    racer.save()
        return HttpResponseRedirect(reverse('edit_round', kwargs={
            'tournament': tournament, 'number': number}))

    rounds = tournament_object.round_set.all()

    return render(request, 'edit_round.html', {
        'racer_rounds': racer_rounds, 'round': round_object, 'tournament': tournament_object,
        'eliminated_racers': eliminated_racers, 'round_list': rounds})


def overview_tournament(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    racers = Racer.objects.filter(tournament=tournament_object).order_by('pb')
    return render(request, 'overview_tournament.html', {
        'racers': racers, 'tournament': tournament_object})


def overview_with_details(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    racers = Racer.objects.filter(tournament=tournament_object).order_by('-elimination_round', 'best_time_in_race')
    return render(request, 'overview_with_details.html', {
        'racers': racers, 'tournament': tournament_object})


@login_required
def create_next_round(request, tournament):
    tournament = get_object_or_404(Tournament, pk=tournament)
    try:
        last_round = Round.objects.filter(tournament=tournament).latest('id').number
    except Round.DoesNotExist:
        last_round = 0
    # First we create the next round
    round = Round.objects.create(tournament=tournament, number=last_round + 1)
    # Then we move on to add all the racers to the round
    for racer in Racer.objects.filter(tournament=tournament):
        RacerRound.objects.create(
            racer=racer,
            round_number=round)
    return HttpResponseRedirect(reverse(
        'edit_round', kwargs={'tournament': tournament.id, 'number': round.number}))


@login_required
def tournament_menu(request):
    tournaments = Tournament.objects.all()
    return render(request, 'tournament_menu.html', {'tournaments': tournaments})


@login_required
def tournament_details(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    rounds = tournament_object.round_set.all()
    return render(request, 'tournament_details.html', {
        'tournament': tournament_object, 'rounds': rounds})
