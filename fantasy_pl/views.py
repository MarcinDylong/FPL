from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Team, Player, Position
from .forms import LoginForm
from .getters import read_json, get_data


class IndexView(View):

    def get(self, request):
        ctx = {'title': 'Landing page'}
        return render(request, "components/index.html", ctx)


class BlankView(View):

    def get(self, request):
        ctx = {'title': "Blank Page"}
        return render(request, "components/blank.html", ctx)



class LoginView(View):

    def get(self, request):
        ctx = {'title': "Log in", 'form': LoginForm()}
        return render(request, 'components/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'components/login.html', {'form': LoginForm(), 'unsuccessful': True})

        return redirect('/login')


def LogoutView(request):
    logout(request)
    return redirect('/')


class PopulateTeamsView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        try:
            teams = data['teams']
            for t in teams:
                team = Team()
                team.id = int(t['id'])
                team.code = t['code']
                team.draw = t['draw']
                team.form = t['form']
                team.loss = t['loss']
                team.name = t['name']
                team.played = t['played']
                team.points = t['points']
                team.position = t['position']
                team.short_name = t['short_name']
                team.strength = t['strength']
                team.team_division = t['team_division']
                team.unavailable = t['unavailable']
                team.win = t['win']
                team.strength_overall_home = t['strength_overall_home']
                team.strength_overall_away = t['strength_overall_away']
                team.strength_attack_home = t['strength_attack_home']
                team.strength_attack_away = t['strength_attack_away']
                team.strength_defence_home = t['strength_defence_home']
                team.strength_defence_away = t['strength_defence_away']
                team.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Teams database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdateTeamsView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        teams = data['teams']
        try:
            for t in teams:
                team = Team.objects.get(id=t['id'])
                team.draw = t['draw']
                team.form = t['form']
                team.loss = t['loss']
                team.played = t['played']
                team.points = t['points']
                team.position = t['position']
                team.strength = t['strength']
                team.unavailable = t['unavailable']
                team.win = t['win']
                team.strength_overall_home = t['strength_overall_home']
                team.strength_overall_away = t['strength_overall_away']
                team.strength_attack_home = t['strength_attack_home']
                team.strength_attack_away = t['strength_attack_away']
                team.strength_defence_home = t['strength_defence_home']
                team.strength_defence_away = t['strength_defence_away']
                team.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Teams database has been updated.'}
        return render(request, "components/event.html", ctx)


class PopulatePositionsView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.add_position'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        positions = data['element_types']
        try:
            for p in positions:
                pos = Position()
                pos.id = int(p['id'])
                pos.name = p['singular_name']
                pos.short_name = p['singular_name_short']
                pos.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Position database has been populated.'}
        return render(request, "components/event.html", ctx)


class PopulatePlayersView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        players = data['elements']
        try:
            for p in players:
                player = Player()
                player.chance_of_playing_next_round = p['chance_of_playing_next_round']
                player.chance_of_playing_this_round = p['chance_of_playing_this_round']
                player.code = p['code']
                player.cost_change_event = p['cost_change_event']
                player.cost_change_event_fall = p['cost_change_event_fall']
                player.cost_change_start = p['cost_change_start']
                player.cost_change_start_fall = p['cost_change_start_fall']
                player.dreamteam_count = p['dreamteam_count']
                player.element_type = p['element_type']
                player.ep_next = float(p['ep_next'])
                player.ep_this = float(p['ep_this'])
                player.event_points = p['event_points']
                player.first_name = p['first_name']
                player.form = p['form']
                player.id = p['id']
                player.in_dreamteam = p['in_dreamteam']
                player.news = p['news']
                player.news_added = p['news_added']
                player.now_cost = p['now_cost']
                player.points_per_game = p['points_per_game']
                player.second_name = p['second_name']
                player.selected_by_percent = p['selected_by_percent']
                player.special = p['special']
                player.team = Team.objects.get(id=p['team'])
                player.total_points = p['total_points']
                player.value_form = float(p['value_form'])
                player.value_season = float(p['value_season'])
                player.minutes = p['minutes']
                player.goals_scored = p['goals_scored']
                player.assists = p['assists']
                player.clean_sheets = p['clean_sheets']
                player.goals_conceded = p['goals_conceded']
                player.own_goals = p['own_goals']
                player.penalties_saved = p['penalties_saved']
                player.penalties_missed = p['penalties_missed']
                player.yellow_cards = p['yellow_cards']
                player.red_cards = p['red_cards']
                player.saves = p['saves']
                player.bonus = p['bonus']
                player.bps = p['bps']
                player.influence = float(p['influence'])
                player.creativity = float(p['creativity'])
                player.threat = float(p['threat'])
                player.ict_index = float(p['ict_index'])
                player.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Players database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdatePlayersView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        players = data['elements']
        try:
            for p in players:
                player = Player.objects.get(id=p['id'])
                player.chance_of_playing_next_round = p['chance_of_playing_next_round']
                player.chance_of_playing_this_round = p['chance_of_playing_this_round']
                player.cost_change_event = p['cost_change_event']
                player.cost_change_event_fall = p['cost_change_event_fall']
                player.cost_change_start = p['cost_change_start']
                player.cost_change_start_fall = p['cost_change_start_fall']
                player.dreamteam_count = p['dreamteam_count']
                player.element_type = p['element_type']
                player.ep_next = float(p['ep_next'])
                player.ep_this = float(p['ep_this'])
                player.event_points = p['event_points']
                player.form = p['form']
                player.in_dreamteam = p['in_dreamteam']
                player.news = p['news']
                player.news_added = p['news_added']
                player.now_cost = p['now_cost']
                player.points_per_game = p['points_per_game']
                player.selected_by_percent = p['selected_by_percent']
                player.special = p['special']
                player.team = Team.objects.get(id=p['team'])
                player.total_points = p['total_points']
                player.value_form = float(p['value_form'])
                player.value_season = float(p['value_season'])
                player.minutes = p['minutes']
                player.goals_scored = p['goals_scored']
                player.assists = p['assists']
                player.clean_sheets = p['clean_sheets']
                player.goals_conceded = p['goals_conceded']
                player.own_goals = p['own_goals']
                player.penalties_saved = p['penalties_saved']
                player.penalties_missed = p['penalties_missed']
                player.yellow_cards = p['yellow_cards']
                player.red_cards = p['red_cards']
                player.saves = p['saves']
                player.bonus = p['bonus']
                player.bps = p['bps']
                player.influence = float(p['influence'])
                player.creativity = float(p['creativity'])
                player.threat = float(p['threat'])
                player.ict_index = float(p['ict_index'])
                player.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Players database has been updated.'}
        return render(request, "components/event.html", ctx)