from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from fantasy_pl.forms import GetDataForm, GetFixtureForm
from fantasy_pl.views.getters import read_json, get_individual_player_data, \
    populate_teams, populate_players, update_players, populate_positions, \
    update_teams, get_player_data, get_player_fixture, download_json, \
    get_fixtures_for_season, populate_fixture, update_fixture
from fantasy_pl.models import Player


class DownloadDataView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        try:
            download_json()
            ctx = {'event': 'Success!', 'info': 'Data has been downloaded'}
            return render(request, "components/event.html", ctx)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)


class PopulateTablesView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        teams = data['teams']
        positions = data['element_types']
        players = data['elements']
        try:
            populate_teams(teams)
            populate_positions(positions)
            populate_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Tables Team, Position, Player has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdateTablesView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        teams = data['teams']
        players = data['elements']
        try:
            update_teams(teams)
            update_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Tables database has been updated.'}
        return render(request, "components/event.html", ctx)


class GetPlayersHistoryView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_player'

    def get(self, request):
        ctx = {'title': "Get data", 'form': GetDataForm()}
        return render(request, 'components/get_data.html', ctx)

    def post(self, request):
        form = GetDataForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            team = form.cleaned_data['team']
            all = form.cleaned_data['all']
            if id:
                try:
                    data = get_individual_player_data(id)
                    history = data['history']
                    get_player_data(history)
                    game = data['fixtures']
                    get_player_fixture(game, id)
                    ctx = {'successful': True,
                           'info': f'Data for player {id} has been updated',
                           'title': "Get data",
                           'form': GetDataForm()}
                    return render(request, "components/get_data.html", ctx)
                except Exception as e:
                    ctx = {'unsuccessful': True,
                           'error': format(e),
                           'title': "Get data",
                           'form': GetDataForm()}
                    return render(request, "components/event.html", ctx)
            elif team:
                players = Player.objects.filter(team=team)
                for p in players:
                    try:
                        data = get_individual_player_data(p.id)
                        history = data['history']
                        get_player_data(history)
                        game = data['fixtures']
                        get_player_fixture(game, p.id)
                    except Exception as e:
                        ctx = {'unsuccessful': True,
                               'error': format(e),
                               'title': "Get data",
                               'form': GetDataForm()}
                        return render(request, "components/event.html", ctx)

                ctx = {'successful': True,
                       'info': f'Data for players in {team} has been updated',
                       'title': "Get data",
                       'form': GetDataForm()}
                return render(request, "components/get_data.html", ctx)
            elif all:
                players = Player.objects.all()
                for p in players:
                    try:
                        data = get_individual_player_data(p.id)
                        history = data['history']
                        get_player_data(history)
                        game = data['fixtures']
                        get_player_fixture(game, p.id)
                    except Exception as e:
                        ctx = {'unsuccessful': True,
                               'error': format(e),
                               'title': "Get data",
                               'form': GetDataForm()}
                        return render(request, "components/event.html", ctx)

                ctx = {'successful': True,
                       'info': f'Data for players has been updated',
                       'title': "Get data",
                       'form': GetDataForm()}
                return render(request, "components/get_data.html", ctx)
            else:
                ctx = {'title': "Get data", 'form': GetDataForm()}
                return render(request, 'components/get_data.html', ctx)


class GetFixtureView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_fixture'

    def get(self, request):
        ctx = {'title': 'Get fixtures', 'form': GetFixtureForm()}
        return render(request, 'components/get_fixture.html', ctx)

    def post(self, request):
        form = GetFixtureForm(request.POST)
        if form.is_valid():
            choice = int(form.cleaned_data['choice'])
            if choice == 0:
                try:
                    fixture = get_fixtures_for_season()
                    populate_fixture(fixture)
                    ctx = {'successful': True,
                           'info': 'Fixture downloaded',
                           'title': 'Get Fixture',
                           'form': GetFixtureForm()}
                    return render(request, 'components/get_fixture.html',ctx)
                except Exception as e:
                    ctx = {'unsuccessful': True,
                           'error': format(e),
                           'title': "Get Fixture",
                           'form': GetFixtureForm()}
                    return render(request, "components/event.html", ctx)
            elif choice == 1:
                try:
                    fixture = get_fixtures_for_season()
                    update_fixture(fixture)
                    ctx = {'successful': True,
                           'info': 'Fixture updated',
                           'title': 'Get Fixture',
                           'form': GetFixtureForm()}
                    return render(request, 'components/get_fixture.html', ctx)
                except Exception as e:
                    ctx = {'unsuccessful': True,
                           'error': format(e),
                           'title': "Get Fixture",
                           'form': GetFixtureForm()}
                    return render(request, "components/event.html", ctx)
            else:
                ctx = {'title': "Get fixture", 'form': GetFixtureForm()}
                return render(request, 'components/get_fixture.html', ctx)