from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


from fantasy_pl.forms import GetDataForm, GetFixtureForm, GetUserteamForm
from fantasy_pl.models import Player, Fixtures
from fantasy_pl.views.getters import read_json, get_individual_player_data, \
    populate_teams, populate_players, update_players, populate_positions, \
    update_teams, get_player_data, get_player_fixture, download_json, \
    get_fixtures_for_season, populate_fixture, update_fixture, \
    get_fpl_userteam, update_userteam, get_data


class DownloadDataView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        try:
            download_json()
            ctx = {'event': 'success', 'info': 'Data has been downloaded'}
            return render(request, "page-event.html", ctx)
        except Exception as e:
            ctx = {'event': 'error', 'error': format(e)}
            return render(request, "page-event.html", ctx)


def DownloadUserteamView(request):
    form = GetUserteamForm(request.POST)
    if form.is_valid():
        player_id = form.cleaned_data['fpl_id']
        try:
            last_game = Fixtures.objects.filter(finished=True).last()
            gw = last_game.event
            team = get_fpl_userteam(player_id, gw)
            player = team['picks']
            player_list = [p['element'] for p in player]
        except Exception as e:
            messages.error(request, f"Failure downloading your team: "
                                    f"{format(e)}")
            return redirect('/user-team/')
        user = request.user
        update_userteam(user, player_list)
        messages.success(request, "Your team was succesfully downloaded.")
        return redirect('/user-team/')


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
            ctx = {'event': 'error', 'error': format(e)}
            return render(request, "page-event.html", ctx)

        ctx = {'event': 'success',
               'info': 'Tables Team, Position, Player has been populated.'}
        return render(request, "page-event.html", ctx)


class UpdateTablesView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        # data = read_json()  ## Read data from JSON file on disk
        data = get_data() ## Read data from Fantasy Premier League API
        teams = data['teams']
        players = data['elements']
        try:
            update_teams(teams)
            update_players(players)
        except Exception as e:
            ctx = {'event': 'error', 'error': format(e)}
            return render(request, "page-event.html", ctx)

        ctx = {'event': 'success',
               'info': 'Tables database has been updated.'}
        return render(request, "page-event.html", ctx)


class GetPlayersHistoryView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_player'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        ctx = {'form': GetDataForm()}
        return render(request, 'get_player_data.html', ctx)

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
                    ctx = {'event': 'success',
                           'info': f'Data for player {id} has been updated',
                           'form': GetDataForm()}
                    return render(request, "get_player_data.html", ctx)
                except Exception as e:
                    ctx = {'event': 'error', 'error': format(e),
                           'form': GetDataForm()}
                    return render(request, "get_player_data.html", ctx)
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
                        ctx = {'event': 'error', 'error': format(e),
                               'form': GetDataForm()}
                        return render(request, "get_player_data.html", ctx)

                ctx = {'event': 'success',
                       'info': f'Data for players in {team} has been updated',
                       'form': GetDataForm()}
                return render(request, "get_player_data.html", ctx)
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
                        ctx = {'event': 'error',
                               'error': format(e),
                               'form': GetDataForm()}
                        return render(request, "get_player_data.html", ctx)

                ctx = {'event': 'success',
                       'info': f'Data for players has been updated',
                       'form': GetDataForm()}
                return render(request, "get_player_data.html", ctx)
            else:
                ctx = {'form': GetDataForm()}
                return render(request, 'get_player_data.html', ctx)


class GetFixtureView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_fixture'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        ctx = {'form': GetFixtureForm()}
        return render(request, 'get_fixture.html', ctx)

    def post(self, request):
        form = GetFixtureForm(request.POST)
        if form.is_valid():
            choice = int(form.cleaned_data['choice'])
            if choice == 0:
                try:
                    fixture = get_fixtures_for_season()
                    populate_fixture(fixture)
                    ctx = {'event': 'success', 'info': 'Fixture downloaded',
                           'form': GetFixtureForm()}
                    return render(request, 'get_fixture.html', ctx)
                except Exception as e:
                    ctx = {'event': 'error', 'error': format(e),
                           'form': GetFixtureForm()}
                    return render(request, "page-event.html", ctx)
            else:
                try:
                    fixture = get_fixtures_for_season()
                    update_fixture(fixture)
                    ctx = {'event': 'success', 'info': 'Fixture updated',
                           'form': GetFixtureForm()}
                    return render(request, 'get_fixture.html', ctx)
                except Exception as e:
                    ctx = {'event': 'error', 'error': format(e),
                           'form': GetFixtureForm()}
                    return render(request, "page-event.html", ctx)