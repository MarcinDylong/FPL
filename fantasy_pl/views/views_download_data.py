from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from fantasy_pl.forms import GetPlayerDataForm, GetFixtureForm, \
    GetUserteamForm, GetDataForm
from fantasy_pl.models import Player, Fixtures, Event
from fantasy_pl.views.getters import read_json, get_individual_player_data, \
    download_json, get_fixtures_for_season, get_fpl_userteam, get_data, \
    get_fpl_user, get_fpl_user_history_and_season, get_fpl_user_picks, \
    download_data_json 
from fantasy_pl.views.updates import update_teams, update_players, \
    populate_positions, update_player_data, update_player_fixture, \
    update_fixture, update_userteam, update_user, update_events, \
    update_user_history, update_user_season, update_user_picks

'''
    Views for downloading data from Fantasy Premier League API;

    Views below depend on two types of functions imported from different files:
    - getters: functions which send request to FPL API and return data in form 
               of dictionaries or lists of dictionaries
    - data_updates: functions which process data from getters and save them in 
                    database
'''
def DownloadUserteamView(request):
    """
    Donwload or update UserTeam model

    View without own template, 

    App is redirected to this view when user submit Form on site /user-team/;
    After downloading/updating UserTeam model redirected back to /user-team/.
    """
    form = GetUserteamForm(request.POST)
    if form.is_valid():
        player_id = form.cleaned_data['fpl_id']
        last_event = Event.objects.filter(finished=False).first()
        gw = last_event.id
        try:
            team = get_fpl_userteam(player_id, gw)
            players = team['picks']
            user = request.user
            update_userteam(user, players)
        except Exception as e:
            messages.error(request, f"Failure downloading your team "
                                    f"for gw {gw}: {format(e)}")

        return redirect('/user-team/')


def DownloadUserView(request):
    """
    Download and update UserProfile Model and connected to this model different
    instances of models:
    - UserFplHistory;
    - UserFplSeason;
    - UserFplPicks;

    Noticed that when UserFpl is mutable instance connected OneToOne to user 
    istances, rest of mentioned above models are immutable with Foreign key to 
    Event model. They can be override only if user provide different ID from 
    Fantasy Premier League

    App is redirected to this view when user submit Form on site /user-profile/;
    After downloading/updating UserTeam model redirected back to /user-profile/.

    """
    form = GetUserteamForm(request.POST)
    if form.is_valid():
        player_id = form.cleaned_data['fpl_id']
        last_event = Event.objects.filter(finished=false).first()
        gw = last_event.id
        ## Retrieve data from API
        try:
            user_fpl = get_fpl_user(player_id)
            user_fpl_history = get_fpl_user_history_and_season(player_id)
        except Exception as e:
            messages.error(request, f"Failure updating your profile: "
                                    f"{format(e)}")
            return redirect('/user-profile/')
        ## Update data for UserFPL
        user = request.user
        update_user(user, user_fpl)
        update_user_history(user, user_fpl_history)
        user_fpl_season = user_fpl_history['current']
        update_user_season(user, user_fpl_season)
        update_user_picks(user)
        ## Update data for UserTeam
        team = get_fpl_userteam(player_id, gw)
        players = team['picks']
        user = request.user
        update_userteam(user, players)
        ## Pass message
        messages.success(request, "Your Profile was succesfully updated.")
        return redirect('/user-profile/')


def PopulateTables():
    """
    Populate Tables for models:
    - Team;
    - Position;
    - Players;
    - Events;
    """

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
    """
    Update Tables for models:
    - Team;
    - Position;
    - Players;
    - Events;
    """
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
    """
    View for manual updating data for tables:
    - Team;
    - Players;
    - Events;
    """
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
                ctx = download_data_json()
            elif choice == 1:
                ctx = PopulateTables()
            else:
                ctx = UpdateTables()
            ctx['form'] = GetDataForm
            return render(request, 'get_data.html', ctx)


class GetPlayersHistoryView(PermissionRequiredMixin, View):
    """
    View for manual updating data for table:
    - PlayerHistory
    """
    
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
                    update_player_data(history)
                    game = data['fixtures']
                    update_player_fixture(game, id)
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
                        update_player_data(history)
                        game = data['fixtures']
                        update_player_fixture(game, p.id)
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
                        update_player_data(history)
                        game = data['fixtures']
                        update_player_fixture(game, p.id)
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
    """
    View for manual updating data for tables:
    - Fixtures;
    """
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