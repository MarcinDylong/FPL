import operator
import random
from functools import reduce

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics

from fantasy_pl.serializers import TeamSerializer, PlayerSerializer, UserTeamSerializer
from .forms import LoginForm, SearchForm, CreateUserForm, ResetPasswordForm, MessageForm, UserTeamForm, AdvSearchForm, \
    GetDataForm
from .getters import read_json, get_data, get_individual_player_data, populate_teams, populate_players, update_players, \
    populate_positions, update_teams, get_player_data, get_player_fixture
from .models import Team, Player, Position, Message, UserTeam, PlayerHistory, Fixture


class IndexView(View):

    def get(self, request):
        ctx={'title': 'Landing page'}
        # Random team
        try:
            team = list(Team.objects.all())
            random.shuffle(team)
            photo = "/static/logos/" + team[0].short_name.lower() + ".png "
            cnt = len(Player.objects.filter(team=team[0]))
            ctx['team'] = team[0]
            ctx['cnt'] = cnt
            ctx['photo'] = photo
        except:
            pass
        # Random player
        try:
            player = list(Player.objects.all())
            random.shuffle(player)
            tp = Team.objects.get(name=player[0].team)
            tpphoto = "/static/logos/" + tp.short_name.lower() + ".png "
            ctx['player'] = player[0]
            ctx['tp'] = tp
            ctx['tpphoto'] = tpphoto
        except:
            pass
        # Random statistic
        try:
            stats_names = ['goals_scored', 'minutes', 'assists', 'own_goals', 'penalties_saved', 'yellow_cards',
                           'red_cards']
            random.shuffle(stats_names)
            s_name = stats_names[0]
            rename = Player.objects.extra(select={'stat': s_name, 'id': 'id', 'name': 'second_name'})
            rename_t = Player.objects.select_related('team')
            rename.union(rename_t)
            stat = rename.order_by('-stat')[:10]
            name_stat = s_name.replace('_', ' ').capitalize()
            ctx['stat'] = stat
            ctx['name_stat'] = name_stat
        except:
            pass

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
        ctx['novelty'] = round(novelty / 15, 1)
        uteam.novelty = round(novelty / 15, 1)
        uteam.save()

        # ratio = []
        # for u in luteam:
        #     ratio.append({'Player': str(u), 'Value': round(u.points_per_game/u.now_cost)})
        #
        # ctx['data'] = json.dumps(ratio)

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
    lookup_url_kwarg = 'format=JSON'


class ApiUserTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTeam.objects.all()
    serializer_class = UserTeamSerializer


class DownloadDataView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        try:
            get_data()
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
        # data = get_data() ## Read data from JSON file from Fantasy Premier League API
        teams = data['teams']
        try:
            populate_teams(teams)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Teams database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdateTeamsView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from JSON file from Fantasy Premier League API

        teams = data['teams']
        try:
            update_teams(teams)
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
        players = Player.objects.filter(team=team.id).order_by(sort, 'id')
        fixtures_a = Fixture.objects.filter(team_a=team).filter(is_home=False)
        fixtures_h = Fixture.objects.filter(team_h=team).filter(is_home=True)
        fixtures = fixtures_a | fixtures_h
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        cnt = len(players)
        ctx = {'team': team, 'players': players, 'cnt': cnt, 'photo': photo, 'title': team.name, 'fixtures': fixtures}
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
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from JSON file from Fantasy Premier League API
        positions = data['element_types']
        try:
            populate_positions(positions)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Position database has been populated.'}
        return render(request, "components/event.html", ctx)


class PopulatePlayersView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from JSON file from Fantasy Premier League API
        players = data['elements']
        try:
            populate_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Players database has been populated.'}
        return render(request, "components/event.html", ctx)


class UpdatePlayersView(PermissionRequiredMixin, View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()  ## Read data from JSON file on disk
        # data = get_data() ## Read data from JSON file from Fantasy Premier League API
        players = data['elements']
        try:
            update_players(players)
        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
            return render(request, "components/event.html", ctx)

        ctx = {'event': 'Success!', 'info': 'Players database has been updated.'}
        return render(request, "components/event.html", ctx)


class GetIndividualPlayerDataView(PermissionRequiredMixin, View):
    permission_required = 'fanatasy_pl.add_player'

    def get(self, request, id):
        try:
            data = get_individual_player_data(id)
            history = data['history']
            get_player_data(history)
            fixture = data['fixtures']
            get_player_fixture(fixture, history[0]['element'])

            ctx = {'event': 'Success!', 'info': f'Data for player {id} has been updated'}
            return render(request, "components/event.html", ctx)

        except Exception as e:
            ctx = {'event': 'Error occured', 'error': format(e)}
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
                    ctx = {'successful': True, 'info': f'Data for player {id} has been updated', 'title': "Get data",
                           'form': GetDataForm()}
                    return render(request, "components/get_data.html", ctx)
                except Exception as e:
                    ctx = {'unsuccessful': True, 'info': 'Error occured', 'error': format(e), 'title': "Get data",
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
                        ctx = {'unsuccessful': True, 'info': 'Error occured', 'error': format(e), 'title': "Get data",
                               'form': GetDataForm()}
                        return render(request, "components/event.html", ctx)

                ctx = {'successful': True, 'info': f'Data for players in {team} has been updated',
                       'title': "Get data", 'form': GetDataForm()}
                return render(request, "components/get_data.html", ctx)
            else:
                ctx = {'title': "Get data", 'form': GetDataForm()}
                return render(request, 'components/get_data.html', ctx)


class PlayerView(View):

    def get(self, request, id):
        player = Player.objects.get(id=id)
        games = PlayerHistory.objects.filter(player=player).order_by('-kickoff_time')
        team = Team.objects.get(name=player.team)
        fixtures_a = Fixture.objects.filter(team_a=team).filter(is_home=False)
        fixtures_h = Fixture.objects.filter(team_h=team).filter(is_home=True)
        fixtures = fixtures_a | fixtures_h
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        ctx = {'team': team, 'player': player, 'photo': photo, 'title': player, 'games': games, 'fixtures': fixtures}
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
            ctx = {'players': q_players, 'title': 'Search', 'adv_form': adv_form, 'stat': stat, 'pos': pos}
            return render(request, 'components/search.html', ctx)
        else:
            ctx = {'adv_form': AdvSearchForm(request.POST), 'title': 'Search', 'failure': True}
            return render(request, 'components/search.html', ctx)
