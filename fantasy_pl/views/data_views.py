from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.views import View

from fantasy_pl.forms import GetDataForm
from fantasy_pl.views.getters import read_json, get_individual_player_data, \
    populate_teams, populate_players, update_players, populate_positions, \
    update_teams, get_player_data, get_player_fixture, download_json
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


class PopulateTeamsView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        teams = data['teams']
        try:
            populate_teams(teams)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Teams database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdateTeamsView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API

        teams = data['teams']
        try:
            update_teams(teams)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Teams database has been updated.'}
        return render(request, "components/event.html", ctx)


class PopulatePositionsView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_position'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        positions = data['element_types']
        try:
            populate_positions(positions)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Position database has been populated.'}
        return render(request, "components/event.html", ctx)


class PopulatePlayersView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        players = data['elements']
        try:
            populate_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Players database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdatePlayersView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from Fantasy Premier League API
        players = data['elements']
        try:
            update_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!',
               'info': 'Players database has been updated.'}
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
            if id:
                try:
                    data = get_individual_player_data(id)
                    history = data['history']
                    get_player_data(history)
                    fixture = data['fixtures']
                    get_player_fixture(fixture)
                    ctx = {'successful': True,
                           'info': f'Data for player {id} has been updated',
                           'title': "Get data",
                           'form': GetDataForm()}
                    return render(request, "components/get_data.html", ctx)
                except Exception as e:
                    ctx = {'unsuccessful': True, 'info': 'Error occured',
                           'error': format(e), 'title': "Get data",
                           'form': GetDataForm()}
                    return render(request, "components/event.html", ctx)
            elif team:
                players = Player.objects.filter(team=team)
                for p in players:
                    try:
                        data = get_individual_player_data(p.id)
                        history = data['history']
                        get_player_data(history)
                        fixture = data['fixtures']
                        get_player_fixture(fixture)
                    except Exception as e:
                        ctx = {'unsuccessful': True,
                               'info': 'Error occured',
                               'error': format(e),
                               'title': "Get data",
                               'form': GetDataForm()}
                        return render(request, "components/event.html", ctx)

                ctx = {'successful': True,
                       'info': f'Data for players in {team} has been updated',
                       'title': "Get data",
                       'form': GetDataForm()}
                return render(request, "components/get_data.html", ctx)
            else:
                ctx = {'title': "Get data", 'form': GetDataForm()}
                return render(request, 'components/get_data.html', ctx)
