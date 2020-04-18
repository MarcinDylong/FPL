import operator
import random
from functools import reduce

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics

from fantasy_pl.serializers import TeamSerializer, PlayerSerializer, UserTeamSerializer
from .forms import LoginForm, SearchForm, CreateUserForm, ResetPasswordForm, MessageForm, UserTeamForm, AdvSearchForm
from .getters import read_json
from .models import Team, Player, Position, Message, UserTeam


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

        rename = Player.objects.extra(select={'stat': s_name, 'id': 'id', 'name': 'second_name'})
        rename_t = Player.objects.select_related('team')
        rename.union(rename_t)
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
        ctx = {'form': CreateUserForm(), 'title': 'Create user'}
        return render(request, 'components/create_user.html', ctx)

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
            ctx = {'form': CreateUserForm(), 'title': 'Create user'}
            return render(request, 'components/create_user.html', ctx)


class ChangetPasswordView(LoginRequiredMixin, View):
    login_url = '/login'
    permission_required = 'exercises.change_user'

    def get(self, request, user_id):
        try:
            if 'user_name' in request.session:
                username = request.session['user_name']
                user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        return render(request, 'components/change_password.html', {
            'form': ResetPasswordForm(initial={
                'user_id': user_id, 'title': 'Change password'
            }),
            'logged_user': request.user.username
        })

    def post(self, request, user_id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return redirect('/login')
        else:
            return render(request, 'components/change_password.html',
                          {'form': form, 'unsuccessful': True, 'title': 'Change password'})


class SendMessageView(View):

    def get(self, request):
        form = MessageForm()
        return render(request, 'components/message_sending.html', {'form': form, 'title': 'Send Massage'})

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
                ctx['failure'] = 'Something went wrong'

            ctx['title'] = 'Send message'
            return render(request, 'components/message_sending.html', ctx)
        else:
            ctx = {'form': MessageForm()}
            ctx['failure'] = 'Cannot send message with empty Subject or content!'
            return render(request, 'components/message_sending.html', ctx)

class MessageReceivedView(View):

    def get(self, request):
        messages = Message.objects.filter(recipient=request.user.id).order_by('date_sent')
        return render(request, 'components/message_received.html', {'messages': messages, 'title': 'Received'})


class MessageSentView(View):

    def get(self, request):
        messages = Message.objects.filter(sender=request.user.id).order_by('date_sent')
        return render(request, 'components/message_sent.html', {'messages': messages, 'title': 'Sent'})


class UserTeamView(View):

    def team_overall(self, uteam, ctx):
        luteam = [uteam.gkp, uteam.def1, uteam.def2, uteam.def3, uteam.def4, uteam.mdf1, uteam.mdf2, uteam.mdf3,
                  uteam.mdf4, uteam.fwd1, uteam.fwd2, uteam.gkpb, uteam.defb, uteam.mdfb, uteam.fwdb]
        ctx['uteam'] = luteam

        overall_cost = 0
        for u in luteam:
            overall_cost += u.now_cost
        ctx['overall_cost'] = round(overall_cost, 1)
        if overall_cost > 100:
            ctx['overpaid'] = round(overall_cost - 100, 2)
        uteam.cost = round(overall_cost, 1)

        points_per_game = 0
        for u in luteam:
            points_per_game += u.points_per_game
        ctx['ppg'] = round(points_per_game, 1)
        uteam.points_per_game = round(points_per_game, 1)

        influence = 0
        for u in luteam:
            influence += u.influence
        ctx['influence'] = round(influence, 1)
        uteam.influence = round(influence, 1)

        creativity = 0
        for u in luteam:
            creativity += u.creativity
        ctx['creativity'] = round(creativity, 1)
        uteam.creativity = round(creativity, 1)

        threat = 0
        for u in luteam:
            threat += u.threat
        ctx['threat'] = round(threat, 1)
        uteam.threat = round(threat, 1)

        dreamteam = 0
        for u in luteam:
            dreamteam += u.dreamteam_count
        ctx['dreamteam'] = round(dreamteam, 1)
        uteam.dt_apps = round(dreamteam, 1)

        total_points = 0
        for u in luteam:
            total_points += u.total_points
        ctx['total_points'] = round(total_points, 1)
        uteam.total_points = round(total_points, 1)

        novelty = 0
        for u in luteam:
            novelty = novelty + u.selected_by_percent
        ctx['novelty'] = round(novelty / 11, 1)
        uteam.novelty = round(novelty / 11, 1)
        uteam.save()
        return ctx

    def get(self, request):
        ctx = {}
        form = UserTeamForm()
        ctx['form'] = form
        ctx['title'] = 'Your Team'

        if UserTeam.objects.filter(user=request.user):
            uteam = UserTeam.objects.get(user=request.user)
            form.fields['gkp'].initial = uteam.gkp_id
            form.fields['def1'].initial = uteam.def1_id
            form.fields['def2'].initial = uteam.def2_id
            form.fields['def3'].initial = uteam.def3_id
            form.fields['def4'].initial = uteam.def4_id
            form.fields['mdf1'].initial = uteam.mdf1_id
            form.fields['mdf2'].initial = uteam.mdf2_id
            form.fields['mdf3'].initial = uteam.mdf3_id
            form.fields['mdf4'].initial = uteam.mdf4_id
            form.fields['fwd1'].initial = uteam.fwd1_id
            form.fields['fwd2'].initial = uteam.fwd2_id
            form.fields['gkpb'].initial = uteam.gkpb_id
            form.fields['defb'].initial = uteam.defb_id
            form.fields['mdfb'].initial = uteam.mdfb_id
            form.fields['fwdb'].initial = uteam.fwdb_id

            self.team_overall(uteam, ctx)

        return render(request, 'components/userteam.html', ctx)

    def post(self, request):
        form = UserTeamForm(request.POST)
        ctx = {}
        ctx['title'] = 'Your Team'
        if form.is_valid():
            try:
                userTeam = UserTeam.objects.get(user=request.user)
                userTeam.gkp = form.cleaned_data['gkp']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.mdf1 = form.cleaned_data['mdf1']
                userTeam.mdf2 = form.cleaned_data['mdf2']
                userTeam.mdf3 = form.cleaned_data['mdf3']
                userTeam.mdf4 = form.cleaned_data['mdf4']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.gkpb = form.cleaned_data['gkpb']
                userTeam.defb = form.cleaned_data['defb']
                userTeam.mdfb = form.cleaned_data['mdfb']
                userTeam.fwdb = form.cleaned_data['fwdb']
                userTeam.save()
                ctx['success'] = 'Team updated'
            except ObjectDoesNotExist:
                userTeam = UserTeam()
                userTeam.user = request.user
                userTeam.gkp = form.cleaned_data['gkp']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.mdf1 = form.cleaned_data['mdf1']
                userTeam.mdf2 = form.cleaned_data['mdf2']
                userTeam.mdf3 = form.cleaned_data['mdf3']
                userTeam.mdf4 = form.cleaned_data['mdf4']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.gkpb = form.cleaned_data['gkpb']
                userTeam.defb = form.cleaned_data['defb']
                userTeam.mdfb = form.cleaned_data['mdfb']
                userTeam.fwdb = form.cleaned_data['fwdb']
                userTeam.save()
                ctx['success'] = 'Team created'

            uteam = UserTeam.objects.get(user=request.user)
            self.team_overall(uteam, ctx)
            ctx['form'] = form
            return render(request, 'components/userteam.html', ctx)
        else:
            uteam = UserTeam.objects.get(user=request.user)
            self.team_overall(uteam, ctx)
            ctx['failure'] = True
            ctx['form'] = form
            return render(request, 'components/userteam.html', ctx)


class ApiUserTeamsListView(generics.ListCreateAPIView):
    queryset = UserTeam.objects.all().order_by('id')
    serializer_class = UserTeamSerializer


class ApiUserTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTeam.objects.all()
    serializer_class = UserTeamSerializer


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

    def get(self, request, id, sort):
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
                player.position = p['element_type']
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
                player.position = p['element_type']
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

            if len(q_list)==0:
                q_players = None
            else:
                q_players = Player.objects.filter(reduce(operator.and_, q_list)).order_by('-'+stat)
                paginator = Paginator(q_players, 25)
                page = request.GET.get('page')
                q_players = paginator.get_page(page)
            ctx = {'players': q_players, 'title': 'Search', 'adv_form': adv_form, 'stat': stat, 'pos':pos}
            return render(request, 'components/search.html', ctx)
        else:
            ctx = {'adv_form': AdvSearchForm(request.POST), 'title': 'Search', 'failure':True}
            return render(request, 'components/search.html', ctx)
