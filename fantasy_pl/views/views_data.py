from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from fantasy_pl.forms import GetPlayerDataForm, GetFixtureForm, \
    GetUserteamForm, GetDataForm
from fantasy_pl.models import Player, Fixtures, Event
from fantasy_pl.views.getters import read_json, get_individual_player_data, \
    update_teams, update_players, populate_positions, get_player_data, \
    get_player_fixture, download_json, get_fixtures_for_season, \
    update_fixture, get_fpl_userteam, update_userteam, \
    get_data, get_fpl_user, update_user, update_events, \
    update_user_history, get_fpl_user_history_and_season, update_user_season


def DownloadUserteamView(request):
    form = GetUserteamForm(request.POST)
    if form.is_valid():
        player_id = form.cleaned_data['fpl_id']
        try:
            last_event = Event.objects.filter(finished=True).last()
            gw = last_event.id
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


def DownloadUserView(request):
    form = GetUserteamForm(request.POST)
    if form.is_valid():
        player_id = form.cleaned_data['fpl_id']
        try:
            user_fpl = get_fpl_user(player_id)
            user_fpl_history = get_fpl_user_history_and_season(player_id)
        except Exception as e:
            messages.error(request, f"Failure updating your profile: "
                                    f"{format(e)}")
            return redirect('/user-profile/')
        user = request.user
        update_user(user, user_fpl)
        update_user_history(user, user_fpl_history)
        user_fpl_season = user_fpl_history['current']
        update_user_season(user, user_fpl_season)
        messages.success(request, "Your Profile was succesfully updated.")
        return redirect('/user-profile/')


def DownloadDataJSON():
    try:
        download_json()
        ctx = {'event': 'success', 'info': 'Data has been downloaded to JSON'}
        return ctx
    except Exception as e:
        ctx = {'event': 'error', 'error': format(e)}
        return ctx


def PopulateTables():
    # data = read_json()  ## Read data from JSON file on disk
    data = get_data()  # Read data from Fantasy Premier League API
    teams = data['teams']
    positions = data['element_types']
    players = data['elements']
    events = data['events']
    total_players = data['total_players']
    try:
        update_teams(teams)
        populate_positions(positions)
        update_players(players)
        update_events(events, total_players)
        ctx = {'event': 'success',
               'info': 'Tables Team, Position, Player & Event has been populated.'}
        return ctx
    except Exception as e:
        ctx = {'event': 'error', 'error': format(e)}


def UpdateTables():
    # data = read_json()  ## Read data from JSON file on disk
    data = get_data()  # Read data from Fantasy Premier League API
    teams = data['teams']
    players = data['elements']
    events = data['events']
    total_players = data['total_players']
    try:
        update_teams(teams)
        update_players(players)
        update_events(events, total_players)
        ctx = {'event': 'success',
            'info': 'Tables Team, Player & Event in database has been updated.'}
        return ctx
    except Exception as e:
        ctx = {'event': 'error', 'error': format(e)}
        return ctx


class GetDataView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        ctx = {'form': GetDataForm}
        return render(request, 'get_data.html', ctx)

    def post(self, request):
        form = GetDataForm(request.POST)
        ctx = {}
        if form.is_valid():
            choice = int(form.cleaned_data['choice'])
            if choice == 0:
                ctx = DownloadDataJSON()
            elif choice == 1:
                ctx = PopulateTables()
            else:
                ctx = UpdateTables()
            ctx['form'] = GetDataForm
            return render(request, 'get_data.html', ctx)


class GetPlayersHistoryView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_player'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        ctx = {'form': GetPlayerDataForm()}
        return render(request, 'get_player_data.html', ctx)

    def post(self, request):
        form = GetPlayerDataForm(request.POST)
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
                           'form': GetPlayerDataForm()}
                    return render(request, "get_player_data.html", ctx)
                except Exception as e:
                    ctx = {'event': 'error', 'error': format(e),
                           'form': GetPlayerDataForm()}
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
                               'form': GetPlayerDataForm()}
                        return render(request, "get_player_data.html", ctx)

                ctx = {'event': 'success',
                       'info': f'Data for players in {team} has been updated',
                       'form': GetPlayerDataForm()}
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
                               'form': GetPlayerDataForm()}
                        return render(request, "get_player_data.html", ctx)

                ctx = {'event': 'success',
                       'info': f'Data for players has been updated',
                       'form': GetPlayerDataForm()}
                return render(request, "get_player_data.html", ctx)
            else:
                ctx = {'form': GetPlayerDataForm()}
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
                    update_fixture(fixture)
                    ctx = {'event': 'success', 'info': 'Fixture downloaded',
                            'form': GetFixtureForm()}
                    return render(request, 'get_fixture.html', ctx)
                except Exception as e:
                    ctx = {'event': 'error', 'error': format(e),
                           'form': GetFixtureForm()}
                    return render(request, "page-event.html", ctx)
                    
