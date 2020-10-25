import operator
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from fantasy_pl.forms import SearchForm, PlayerSearchForm
from fantasy_pl.models import Team, Player, PlayerHistory, Fixtures


class TeamView(View):

    def get(self, request, id, sort):
        team = Team.objects.get(id=id)
        if sort in ['points_per_game', 'influence', 'now_cost', 'creativity',
                    'threat']:
            sort = '-' + sort
        players = Player.objects.filter(team=team.id).order_by(sort, 'id')
        fixtures_a = PlayerHistory.objects.filter(team_a=team)\
            .filter(is_home=False).filter(finished=False)\
            .order_by('kickoff_time').distinct('kickoff_time')
        fixtures_h = PlayerHistory.objects.filter(team_h=team) \
            .filter(is_home=True).filter(finished=False) \
            .order_by('kickoff_time').distinct('kickoff_time')
        fixtures = fixtures_a | fixtures_h
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        cnt = len(players)
        ctx = {'team': team, 'players': players, 'cnt': cnt, 'photo': photo,
               'title': team.name, 'fixtures': fixtures}
        return render(request, 'components/team/team.html', ctx)


class PlayerView(View):

    def get(self, request, id):
        player = Player.objects.get(id=id)
        hist = PlayerHistory.objects.filter(player=player)\
                                    .filter(finished=True)\
                                    .order_by('kickoff_time')
        games = PlayerHistory.objects.filter(player=player) \
            .filter(finished=False) \
            .order_by('kickoff_time')
        chart = hist
        team = Team.objects.get(name=player.team)

        photo = "/static/logos/" + team.short_name.lower() + ".png "
        ctx = {'team': team, 'player': player, 'photo': photo, 'title': player,
               'games': games, 'hist': hist, 'chart': chart}
        return render(request, 'components/player/player.html', ctx)


class StandingsView(View):

    def get(self, request):
        table = Team.objects.all().order_by('position')
        ctx = {'table': table, 'title': 'Table'}
        return render(request, 'components/standings.html', ctx)


class FixtureView(View):

    def get(self, request):
        fixture = Fixtures.objects.all().order_by('event', 'kickoff_time')
        curr_event = Fixtures.objects.filter(finished=True).last().event
        paginator = Paginator(fixture, 10)
        page = request.GET.get('page', curr_event)
        fixture = paginator.get_page(page)
        ctx = {'fixture': fixture, 'title': 'Fixtures'}
        return render(request, 'components/fixture.html', ctx)


class StatsView(View):

    def get(self, request):
        ctx = {'title': 'Stats'}
        ctx['stats'] = Player.objects.filter(minutes__gt=0)
        return render(request, 'components/stats.html', ctx)


class PlayersSearchView(View):

    def get(self, request):
        form = SearchForm(request.GET)
        adv_form = PlayerSearchForm()
        if form.is_valid():
            query_search = form.cleaned_data['search']
            q_players = Player.objects.filter(
                Q(first_name__icontains=query_search) |
                Q(second_name__icontains=query_search)).order_by(
                    '-selected_by_percent')
            ctx = {'players': q_players, 'title': 'Search',
                   'adv_form': adv_form}
        else:
            ctx = {'title': 'Search', 'adv_form': adv_form}
        return render(request, 'components/player_search.html', ctx)

    def post(self, request):
        adv_form = PlayerSearchForm(request.POST)
        if adv_form.is_valid():
            pos = adv_form.cleaned_data['position']
            max = adv_form.cleaned_data['max']
            q_players = Player.objects.order_by('-now_cost')

            if pos is not None:
                q_players = q_players.filter(position=pos)
            if max is not None:
                q_players = q_players.filter(now_cost__lte=max)

            ctx = {'players': q_players, 'title': 'Search',
                   'adv_form': adv_form, 'pos': pos}
            return render(request, 'components/player_search.html', ctx)
        else:
            ctx = {'adv_form': PlayerSearchForm(request.POST),
                   'title': 'Search', 'failure': True}
            return render(request, 'components/player_search.html', ctx)