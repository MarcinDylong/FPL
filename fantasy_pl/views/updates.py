import json
import time
import bs4 as bs
import urllib.request

import requests

from fantasy_pl.models import Team, Position, Player, PlayerHistory, Fixtures, \
    UserTeam, UserFpl, Event, UserFplSeason, UserFplPicks
from fantasy_pl.views.getters import league_table_scraper, get_fpl_user_picks


'''
    Functions for update/create data in database
'''


def update_teams(teams):
    """Update or create teams table and save in database

    Args:
        teams (dict): Retrieved data from API
    """    
    
    perf = league_table_scraper()
    for t in teams:
        t_perf = perf[t['pulse_id']]
        defaults = {
            'position': t_perf[0],
            'played': t_perf[1],
            'win': t_perf[2],
            'draw': t_perf[3],
            'loss': t_perf[4],
            'gf': t_perf[5],
            'ga': t_perf[6],
            'gd': t_perf[7],
            'points': t_perf[8],
            'form': t['form'],
            'short_name': t['short_name'],
            'strength': t['strength'],
            'strength_overall_home': t['strength_overall_home'],
            'strength_overall_away': t['strength_overall_away'],
            'strength_attack_home': t['strength_attack_home'],
            'strength_attack_away': t['strength_attack_away'],
            'strength_defence_home': t['strength_defence_home'],
            'strength_defence_away': t['strength_defence_away']
        }

        team, created = Team.objects.update_or_create(
            id = t['id'],
            pulse_id=t['pulse_id'],
            name=t['name'],
            defaults=defaults
        )


def populate_positions(positions):
    """Create position table in database

    Args:
        positions (dict): Retrieved data from API
    """    
    for p in positions:
        pos = Position()
        pos.id = int(p['id'])
        pos.name = p['singular_name']
        pos.name_short = p['singular_name_short']
        pos.save()


def update_players(players):
    """Update/create players table in database

    Args:
        players (dict): Retrieved data from API
    """    
    for p in players:
        defaults={
            'chance_of_playing_next_round': p['chance_of_playing_next_round'],
            'chance_of_playing_this_round': p['chance_of_playing_this_round'],
            'cost_change_event': p['cost_change_event'],
            'cost_change_event_fall': p['cost_change_event_fall'],
            'cost_change_start': p['cost_change_start'],
            'cost_change_start_fall': p['cost_change_start_fall'],
            'dreamteam_count': p['dreamteam_count'],
            'position': Position.objects.get(id=p['element_type']),
            'ep_next': float(p['ep_next']),
            'ep_this': float(p['ep_this']) 
                if p['ep_this'] != None else 0,
            'event_points': p['event_points'],
            'form': p['form'],
            'in_dreamteam': p['in_dreamteam'],
            'news': p['news'],
            'news_added': p['news_added'],
            'now_cost': p['now_cost'] / 10,
            'points_per_game': p['points_per_game'],
            'selected_by_percent': p['selected_by_percent'],
            'transfers_in': p['transfers_in'],
            'transfers_in_event': p['transfers_in_event'],
            'transfers_out': p['transfers_out'],
            'transfers_out_event': p['transfers_out_event'],
            'special': p['special'],
            'team': Team.objects.get(id=p['team']),
            'total_points': p['total_points'],
            'value_form': float(p['value_form']),
            'value_season': float(p['value_season']),
            'minutes': p['minutes'],
            'goals_scored': p['goals_scored'],
            'assists': p['assists'],
            'clean_sheets': p['clean_sheets'],
            'goals_conceded': p['goals_conceded'],
            'own_goals': p['own_goals'],
            'penalties_saved': p['penalties_saved'],
            'penalties_missed': p['penalties_missed'],
            'yellow_cards': p['yellow_cards'],
            'red_cards': p['red_cards'],
            'saves': p['saves'],
            'bonus': p['bonus'],
            'bps': p['bps'] / 10,
            'influence': float(p['influence']),
            'creativity': float(p['creativity']),
            'threat': float(p['threat']),
            'ict_index': float(p['ict_index']),
            'influence_rank': p['influence_rank'],
            'influence_rank_type': p['influence_rank_type'],
            'creativity_rank': p['creativity_rank'],
            'creativity_rank_type': p['creativity_rank_type'],
            'threat_rank': p['threat_rank'],
            'threat_rank_type': p['threat_rank_type'],
            'ict_index_rank': p['ict_index_rank'],
            'ict_index_rank_type': p['ict_index_rank_type'],
            'corners_and_indirect_freekicks_order':
                p['corners_and_indirect_freekicks_order'],
            'corners_and_indirect_freekicks_text':
                p['corners_and_indirect_freekicks_text'],
            'direct_freekicks_order': p['direct_freekicks_order'],
            'direct_freekicks_text': p['direct_freekicks_text'],
            'penalties_order': p['penalties_order'],
            'penalties_text': p['penalties_text']    
        }

        player, created = Player.objects.update_or_create(
            id = p['id'],
            first_name = p['first_name'],
            second_name = p['second_name'],
            defaults=defaults
        )


def update_fixture(fixtures):
    """Update/create fixture table in database

    Args:
        fixtures (dict): Retrieved data from API
    """    
    for f in fixtures:
        try:
            updated_values = {
                'finished': f['finished'],
                'event': Event.objects.get(id=f['event']) \
                    if type(f['event'])== int else None,
                'kickoff_time': f['kickoff_time'],
                'team_h_difficulty': f['team_h_difficulty'],
                'team_a_difficulty': f['team_a_difficulty'],
                'team_h_score': str(f['team_h_score']) \
                    if f['finished'] == True else '-',
                'team_a_score': str(f['team_a_score']) \
                    if f['finished'] == True else '-'
            }

            fix, created = Fixtures.objects.update_or_create(
                id=f['id'],
                team_h=Team.objects.get(id=f['team_h']),
                team_a=Team.objects.get(id=f['team_a']),
                defaults=updated_values
            )
        except:
            pass


def update_events(events, total_players):
    """Update/create events table in database

    Args:
        events (dict): Retrieved data from API
        total_players (int): Total number of players
    """    
    for e in events:
        defaults={
            'deadline_time': e['deadline_time'],
            'average_entry_score': e['average_entry_score'],
            'finished': e['finished'],
            'data_checked': e['data_checked'],
            'highest_score': e['highest_score']
                             if type(e['highest_score']) == int else 0,
            'is_previous': e['is_previous'],
            'is_current': e['is_current'],
            'is_next': e['is_next'],
            'transfers_made': e['transfers_made'],
            'total_players': total_players,
            'top_element': Player.objects.get(id=e['top_element'])
                            if e['finished'] == True else None,
            'most_selected': Player.objects.get(id=e['most_selected'])
                            if e['finished'] == True else None,
            'most_transferred_in': Player.objects.get(
                                            id=e['most_transferred_in'])
                            if e['finished'] == True else None,
            'most_captained': Player.objects.get(id=e['most_captained'])
                            if e['finished'] == True else None,
            'most_vice_captained': Player.objects.get(
                                            id=e['most_vice_captained'])
                            if e['finished'] == True else None,
            }
        try:
            defaults['top_element_points'] = e['top_element_info']['points']
        except:
            defaults['top_element_points'] = 0

        event, created = Event.objects.update_or_create(
            id=e['id'],
            name=e['name'],
            defaults = defaults
        )


def update_userteam(user, players):
    """Create or update userteam for given GW and user based on data from
    FPL API

    Args:
        user (model_instance): currently logged in User
        players (dict): dictionary created from FPL API
        event (model_instance): instance of GW from Event model
    """    
    defaults = {}
    pos_d = {'gkp':1, 'def':1, 'mid':1 ,'fwd':1}
    for p in players:
        element = Player.objects.get(id=p['element'])
        pos = element.position.name_short.lower()
        num = pos_d[pos]
        key = f'{pos}{num}'
        elem = {
            f'{key}': element,
            f'{key}_pos': p['position'],
        }
        defaults.update(elem)
        pos_d[pos] += 1

    ust = UserTeam.objects.update_or_create(
        user=user,
        defaults=defaults
    )


def update_user(user, user_fpl, user_fpl_history, user_fpl_transfers):
    """Update/create user in database

    Args:
        user (model_instance): Currently logged user
        user_fpl (dict): Retrieved data from API
    """    
    chips = user_fpl_history['chips']
    past = user_fpl_history['past']

    defaults = {
        'joined_time': user_fpl['joined_time'],
        'fpl': user_fpl['id'], ## Comment to disable updating data for User FPL
        'started_event': user_fpl['started_event'],
        'favourite_team': user_fpl['favourite_team'],
        'player_first_name': user_fpl['player_first_name'],
        'player_last_name': user_fpl['player_last_name'],
        'player_region_name': user_fpl['player_region_name'],
        'player_region_iso_code_short': user_fpl['player_region_iso_code_short'],
        'player_region_iso_code_long': user_fpl['player_region_iso_code_long'],
        'summary_overall_points': user_fpl['summary_overall_points'],
        'summary_overall_rank': user_fpl['summary_overall_rank'],
        'summary_event_points': user_fpl['summary_event_points'],
        'summary_event_rank': user_fpl['summary_event_rank'],
        'current_event': user_fpl['current_event'],
        'name': user_fpl['name'],
        'last_deadline_bank': user_fpl['last_deadline_bank'] / 10,
        'last_deadline_value': user_fpl['last_deadline_value'] / 10,
        'last_deadline_total_transfers': user_fpl['last_deadline_total_transfers'],
        'chips': chips,
        'past': past,
        'transfers': user_fpl_transfers
    }

    usr, created = UserFpl.objects.update_or_create(
        user=user,
        # fpl=user_fpl['id'], ## Uncomment to disable updating data for User FPL
        defaults=defaults      
    )


def update_user_season(user, user_fpl_season):
    """Update/create UserSeason table in database

    Args:
        user (model_instance): Currently logged in user
        user_fpl_season (dict): Retrieved data from API
    """    
    user_fpl = UserFpl.objects.get(user=user)
    for season in user_fpl_season:
        defaults = {
            'points': season['points'],
            'total_points': season['total_points'],
            'rank': season['rank'],
            'rank_sort': season['rank_sort'],
            'overall_rank': season['overall_rank'],
            'bank': season['bank']/10,
            'value': season['value'] / 10,
            'money': season['bank']/10 + season['value']/10,
            'event_transfers': season['event_transfers'],
            'event_transfers_cost': season['event_transfers_cost'],
            'points_on_bench': season['points_on_bench']
        }
        obj, created = UserFplSeason.objects.update_or_create(
            userfpl=user_fpl,
            event=Event.objects.get(id=season['event']),
            defaults = defaults
        )


def update_user_picks(user):    
    """Update/create element(players) picks for every instance of userfplseason

    Args:
        userfplseason (model_instance): Instance of UserFplSeason
        picks (json): Retrieved data from API
    """  
    userfpl = UserFpl.objects.get(user=user)
    fpl_id = userfpl.fpl
    start = userfpl.started_event
    end = userfpl.current_event + 1
    userfplseason = UserFplSeason.objects.filter(userfpl=userfpl) 

    for i in range(start, end):
        try:
            data = get_fpl_user_picks(player_id=fpl_id, gw=i)
            ufs = userfplseason.get(event_id=i)
        except:
            continue
        picks = data['picks']
        defaults = {}
        key = 1
        for p in picks:
            element = Player.objects.get(id=p['element'])
            elem = {
                f'pck{key}': element,
                f'pck{key}_pos': p['position'],
                f'pck{key}_mult': p['multiplier'],
                f'pck{key}_cpt': p['is_captain'],
                f'pck{key}_vcpt': p['is_vice_captain']
            }
            defaults.update(elem)
            key += 1

        pick, created = UserFplPicks.objects.update_or_create(
            user=ufs,
            defaults=defaults
        )


def update_player_data(history):
    """Update/create PlayerData table in database

    Args:
        history (dict): Retrieved data from API
    """    
    for h in history:
        defaults = {
            'event': Fixtures.objects.get(id=h['fixture']).event,
            'position': Player.objects.get(id=h['element']).position_id,
            'opponent_team': Team.objects.get(id=h['opponent_team']),
            'team_h': Fixtures.objects.get(id=h['fixture']).team_h,
            'team_a': Fixtures.objects.get(id=h['fixture']).team_a,
            'total_points': h['total_points'],
            'is_home': h['was_home'],
            'kickoff_time': h['kickoff_time'],
            'team_h_score': h['team_h_score'],
            'team_a_score': h['team_a_score'],
            'finished': True,
            'minutes': h['minutes'],
            'goals_scored': h['goals_scored'],
            'assists': h['assists'],
            'clean_sheets': h['clean_sheets'],
            'goals_conceded': h['goals_conceded'],
            'own_goals': h['own_goals'],
            'penalties_saved': h['penalties_saved'],
            'penalties_missed': h['penalties_missed'],
            'yellow_cards': h['yellow_cards'],
            'red_cards': h['red_cards'],
            'saves': h['saves'],
            'bonus': h['bonus'],
            'bps': h['bps'],
            'influence': float(h['influence']),
            'creativity': float(h['creativity']),
            'threat': float(h['threat']),
            'ict_index': float(h['ict_index']),
            'value': h['value'] / 10,
            'selected': h['selected']
        }


        hist, created = PlayerHistory.objects.update_or_create(
            player = Player.objects.get(id=h['element']),
            fixture = Fixtures.objects.get(id=h['fixture']),
            defaults = defaults
        )
    

def update_player_fixture(game: dict, id: int):
    """Update/create PlayerFixture table in database

    Args:
        game (dict): Retrieved data from API
        id (int): ID of player
    """    
    for g in game:
        defaults = {
            'event': Fixtures.objects.get(id=g['id']).event,
            'team_h': Team.objects.get(id=g['team_h']),
            'team_h_score': g['team_h_score'],
            'team_a': Team.objects.get(id=g['team_a']),
            'team_a_score': g['team_a_score'],
            'finished': g['finished'],
            'minutes': g['minutes'],
            'kickoff_time': g['kickoff_time'],
            'is_home': g['is_home'],
            'difficulty': g['difficulty']
        }

        gam, created = PlayerHistory.objects.update_or_create(
            player=Player.objects.get(id=id),
            fixture=Fixtures.objects.get(id=g['id']),
            defaults=defaults
        )