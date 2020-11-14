import json
import time
import bs4 as bs
import urllib.request

import requests

from fantasy_pl.models import Team, Position, Player, PlayerHistory, Fixtures, \
    UserTeam, UserFpl, Event, UserFplHistory, UserFplSeason


def get_data():
    """ Retrieve the fpl player data from the hard-coded url
    """
    response = requests.get(
        "https://fantasy.premierleague.com/api/bootstrap-static/")
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_individual_player_data(player_id):
    """ Retrieve the player-specific detailed data
    Args:
        player_id (int): ID of the player whose data is to be retrieved
    """
    base_url = "https://fantasy.premierleague.com/api/element-summary/"
    full_url = base_url + str(player_id) + "/"
    response = ''
    while response == '':
        try:
            response = requests.get(full_url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    return data


def get_fixtures_for_season():
    """ Retrieve the fixtures for entire season """
    response = requests.get(
        'https://fantasy.premierleague.com/api/fixtures/'
    )
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user(player_id: int):
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user_history_and_season(player_id: int):
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/history/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_userteam(player_id: int, gw: int):
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/' \
               f'event/{gw}/picks/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def league_table_scraper():
    source_url = 'https://www.premierleague.com/tables'
    source = urllib.request.urlopen(source_url)
    soup = bs.BeautifulSoup(source, 'lxml')
    table = soup.find('tbody', class_='tableBodyContainer isPL')

    tr_name = table.find_all('a', attrs={'class': 'expandableTeam'})
    pulse_id = [a.get('href').split('/')[2] for a in tr_name]

    td_data = table.find_all('td')
    data = []
    for td in td_data:
        try:
            data.append(int(td.string))
        except:
            pass

    table = {int(pulse_id[i]): [i + 1] + data[8 * i: 8 * (i + 1)] for i in
             range(len(pulse_id))}

    return table


def download_json():
    data = get_data()
    with open('data.json', 'w') as outf:
        json.dump(data, outf)


def read_json():
    with open('data.json', 'r+') as f:
        read_data = json.load(f)
        data = read_data
        return data


def update_teams(teams):
    '''
        Create or update instances of Team
    '''
    perf = league_table_scraper()
    for t in teams:
        t_perf = perf[t['pulse_id']]
        team, created = Team.objects.update_or_create(
            id = t['id'],
            pulse_id = t['pulse_id'],
            position = t_perf[0],
            played = t_perf[1],
            win = t_perf[2],
            draw = t_perf[3],
            loss = t_perf[4],
            gf = t_perf[5],
            ga = t_perf[6],
            gd = t_perf[7],
            points = t_perf[8],
            form = t['form'],
            name = t['name'],
            short_name = t['short_name'],
            strength = t['strength'],
            strength_overall_home = t['strength_overall_home'],
            strength_overall_away = t['strength_overall_away'],
            strength_attack_home = t['strength_attack_home'],
            strength_attack_away = t['strength_attack_away'],
            strength_defence_home = t['strength_defence_home'],
            strength_defence_away = t['strength_defence_away']
        )


def populate_positions(positions):
    for p in positions:
        pos = Position()
        pos.id = int(p['id'])
        pos.name = p['singular_name']
        pos.name_short = p['singular_name_short']
        pos.save()


def update_players(players):
    for p in players:
        player, created = Player.objects.update_or_create(
            id = p['id'],
            first_name = p['first_name'],
            second_name = p['second_name'],
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
                'ep_this': float(p['ep_this']),
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
                'corners_and_indirect_freekicks_order': p['corners_and_indirect_freekicks_order'],
                'corners_and_indirect_freekicks_text': p['corners_and_indirect_freekicks_text'],
                'direct_freekicks_order': p['direct_freekicks_order'],
                'direct_freekicks_text': p['direct_freekicks_text'],
                'penalties_order': p['penalties_order'],
                'penalties_text': p['penalties_text']    
            }         
        )


def update_fixture(fixtures):
    for f in fixtures:
        fix_dict = {
            id: f['id'],
            event: f['event'],
            finished: f['finished'],
            kickoff_time: f['kickoff_time'],
            team_h: Team.objects.get(id=f['team_h']),
            team_a: Team.objects.get(id=f['team_a']),
            team_h_difficulty: f['team_h_difficulty'],
            team_a_difficulty: f['team_a_difficulty']
        }

        if f['finished'] == True:
                fix_dict[team_h_score] = str(f['team_h_score']),
                fix_dict[team_a_score] = str(f['team_a_score'])

        fix, created = Fixtures.objects.update_or_create(**fix_dict)


def update_events(events, total_players):
    for e in events:
        defaults={
                'deadline_time': e['deadline_time'],
                'average_entry_score': e['average_entry_score'],
                'finished': e['finished'],
                'data_checked': e['data_checked'],
                'highest_score': e['highest_score'],
                'is_previous': e['is_previous'],
                'is_current': e['is_current'],
                'is_next': e['is_next'],
                'transfers_made': e['transfers_made'],
                'total_players': total_players,
                'top_element': Player.objects.get(id=e['top_element']) if e['finished'] == True else None,
                'most_selected': Player.objects.get(id=e['most_selected']) if e['finished'] == True else None,
                'most_transferred_in': Player.objects.get(id=e['most_transferred_in']) if e['finished'] == True else None,
                'most_captained': Player.objects.get(id=e['most_captained']) if e['finished'] == True else None,
                'most_vice_captained': Player.objects.get(id=e['most_vice_captained']) if e['finished'] == True else None,
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


def update_userteam(user, player_list):
    ust = UserTeam.objects.update_or_create(
        user = user,
        gkp = Player.objects.get(id=player_list[0]),
        def1 = Player.objects.get(id=player_list[1]),
        def2 = Player.objects.get(id=player_list[2]),
        def3 = Player.objects.get(id=player_list[3]),
        def4 = Player.objects.get(id=player_list[4]),
        mdf1 = Player.objects.get(id=player_list[5]),
        mdf2 = Player.objects.get(id=player_list[6]),
        mdf3 = Player.objects.get(id=player_list[7]),
        mdf4 = Player.objects.get(id=player_list[8]),
        fwd1 = Player.objects.get(id=player_list[9]),
        fwd2 = Player.objects.get(id=player_list[10]),
        gkpb = Player.objects.get(id=player_list[11]),
        defb = Player.objects.get(id=player_list[12]),
        mdfb = Player.objects.get(id=player_list[13]),
        fwdb = Player.objects.get(id=player_list[14])
    )


def update_user(user, user_fpl):
    usr, created = UserFpl.objects.update_or_create(
        user=user,
        fpl = user_fpl['id'],
        joined_time = user_fpl['joined_time'],
        started_event = user_fpl['started_event'],
        favourite_team = user_fpl['favourite_team'],
        player_first_name = user_fpl['player_first_name'],
        player_last_name = user_fpl['player_last_name'],
        player_region_name = user_fpl['player_region_name'],
        player_region_iso_code_short = user_fpl['player_region_iso_code_short'],
        player_region_iso_code_long = user_fpl['player_region_iso_code_long'],
        summary_overall_points = user_fpl['summary_overall_points'],
        summary_overall_rank = user_fpl['summary_overall_rank'],
        summary_event_points = user_fpl['summary_event_points'],
        summary_event_rank = user_fpl['summary_event_rank'],
        current_event = user_fpl['current_event'],
        name = user_fpl['name'],
        last_deadline_bank = user_fpl['last_deadline_bank'] / 10,
        last_deadline_value = user_fpl['last_deadline_value'] / 10,
        last_deadline_total_transfers = user_fpl['last_deadline_total_transfers']       
    )


def update_user_history(user, user_fpl_history):
    user_fpl = UserFpl.objects.get(user=user)
    chips = user_fpl_history['chips']
    past = user_fpl_history['past']
    obj, created = UserFplHistory.objects.update_or_create(
        userfpl=user_fpl,
        chips=chips,
        past=past
    )


def update_user_season(user, user_fpl_season):
    user_fpl = UserFpl.objects.get(user=user)
    for season in user_fpl_season:
        obj, created = UserFplSeason.objects.update_or_create(
            userfpl=user_fpl,
            event=Event.objects.get(id=season['event']),
            points=season['points'],
            total_points=season['total_points'],
            rank=season['rank'],
            rank_sort=season['rank_sort'],
            overall_rank=season['overall_rank'],
            bank=season['bank']/10,
            value=season['value']/10,
            event_transfers=season['event_transfers'],
            event_transfers_cost=season['event_transfers_cost'],
            points_on_bench=season['points_on_bench']
        )


def get_player_data(history):
    for h in history:
        hist, created = PlayerHistory.objects.update_or_create(
            player = Player.objects.get(id=h['element']),
            fixture=Fixtures.objects.get(id=h['fixture']),
            event = Fixtures.objects.get(id=h['fixture']).event,
            position = hist.player.position_id,
            opponent_team = Team.objects.get(id=h['opponent_team']),
            team_h = Fixtures.objects.get(id=h['fixture']).team_h,
            team_a = Fixtures.objects.get(id=h['fixture']).team_a,
            total_points = h['total_points'],
            is_home = h['was_home'],
            kickoff_time = h['kickoff_time'],
            team_h_score = h['team_h_score'],
            team_a_score = h['team_a_score'],
            finished = True,
            minutes = h['minutes'],
            goals_scored = h['goals_scored'],
            assists = h['assists'],
            clean_sheets = h['clean_sheets'],
            goals_conceded = h['goals_conceded'],
            own_goals = h['own_goals'],
            penalties_saved = h['penalties_saved'],
            penalties_missed = h['penalties_missed'],
            yellow_cards = h['yellow_cards'],
            red_cards = h['red_cards'],
            saves = h['saves'],
            bonus = h['bonus'],
            bps = h['bps'],
            influence = float(h['influence']),
            creativity = float(h['creativity']),
            threat = float(h['threat']),
            ict_index = float(h['ict_index']),
            value = h['value'] / 10,
            selected = h['selected']
        )
    

def get_player_fixture(game, id):
    for g in game:
        gam, created = PlayerHistory.objects.update_or_create(
            player = Player.objects.get(id=id),
            fixture=Fixtures.objects.get(id=g['id']),
            event = Fixtures.objects.get(id=g['id']).event,
            team_h = Team.objects.get(id=g['team_h']),
            team_h_score = g['team_h_score'],
            team_a = Team.objects.get(id=g['team_a']),
            team_a_score = g['team_a_score'],
            finished = g['finished'],
            minutes = g['minutes'],
            kickoff_time = g['kickoff_time'],
            is_home = g['is_home'],
            difficulty = g['difficulty']
        )


if __name__ == "__main__":
    download_json()