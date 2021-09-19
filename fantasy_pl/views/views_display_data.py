from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q, Max, Min
from django.shortcuts import render
from django.views import View
from collections import OrderedDict

import json

from fantasy_pl.forms import SearchForm, PlayerSearchForm, UserTeamForm, \
    GetUserteamForm, ChartForm, PlayerChartForm
from fantasy_pl.models import Team, Player, PlayerHistory, Fixtures, Position, \
    UserTeam, Event, UserFpl, UserFplSeason, UserFplPicks

from fantasy_pl.views.views_download_data import DownloadUserView
from fantasy_pl.views.pandas import players_ctx, player_gwByGw

class IndexView(LoginRequiredMixin, View):
    """
    Dashboard with information about current players performance
    """    
    login_url = '/login'

    def season_best_eleven(self, players_raw, parameter: str, 
        additional_parameter = '-minutes'):
        """Determine best 11 for season by given paramater

        Args:
            players_raw (ORM querries): Django querry with players data
            parameter (str): Parameter to determine best eleven by

        Returns:
            [ORM querries]: Querries of 11 selected players
        """        
        ### Divide by position
        gk = players_raw.filter(position=(Position.objects.get(id=1)))
        df = players_raw.filter(position=(Position.objects.get(id=2)))
        md = players_raw.filter(position=(Position.objects.get(id=3)))
        fw = players_raw.filter(position=(Position.objects.get(id=4)))
        ### All season best parameter
        season_best_gk = gk.order_by(parameter, additional_parameter)[:1]
        season_best_df = df.order_by(parameter, additional_parameter)[:5]
        season_best_md = md.order_by(parameter, additional_parameter)[:5]
        season_best_fw = fw.order_by(parameter, additional_parameter)[:3]
        ### Every team has to have at least one GKP, two DEFs and MIDs and one
        ### FWD's; The remaining five places in the squad should be filled by 
        ### the players with the highest score, regardless of their position
        core_of_squad = (season_best_gk | season_best_df[:2] | \
            season_best_md[:2] | season_best_fw[:1])
        rest_of_squad = (season_best_df[2:] | season_best_md[2:] | \
            season_best_fw[1:]).order_by(parameter, additional_parameter)[:5]
        ### Add all querries together and order by postion
        season_best = (core_of_squad | rest_of_squad).order_by('position_id')

        return season_best

    def gw_best_eleven(self, phistory_raw, parameter: str, 
        additional_parameter = 'bps'):
        """Determine best 11 for for current GW by given paramater

        Args:
            phistory_raw (ORM querries): Django querry with players data
            parameter (str): Parameter to determine best eleven by

        Returns:
            [ORM querries]: Querries of 11 selected players
        """  
        ### Divide by position
        gk = phistory_raw.filter(position=1)
        df = phistory_raw.filter(position=2)
        md = phistory_raw.filter(position=3)
        fw = phistory_raw.filter(position=4)
        ### GW best parameter
        gw_best_gk = gk.order_by(parameter, additional_parameter)[:1]
        gw_best_df = df.order_by(parameter, additional_parameter)[:5]
        gw_best_md = md.order_by(parameter, additional_parameter)[:5]
        gw_best_fw = fw.order_by(parameter, additional_parameter)[:3]
        ### Every team has to have at least one GKP, two DEFs and MIDs and one
        ### FWD's; The remaining five places in the squad should be filled by 
        ### the players with the highest score, regardless of their position
        core_of_squad = (gw_best_gk | gw_best_df[:2] | gw_best_md[:2] | \
            gw_best_fw[:1])
        rest_of_squad = (gw_best_df[2:] | gw_best_md[2:] | gw_best_fw[1:]) \
            .order_by(parameter, additional_parameter)[:5]
        ### Add all querries together and order by postion
        best_gw_squad = (core_of_squad | rest_of_squad).order_by('position')

        return best_gw_squad

    def get(self, request):
        ctx = {}
        ctx['segment'] = 'home'
        players_raw = Player.objects.filter(minutes__gt=0)
        try:
            gw = Fixtures.objects.filter(finished=True).order_by('event') \
            .last().event
        except:
            gw = 1
        phistory_raw = PlayerHistory.objects.filter(event=gw) \
        .filter(minutes__gt=0)

        ### Player availability
        avl = players_raw.filter(chance_of_playing_this_round__lt=100) \
            .filter(~Q(news__contains='Joined')) \
            .order_by('chance_of_playing_this_round')
        ctx['avl'] = avl
        ### Transfers In of current GW
        tri = players_raw.order_by('-transfers_in_event')[:5]
        ctx['tri'] = tri
        ### Transfers Out of current GW
        tro = players_raw.order_by('-transfers_out_event')[:5]
        ctx['tro'] = tro
        try:
            ctx['ball'] = self.season_best_eleven(players_raw, '-total_points')
            ctx['popular'] = self.season_best_eleven(players_raw,
                                                     '-selected_by_percent')
            ctx['gwbest'] = self.gw_best_eleven(phistory_raw, '-total_points')
            ctx['gwbonus'] = self.season_best_eleven(players_raw, '-bonus')
        except:
            pass
        return render(request, 'index.html', ctx)


def view_400(request, *args, **kwargs):
    """
    Error 400 handler
    """    
    return render(request, 'page-400.html')


def view_403(request, *args, **kwargs):
    """
    Error 403 handler
    """
    return render(request, 'page-403.html')


def view_404(request, *args, **kwargs):
    """
    Error 404 handler
    """
    return render(request, 'page-404.html')


def view_500(request, *args, **kwargs):
    """
    Error 500 handler
    """
    return render(request, 'page-500.html')


class TeamView(View):
    """
    View for BPL teams informations
    """    

    def get(self, request, id):
        team = Team.objects.get(id=id)
        players = Player.objects.filter(team=team.id)
        played_a = PlayerHistory.objects.filter(team_a=team) \
            .filter(is_home=False).filter(finished=True) \
            .order_by('kickoff_time').distinct('kickoff_time')
        played_h = PlayerHistory.objects.filter(team_h=team) \
            .filter(is_home=True).filter(finished=True) \
            .order_by('kickoff_time').distinct('kickoff_time')
        played = played_a | played_h
        fixtures_a = PlayerHistory.objects.filter(team_a=team) \
            .filter(is_home=False).filter(finished=False) \
            .filter(event__isnull=False).order_by('kickoff_time') \
            .distinct('kickoff_time')
        fixtures_h = PlayerHistory.objects.filter(team_h=team) \
            .filter(is_home=True).filter(finished=False) \
            .filter(event__isnull=False).order_by('kickoff_time') \
            .distinct('kickoff_time')
        fixtures = fixtures_a | fixtures_h
        photo = "/static/assets/images/logos/" + team.short_name.lower() + ".png "
        cnt = len(players)
        ctx = {'team': team, 'players': players, 'cnt': cnt, 'photo': photo,
               'title': team.name, 'fixtures': fixtures, 'played': played}
        return render(request, 'team.html', ctx)


class PlayerView(View):
    """
    View for BPL players informations
    """ 
    def get_data(self, id, form, category='selected'):
        ## Django ORMs
        player = Player.objects.get(id=id)
        team_id = player.team.id
        hist = PlayerHistory.objects.filter(player=player) \
            .filter(finished=True) \
            .order_by('-kickoff_time')
        games = PlayerHistory.objects.filter(player=player) \
            .filter(event__isnull=False).filter(finished=False) \
            .filter(Q(team_a_id=team_id) | Q(team_h_id=team_id)) \
            .order_by('kickoff_time')
        ## Data preparation for display
        chart = hist.order_by('kickoff_time')
        team = Team.objects.get(id=team_id)
        photo = "/static/logos/" + team.short_name.lower() + ".png "
        ## Data for chart
        overall = player_gwByGw(hist,category)

        ## Pass data to context
        ctx = {
            'team': team,
            'player': player,
            'photo': photo,
            'title': player,
            'games': games,
            'hist': hist,
            'chart': chart,
            'form': form,
            'overall': overall       
            }

        return ctx

    def get(self, request, id):
        ## Form 
        form = PlayerChartForm()
        ## Context
        ctx = self.get_data(id, form)

        return render(request, 'player.html', ctx)

    def post(self, request, id):
        ## Form
        form = PlayerChartForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['stat']
        else:
            category = 'selected'
        ## Context
        ctx = self.get_data(id, form, category)

        return render(request, 'player.html', ctx)

     
class StandingsView(View):
    """
    View with BPL table
    """    
    def get(self, request):
        table = Team.objects.all().order_by('position')
        ctx = {'table': table, 'title': 'Table', 'segment': 'standings'}
        return render(request, 'standings.html', ctx)


class FixtureView(View):
    """
    View with fixture for BPL Season
    """    

    def get(self, request):
        fix_list = []
        for i in range(1,39):
            fix_list.append(Fixtures.objects.filter(event=i).order_by('kickoff_time'))
        curr_event = Fixtures.objects.filter(finished=True).order_by('kickoff_time').last().event.id
        # tbd = Fixtures.objects.filter(event__isnull=True)
        paginator = Paginator(fix_list, 1)
        page = request.GET.get('page', curr_event)
        fixture = paginator.get_page(page)
        ctx = {'fixture': fixture, 'title': 'Fixtures', 'segment': 'fixtures'}
        return render(request, 'fixtures.html', ctx)


class StatsView(View):
    """
    Players statistic view
    """    
    def get(self, request):
        ctx = {'title': 'Stats'}
        ctx['stats'] = Player.objects.filter(minutes__gt=0)
        return render(request, 'stats.html', ctx)


class StatsChartView(View):
    """
    Statistic for player on given position in form of Bubble Charts
    """
   
    def get(self, request, id):
        ctx = {'title': 'Chart'}
        form = ChartForm()
        ## Return ctx for Goalkeepers
        ctx = players_ctx(pos=id, ctx=ctx, form=form)
        return render(request, 'stats_pos.html', ctx)
    
    def post(self, request, id):
        ctx = {'title': 'Chart'}
        form = ChartForm(request.POST)

        if form.is_valid():
            x_axis = form.cleaned_data['x_axis']
            y_axis = form.cleaned_data['y_axis']
            size_points = form.cleaned_data['size_points']
            limit = form.cleaned_data['limit']
            ctx = players_ctx(pos=id, ctx=ctx, form=form, x_axis=x_axis,
                y_axis=y_axis, size=size_points, limit=limit)
        else:
            ctx = gkp_ctx(pos=id, ctx=ctx, form=form)

        return render(request, 'stats_pos.html', ctx)


class PlayersSearchView(View):
    """
    Player searching View
    """    
    def get(self, request):
        form = SearchForm(request.GET)
        adv_form = PlayerSearchForm()
        if form.is_valid():
            query_search = form.cleaned_data['search']
            q_players = Player.objects.filter(
                Q(first_name__icontains=query_search) |
                Q(second_name__icontains=query_search)).order_by(
                '-selected_by_percent')
            ctx = {'players': q_players, 'title': 'Search',
                   'adv_form': adv_form, 'segment': 'player-search'}
        else:
            ctx = {'title': 'Search', 'adv_form': adv_form,
                   'segment': 'player-search'}
        return render(request, 'player-search.html', ctx)

    def post(self, request):
        adv_form = PlayerSearchForm(request.POST)
        if adv_form.is_valid():
            pos = adv_form.cleaned_data['position']
            mx = adv_form.cleaned_data['max']
            q_players = Player.objects.order_by('-now_cost')

            if pos is not None:
                q_players = q_players.filter(position=pos)
            if mx is not None:
                q_players = q_players.filter(now_cost__lte=mx)

            ctx = {'players': q_players, 'title': 'Search',
                   'adv_form': adv_form, 'pos': pos,
                   'segment': 'player-search'}
            return render(request, 'player-search.html', ctx)
        else:
            ctx = {'adv_form': PlayerSearchForm(request.POST),
                   'title': 'Search', 'failure': True,
                   'segment': 'player-search'}
            return render(request, 'player-search.html', ctx)


class UserTeamView(View):
    """
    View for planning next gameweek team
    """    
    def team_overall(self, uteam, ctx):
        """Determine overall stats for user team and adding it to template 
        context data

        Args:
            uteam (model_instance): Instance of model UserTeam
            ctx (context_data): Template context data

        Returns:
            ctx: updated context data
        """        
        luteam = [uteam.gkp1, uteam.gkp2, uteam.def1, uteam.def2, uteam.def3,
                  uteam.def4, uteam.def5, uteam.mid1, uteam.mid2, uteam.mid3,
                  uteam.mid4, uteam.mid5, uteam.fwd1, uteam.fwd2, uteam.fwd3]
        ctx['uteam'] = luteam

        overall_cost = sum([u.now_cost for u in luteam])
        ctx['overall_cost'] = uteam.overall_cost = round(overall_cost, 1)
        if overall_cost > 100:
            ctx['overpaid'] = round(overall_cost - 100, 2)

        ppg = sum([u.points_per_game for u in luteam])
        ctx['ppg'] = uteam.ppg = round(ppg, 1)

        influence = sum([u.influence for u in luteam])
        ctx['influence'] = uteam.influence = round(influence, 1)

        creativity = sum([u.creativity for u in luteam])
        ctx['creativity'] = uteam.creativity = round(creativity, 1)

        threat = sum([u.threat for u in luteam])
        ctx['threat'] = uteam.threat = round(threat, 1)

        dreamteam = sum([u.dreamteam_count for u in luteam])
        ctx['dreamteam'] = uteam.dt_apps = round(dreamteam, 1)

        total_points = sum([u.total_points for u in luteam])
        ctx['total_points'] = uteam.total_points = round(total_points, 1)

        novelty = sum([u.selected_by_percent for u in luteam])
        ctx['novelty'] = uteam.novelty = round(novelty / 15, 1)

        uteam.save()
        return ctx

    def get(self, request):
        ctx = {'title': 'UserTeam'}
        form = UserTeamForm()
        form_gut = GetUserteamForm()
        ctx['form'] = form
        ctx['form_gut'] = form_gut
        ctx['segment'] = 'user-team'

        try:
            profile = UserFpl.objects.get(user=request.user)
            if profile.fpl:
                form_gut.fields['fpl_id'].initial = profile.fpl
        
            if UserTeam.objects.get(user=request.user):
                uteam = UserTeam.objects.get(user=request.user)
                form.fields['gkp1'].initial = uteam.gkp1_id
                form.fields['gkp2'].initial = uteam.gkp2_id
                form.fields['def1'].initial = uteam.def1_id
                form.fields['def2'].initial = uteam.def2_id
                form.fields['def3'].initial = uteam.def3_id
                form.fields['def4'].initial = uteam.def4_id
                form.fields['def5'].initial = uteam.def5_id
                form.fields['mid1'].initial = uteam.mid1_id
                form.fields['mid2'].initial = uteam.mid2_id
                form.fields['mid3'].initial = uteam.mid3_id
                form.fields['mid4'].initial = uteam.mid4_id
                form.fields['mid5'].initial = uteam.mid5_id
                form.fields['fwd1'].initial = uteam.fwd1_id
                form.fields['fwd2'].initial = uteam.fwd2_id
                form.fields['fwd3'].initial = uteam.fwd3_id
                self.team_overall(uteam, ctx)
        except:
            pass

        return render(request, 'user-team.html', ctx)

    def post(self, request):
        form = UserTeamForm(request.POST)
        ctx = {}
        ctx['segment'] = 'user-team'
        if form.is_valid():
            try:
                userTeam = UserTeam.objects.filter(user=request.user).last()
                userTeam.gkp1 = form.cleaned_data['gkp1']
                userTeam.gkp2 = form.cleaned_data['gkp2']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.def5 = form.cleaned_data['def5']
                userTeam.mid1 = form.cleaned_data['mid1']
                userTeam.mid2 = form.cleaned_data['mid2']
                userTeam.mid3 = form.cleaned_data['mid3']
                userTeam.mid4 = form.cleaned_data['mid4']
                userTeam.mid5 = form.cleaned_data['mid5']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.fwd3 = form.cleaned_data['fwd3']
                userTeam.save()
                ctx['success'] = 'Team updated'
            except ObjectDoesNotExist:
                userTeam = UserTeam()
                userTeam.user = request.user
                userTeam.gkp1 = form.cleaned_data['gkp1']
                userTeam.gkp2 = form.cleaned_data['gkp2']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.def5 = form.cleaned_data['def5']
                userTeam.mid1 = form.cleaned_data['mid1']
                userTeam.mid2 = form.cleaned_data['mid2']
                userTeam.mid3 = form.cleaned_data['mid3']
                userTeam.mid4 = form.cleaned_data['mid4']
                userTeam.mid5 = form.cleaned_data['mid5']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.fwd3 = form.cleaned_data['fwd3']
                userTeam.save()
                ctx['success'] = 'Team created'
        else:
            ctx['failure'] = True
            
        uteam = UserTeam.objects.filter(user=request.user).last()
        self.team_overall(uteam, ctx)
        ctx['form'] = form
        ctx['form_gut'] = GetUserteamForm()
        return render(request, 'user-team.html', ctx)


class UserProfile(View):
    """
    Display User profile data
    """  

    def dict_picks(self, user_season):
        """Creating easy callable in template dictonaries based on UserFplPicks 
        instances for given User

        Args:
            userFplSeason (model_instances): Queries of UserFplSeason for given 
            User

        Returns:
            dict: Dictonary of dictionaries under keys 1-38 where key is a 
            number of Gameweek, number of dictionaries may vary depend of User 
            and already finished gameweeks;
            Every GameWeek dictionary containts another 15 dictionaries (pck1 - 
            pck15) which represtens every element picked to the user team on 
            given GW.
            Finally pck[x] dictionaries contains key-value pairs:
            player: Model instance of Player
            pos: Intiger used for sorting players picks
            mult: Multiplier for elements on given GW
            cpt: Bool value which determine whether element was captain on GW
            vcpt: Bool value which determine whether element was vicecaptain on 
            GW
            last_game: Player model functions returing string of game played 
            on given Gameweek
            last_game_stats: Player model functions returning PlayerHistory
            instance for given player on given gameweek
        """    

        end = len(user_season)
        picks = OrderedDict()

        for i in range(end):
            inst = user_season[i]
            gw = inst.event.id
            pick = UserFplPicks.objects.get(user=inst)#.order_by('id')
            
            pick = pick.__dict__
            del pick['_state']
            del pick['id']
            del pick['user_id']

            team = OrderedDict()
            for k, v in pick.items():
                k = k.split('_')
                if k[1] == 'id':
                    player = Player.objects.get(id=v)
                    team[f'{k[0]}'] = {'player': player}
                    team[f'{k[0]}']['last_game'] = player.last_game(gw)
                    team[f'{k[0]}']['last_game_stats'] = PlayerHistory.objects.filter(player=player, event_id=gw).first()
                    ## For double game during event sum up points
                    phistory = PlayerHistory.objects.filter(player=player, event_id=gw)
                    team[f'{k[0]}']['last_game_event'] = gw
                    team[f'{k[0]}']['last_game_points'] = 0
                    team[f'{k[0]}']['last_game_bonus'] = 0
                    team[f'{k[0]}']['last_game_value'] = 0
                    team[f'{k[0]}']['last_event_games'] = len(phistory)
                    if len(phistory) > 0:
                        for ph in phistory:
                            team[f'{k[0]}']['last_game_points'] += ph.total_points
                            team[f'{k[0]}']['last_game_bonus'] += ph.bonus
                            team[f'{k[0]}']['last_game_value'] += ph.value 
                elif k[1] == 'pos':
                    team[f'{k[0]}']['pos'] = v + i*15
                else:
                    team[f'{k[0]}'][f'{k[1]}'] = v 
            picks[gw] = team

        return picks


    def get(self, request):
        user = request.user
        ctx = {'title': 'UserProfile'}
        form = GetUserteamForm()
        try:
            ## Profile
            profile = UserFpl.objects.get(user=user)
            if profile.fpl:
                form.fields['fpl_id'].initial = profile.fpl
            ctx['profile'] = profile
            ## Event
            event = Event.objects.get(id=profile.current_event)
            ctx['event'] = event
            ## User history
            for h in profile.chips:
                ctx[h['name']] = h['event']
            ## User season
            user_season = UserFplSeason.objects.filter(userfpl=profile).order_by('event_id')
            ctx['season'] = user_season
            ## User Picks
            picks = self.dict_picks(user_season)
            ctx['picks'] = picks
            # Previous game week
            prev_gw = user_season.get(event_id=(profile.current_event - 1))
            ctx['prev'] = prev_gw
        except:
            pass
        ctx['segment'] = 'user-profile'
        ctx['form'] = form
        return render(request, 'user-profile.html', ctx)


class UserProfileTrans(View):
    def get(self, request):
        ## Get Data from database
        user = request.user
        userFpl = UserFpl.objects.get(user=user)
        userSeason = UserFplSeason.objects.filter(userfpl=userFpl).order_by('event_id')
        userFplPick = UserFplPicks.objects.filter(user=userSeason.last()).order_by('id').last()
        gw = Fixtures.objects.filter(finished=True).order_by('event_id').last().event_id

        ## Prepare yLimits for team value charts 
        min_value = userSeason.aggregate(Min('money'))['money__min'] - .5
        max_value = userSeason.aggregate(Max('money'))['money__max'] + .5
        
        ## Prepare data for transfers table
        transfers = userFpl.transfers
        for tran in transfers:
            del tran['entry']
            in_id = tran['element_in']
            out_id = tran['element_out']
            tran['element_in_cost'] /= 10
            tran['element_out_cost'] /= 10
            tran['element_in'] = Player.objects.get(id=in_id)
            tran['element_out'] = Player.objects.get(id=out_id)
            tran['diff'] = round(tran['element_out_cost'] - tran['element_in_cost'], 1)
        transfers = sorted(transfers, key=lambda i: i['event'], reverse=True)

        ## Prepare picks dict with actual squad with GW when this players join
        ## team and how long are they in team
        # Extract actual players from UserFplPicks
        userPicks = [
            userFplPick.pck1, userFplPick.pck2, userFplPick.pck3,
            userFplPick.pck4, userFplPick.pck5, userFplPick.pck6,
            userFplPick.pck7, userFplPick.pck8, userFplPick.pck9,
            userFplPick.pck10, userFplPick.pck11, userFplPick.pck12,
            userFplPick.pck13, userFplPick.pck14, userFplPick.pck15
         ]

        # Create new dicts with players and additional data 
        picks = []
        i = 0
        for up in userPicks:
            i += 1
            pick = {}
            pick['no'] = i
            pick['player'] = up
            for t in transfers:
                if t['element_in'] == up:
                    pick['since'] = t['event']
                    break
            else:
                pick['since'] = userFpl.started_event
            pick['streak'] = gw - pick['since']

            picks.append(pick)

        ## Prepare context data for template
        ctx = {
            'title': 'Transfers history',
            'transfers': transfers,
            'season': userSeason,
            'min_val': min_value,
            'max_val': max_value,
            'picks': picks
            }

        return render(request, 'user-profile-trans.html', ctx)


## Blank View for development purposes
class BlankView(View):
    """Blank view
    """    
    def get(self, request):
        return render(request, 'page-blank.html')