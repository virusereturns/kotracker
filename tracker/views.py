import pandas
from django.conf import settings
from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# from django.db.models import Max
from django.http import HttpResponseRedirect
from .models import *


def view_last_round(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    round_object = get_object_or_404(Round, tournament=tournament, number=tournament.current_round() - 1)
    racer_rounds = RacerRound.objects.filter(
        racer__eliminated=False, racer__dropped=False, racer__tournament=tournament,
        round_number=round_object).order_by('time')
    eliminated_racers = Racer.objects.filter(
        Q(eliminated=True) | Q(dropped=True), tournament=tournament).order_by('-elimination_round')
    eliminated_racers_list = []
    for index, racer in enumerate(eliminated_racers, start=1):
        racer.position_for_table = index + racer_rounds.count()
        eliminated_racers_list.append(racer)
    return render(request, 'view_round.html', {
        'racer_rounds': racer_rounds, 'round': round_object, 'tournament': tournament,
        'eliminated_racers_list': eliminated_racers_list, 'racer_rounds_count': racer_rounds.count()})


@login_required
def edit_round(request, tournament, number):
    """
    In the case you manually want to add the rounds.
    """
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    round_object = get_object_or_404(Round, tournament=tournament, number=number)
    racer_rounds = RacerRound.objects.filter(
        racer__tournament=tournament_object, round_number=round_object,
        racer__eliminated=False, racer__dropped=False)
    if tournament_object.mode == 2:
        racer_rounds = racer_rounds.order_by('racer__pb')
    else:
        # If this is not PB mode, we're gonna order them by time
        racer_rounds = racer_rounds.order_by('time')
    eliminated_racers = Racer.objects.filter(
        Q(eliminated=True) | Q(dropped=True), tournament=tournament_object).order_by('-elimination_round')
    if tournament_object.mode != 2:
        # We're not gonna do this if this is tourament mode
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
                racer = Racer.objects.get(pk=racer)
                racer.eliminated = True
                racer.elimination_round = round
                racer.save()
            elif name.startswith('d'):
                bits = name.split('-')
                racer = bits[1]
                round = bits[2]
                racer = Racer.objects.get(pk=racer)
                racer.dropped = True
                racer.elimination_round = round
                racer.save()
            elif name.startswith('time') and value and tournament_object.mode != 2:
                # We're not gonna do this if this is PB mode
                bits = name.split('-')
                racer_round_id = bits[1]
                racer_round = RacerRound.objects.get(pk=racer_round_id)
                racer_round.time = "00:" + value
                racer_round.save()
                # Next we'll see if this was the fastest run for this racer, get it again so the time is converted
                racer_round = RacerRound.objects.get(pk=racer_round_id)
                racer = racer_round.racer
        # After this has finished, we'll iterate through every finished runner so we can register their position
        position = 0
        for racer_round in RacerRound.objects.filter(
            racer__tournament=tournament_object, round_number=round_object, racer__eliminated=False,
                racer__dropped=False).order_by('time'):
            position = position + 1
            racer_round.position_in_round = position
            racer_round.save()

        return HttpResponseRedirect(reverse('edit_round', kwargs={
            'tournament': tournament, 'number': number}))

    rounds = tournament_object.round_set.all()

    return render(request, 'edit_round.html', {
        'racer_rounds': racer_rounds, 'round': round_object, 'tournament': tournament_object,
        'eliminated_racers': eliminated_racers, 'round_list': rounds})


@login_required
def process(request, tournament_id):
    """
    Process a csv into a Pandas DataFrame from an URL. Soon you'll be able to also post a file with that csv.
    """
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    current_round_number = tournament.current_round()

    try:
        previous_round = Round.objects.get(number=current_round_number - 1, tournament=tournament)
        racer_rounds = RacerRound.objects.filter(
            racer__tournament=tournament,
            round_number=previous_round,
            racer__eliminated=False,
            racer__dropped=False
        ).order_by('time')

        eliminated_racers = Racer.objects.filter(
            Q(eliminated=True) | Q(dropped=True),
            tournament=tournament
        ).order_by('-elimination_round')

        eliminated_racers_list = []
        for index, racer in enumerate(eliminated_racers, start=1):
            racer.position_for_table = index + racer_rounds.count()
            eliminated_racers_list.append(racer)
    except Round.DoesNotExist:
        # This means this is round 1
        racer_rounds, eliminated_racers_list = None, None
    except Exception:
        previous_round = Round.objects.get(number=current_round_number, tournament=tournament)

    if request.POST:
        new_round = create_next_round_lite(tournament)
        df = pandas.read_csv(settings.RACE_CSV_URL, header=None, names=['username', 'time'])
        eliminated_racers = int(request.POST.get('eliminated_racers'))
        unfinished_count = 0
        for row in df.itertuples(index=False, name='Rr'):
            # Get the data from the row
            username = getattr(row, 'username')
            time = getattr(row, 'time')

            try:
                racer_round = RacerRound.objects.get(
                    racer__tournament=tournament,
                    racer__discord_username=username,
                    round_number=new_round
                )
            except Exception:
                continue

            racer = racer_round.racer
            if time.lower() == 'dnf':
                racer_round.eliminated = True
                racer_round.dnf = True
                racer.eliminated = True
                racer.elimination_round = new_round.number
            else:
                racer_round.time = time

            if racer_round.time:
                racer_round.save()
                # Reload this object from BD. TODO: Explain why because I don't remember.
                racer_round = RacerRound.objects.get(pk=racer_round.id)

            racer.save()
            racer_round.save()

        # We will search for unfinished runners and eliminate them if necessary
        unfinished_runners = RacerRound.objects.filter(
            racer__tournament=tournament,
            round_number=new_round,
            time__isnull=True
        )

        for racer_round in unfinished_runners:
            unfinished_count += 1
            racer_round.eliminated = True
            racer_round.dnf = True
            racer_round.save()
            racer = racer_round.racer
            racer.eliminated = True
            racer.elimination_round = new_round.number
            racer.save()

        if unfinished_count < eliminated_racers:
            # If it's not enought with the unfinished runners, which is probably the most common case, we'll eliminate
            # runners based on their time
            have_to_eliminate = eliminated_racers - unfinished_count
            not_yet_eliminated_racers = list(RacerRound.objects.filter(
                racer__tournament=tournament,
                round_number=new_round,
                time__isnull=False,
                racer__eliminated=False
            ).order_by('-time'))[:have_to_eliminate]
            for racer_round in not_yet_eliminated_racers:
                racer_round.eliminated = True
                racer_round.save()
                racer = racer_round.racer
                racer.eliminated = True
                racer.elimination_round = new_round.number
                racer.save()

        # After this has finished, we'll iterate through every finished runner so we can register their position
        position = 0
        finished_runners = RacerRound.objects.filter(
            racer__tournament=tournament,
            round_number=new_round,
            racer__eliminated=False,
            racer__dropped=False
        ).order_by('time')

        for racer_round in finished_runners:
            position = position + 1
            racer_round.position_in_round = position
            racer_round.save()

        return HttpResponseRedirect(reverse('process', args=[tournament.id]))

    return render(request, 'edit3.html', {
        'racer_rounds': racer_rounds,
        'current_round': current_round_number,
        'previous_round': current_round_number - 1,
        'tournament': tournament,
        'eliminated_racers_list': eliminated_racers_list,
    })


def overview_tournament(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    racers = Racer.objects.filter(tournament=tournament_object).order_by('pb')
    return render(request, 'overview_tournament.html', {
        'racers': racers, 'tournament': tournament_object})


def overview_with_details(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    racers = Racer.objects.filter(tournament=tournament_object).order_by('-elimination_round')
    sorted_racers = sorted(racers, key=lambda r: r.get_best_time() or timedelta(999))
    return render(request, 'overview_with_details.html', {
        'racers': sorted_racers, 'tournament': tournament_object})


def overview_pb_mode(request, tournament):
    tournament_object = get_object_or_404(Tournament, pk=tournament)
    racers = Racer.objects.filter(tournament=tournament_object).order_by('pb')
    return render(request, 'overview_pb_mode.html', {
        'racers': racers, 'tournament': tournament_object})


def create_next_round_lite(tournament):
    try:
        last_round = Round.objects.filter(tournament=tournament).latest('id').number
        round = Round.objects.create(tournament=tournament, number=last_round + 1)
    except Round.DoesNotExist:
        # This means the first round does not exist, why not create it.
        round = Round.objects.create(tournament=tournament, number=1)
    # Then we move on to add all the racers to the round
    for racer in Racer.objects.filter(tournament=tournament, eliminated=False, dropped=False):
        RacerRound.objects.create(racer=racer, round_number=round)
    return round


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


@login_required
def revive_racer(request, racer_id):
    racer = get_object_or_404(Racer, pk=racer_id)
    racer.elimination_round = None
    racer.eliminated = False
    racer.dropped = False
    racer.save()
    return HttpResponseRedirect(reverse("main_menu"))
