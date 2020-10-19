import operator
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from fantasy_pl.forms import SearchForm, AdvSearchForm
from fantasy_pl.models import Team, Player, Position, PlayerHistory, \
    Fixture


class TeamView(View):

    def get(self, request, id, sort):
        team = Team.objects.get(id=id)
        if sort in ['points_per_game', 'influence', 'now_cost', 'creativity',
                    'threat']:
            sort = '-' + sort
        players = Player.objects.filter(team=team.id).order_by(sort, 'id')
        fixtures_a = Fixture.objects.filter(team_a=team).filter(is_home=False)
        fixtures_h = Fixture.objects.filter(team_h=team).filter(is_home=True)
        fixtures = fixtures_a | fixtures_h
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        cnt = len(players)
        ctx = {'team': team, 'players': players, 'cnt': cnt, 'photo': photo,
               'title': team.name, 'fixtures': fixtures}
        return render(request, 'components/team.html', ctx)


class PlayerView(View):

    def get(self, request, id):
        player = Player.objects.get(id=id)
        games = PlayerHistory.objects.filter(player=player).order_by('-kickoff_time')
        chart = PlayerHistory.objects.filter(player=player).order_by('kickoff_time')
        team = Team.objects.get(name=player.team)
        fixtures_a = Fixture.objects.filter(team_a=team).filter(is_home=False)
        fixtures_h = Fixture.objects.filter(team_h=team).filter(is_home=True)
        fixtures = fixtures_a | fixtures_h
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        ctx = {'team': team, 'player': player, 'photo': photo, 'title': player,
               'games': games, 'fixtures': fixtures, 'chart': chart}
        return render(request, 'components/player.html', ctx)


class StandingsView(View):

    def get(self, request):
        table = Team.objects.all().order_by('position')
        ctx = {'table': table, 'title': 'Table'}
        return render(request, 'components/standings.html', ctx)


class PositionsView(View):

    def get(self, request, pos, sort):
        pos = Position.objects.get(name_short=pos)
        if pos.name_short == 'ALL':
            players = Player.objects.filter().order_by('-' + sort)
        else:
            players = Player.objects.filter(position=pos).order_by('-' + sort)

        paginator = Paginator(players, 25)
        page = request.GET.get('page')
        players = paginator.get_page(page)
        ctx = {'pos': pos, 'players': players, 'title': pos.name_short}
        return render(request, 'components/positions.html', ctx)


class StatsView(View):

    def get(self, request):
        ctx = {'title': 'Stats'}
        ctx['goals'] = Player.objects.all().order_by('-goals_scored')[:10:1]
        ctx['minutes'] = Player.objects.all().order_by('-minutes')[:10:1]
        ctx['assists'] = Player.objects.all().order_by('-assists')[:10:1]
        ctx['own_goals'] = Player.objects.all().order_by('-own_goals')[:10:1]
        ctx['penalties_saved'] = Player.objects.all().order_by('-penalties_saved')[:10:1]
        ctx['yellow_cards'] = Player.objects.all().order_by('-yellow_cards')[:10:1]
        ctx['red_cards'] = Player.objects.all().order_by('-red_cards')[:10:1]
        ctx['total_points'] = Player.objects.all().order_by('-total_points')[:10:1]
        ctx['points_per_game'] = Player.objects.all().order_by('-points_per_game')[:10:1]
        return render(request, 'components/stats.html', ctx)


class SearchView(View):

    def get(self, request):
        form = SearchForm(request.GET)
        adv_form = AdvSearchForm()
        if form.is_valid():
            query_search = form.cleaned_data['search']
            q_players = Player.objects.filter(
                Q(first_name__icontains=query_search) | Q(second_name__icontains=query_search)).order_by(
                '-selected_by_percent')
            paginator = Paginator(q_players, 25)
            page = request.GET.get('page')
            q_players = paginator.get_page(page)
            ctx = {'players': q_players, 'title': 'Search', 'adv_form': adv_form}
        else:
            ctx = {'title': 'Search', 'adv_form': adv_form}
        return render(request, 'components/search.html', ctx)

    def post(self, request):
        adv_form = AdvSearchForm(request.POST)
        if adv_form.is_valid():
            q_list = []
            pos = adv_form.cleaned_data['position']
            if pos is not None:
                q_list.append((Q(position=pos)))

            min = adv_form.cleaned_data['min']
            if min is None:
                min = 0

            max = adv_form.cleaned_data['max']
            if max is None:
                max = 2000

            stat = adv_form.cleaned_data['stats']
            if stat:
                if stat == 'points_per_game':
                    q_list.append((Q(points_per_game__gte=min)))
                    q_list.append((Q(points_per_game__lte=max)))
                elif stat == 'now_cost':
                    q_list.append((Q(now_cost__gte=min)))
                    q_list.append((Q(now_cost__lte=max)))
                elif stat == 'form':
                    q_list.append((Q(form__gte=min)))
                    q_list.append((Q(form__lte=max)))
                elif stat == 'total_points':
                    q_list.append((Q(total_points__gte=min)))
                    q_list.append((Q(total_points__lte=max)))

            if len(q_list) == 0:
                q_players = None
            else:
                q_players = Player.objects.filter(reduce(operator.and_, q_list)).order_by('-' + stat)
                paginator = Paginator(q_players, 25)
                page = request.GET.get('page')
                q_players = paginator.get_page(page)
            ctx = {'players': q_players, 'title': 'Search',
                   'adv_form': adv_form, 'stat': stat, 'pos': pos}
            return render(request, 'components/search.html', ctx)
        else:
            ctx = {'adv_form': AdvSearchForm(request.POST), 'title': 'Search',
                   'failure': True}
            return render(request, 'components/search.html', ctx)