import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse, request
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics

from fantasy_pl.serializers import TeamSerializer, PlayerSerializer
from .forms import LoginForm, SearchForm, CreateUserForm, ResetPasswordForm, MessageForm
from .getters import read_json
from .models import Team, Player, Position, Message


class IndexView(View):

    def get(self, request):
        # Random team
        team = list(Team.objects.all())
        random.shuffle(team)
        photo = "/static/logos/" + team[0].short_name.lower() + ".png "
        cnt = len(Player.objects.filter(team=team[0]))
        # Random player
        player = list(Player.objects.all())
        random.shuffle(player)
        tp = Team.objects.get(name=player[0].team)
        tpphoto = "/static/logos/" + tp.short_name.lower() + ".png "
        # Random statistic
        stats_names = ['goals_scored', 'minutes', 'assists', 'own_goals', 'penalties_saved', 'yellow_cards',
                       'red_cards']
        random.shuffle(stats_names)
        s_name = stats_names[0]

        # rename = Player.objects.extra(select={'stat': s_name}).values('stat')
        # stat = rename.order_by('-stat')[:10]
        # Foo.objects.filter(cond=1).extra(select={'sth_shiny': 'my_field'})
        rename = Player.objects.extra(select={'stat': s_name, 'id': 'id', 'name': 'second_name'})
        rename2 = Player.objects.select_related('team')
        rename.union(rename2)
        stat = rename.order_by('-stat')[:10]

        name_stat = s_name.replace('_', ' ').capitalize()
        ctx = {'title': 'Landing page', 'team': team[0], 'cnt': cnt, 'photo': photo, 'player': player[0], 'tp': tp,
               'tpphoto': tpphoto, 'stat': stat, 'name_stat': name_stat}
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
                # request.session['user_id'] = User.id
                return render(request, 'components/login.html', {'form': LoginForm(), 'unsuccessful': True})

        return redirect('/')


def LogoutView(request):
    logout(request)
    return redirect('/')


class CreateUserView(View):

    def get(self, request):
        return render(request, 'components/create_user.html', {'form': CreateUserForm()})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Don't use User.objects.create() as it won't hash the password!
            # ...need to: user.set_password()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            return redirect('/login')
        else:
            return render(request, 'components/create_user.html', {'form': form})


class ChangetPasswordView(LoginRequiredMixin, View):
    login_url = '/login'
    permission_required = 'exercises.change_user'

    # user_id = request.user.id

    def get(self, request, user_id):
        try:
            if 'user_name' in request.session:
                username = request.session['user_name']
                user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        return render(request, 'components/change_password.html', {
            'form': ResetPasswordForm(initial={
                'user_id': user_id
            }),
            'logged_user': request.user.username
        })

    def post(self, request, user_id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return redirect('/')
        else:
            return render(request, 'components/change_password.html', {'form': form, 'unsuccessful': True})


class SendMessageView(View):

    def get(self, request):
        form = MessageForm()
        return render(request, 'components/message_sending.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = User.objects.get(username=form.cleaned_data['recipient'])
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            ctx = {'form': MessageForm()}
            try:
                Message.objects.create(subject=subject, content=content, recipient=recipient, sender=request.user)
                ctx['success'] = 'Message was sent!'
            except:
                ctx['failure'] = 'Something went wrong!'

            return render(request, 'components/message_sending.html', ctx)


class MessageReceivedView(View):

    def get(self,request):
        messages = Message.objects.filter(recipient=request.user.id).order_by('date_sent')
        return render(request, 'components/message_received.html',{'messages': messages})


class MessageSentView(View):

    def get(self,request):
        messages = Message.objects.filter(sender=request.user.id).order_by('date_sent')
        return render(request, 'components/message_sent.html',{'messages': messages})


class PopulateTeamsView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        try:
            teams = data['teams']
            for t in teams:
                team = Team()
                team.id = int(t['id'])
                team.draw = t['draw']
                team.form = t['form']
                team.loss = t['loss']
                team.name = t['name']
                team.played = t['played']
                team.points = t['points']
                team.position = t['position']
                team.short_name = t['short_name']
                team.strength = t['strength']
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


class UpdateTeamsView(PermissionRequiredMixin, View):
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


class TeamView(View):

    def get(self, request, id, sort='id'):
        team = Team.objects.get(id=id)
        if sort in ['points_per_game', 'influence', 'now_cost', 'creativity', 'threat']:
            sort = '-' + sort
        players = Player.objects.filter(team=team.id).order_by(sort)
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        cnt = len(players)
        ctx = {'team': team, 'players': players, 'cnt': cnt, 'photo': photo, 'title': team.name}
        return render(request, 'components/team.html', ctx)


class ApiTeamsListView(generics.ListCreateAPIView):
    queryset = Team.objects.all().order_by('id')
    serializer_class = TeamSerializer


class ApiTeamsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class PopulatePositionsView(PermissionRequiredMixin, View):
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
                pos.name_short = p['singular_name_short']
                pos.save()
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Position database has been populated.'}
        return render(request, "components/event.html", ctx)


class PopulatePlayersView(PermissionRequiredMixin, View):
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
                player.now_cost = p['now_cost'] / 10
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


class UpdatePlayersView(PermissionRequiredMixin, View):
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
                player.now_cost = p['now_cost'] / 10
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


class PlayerView(View):

    def get(self, request, id):
        player = Player.objects.get(id=id)
        team = Team.objects.get(name=player.team)
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        ctx = {'team': team, 'player': player, 'photo': photo, 'title': player}
        return render(request, 'components/player.html', ctx)


class ApiPlayersListView(generics.ListCreateAPIView):
    queryset = Player.objects.all().order_by('id')
    serializer_class = PlayerSerializer


class ApiPlayersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


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
        return render(request, 'components/stats.html', ctx)


class SearchView(View):

    def get(self, request):
        form = SearchForm(request.GET)
        if form.is_valid():
            query_search = form.cleaned_data['search']
        q_players = Player.objects.filter(
            Q(first_name__icontains=query_search) | Q(second_name__icontains=query_search)).order_by(
            '-selected_by_percent')
        ctx = {'players': q_players, 'title': 'Search'}
        return render(request, 'components/search.html', ctx)
