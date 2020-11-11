import json
import time
import bs4 as bs
import urllib.request

import requests

from fantasy_pl.models import Team, Position, Player, PlayerHistory, Fixtures, \
    UserTeam, UserFpl, Event


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


# Team updates and populates
def populate_teams(teams):
    perf = league_table_scraper()
    for t in teams:
        team = Team()
        team.id = int(t['id'])
        data_to_team(team, t, perf)
        team.save()


def populate_positions(positions):
    for p in positions:
        pos = Position()
        pos.id = int(p['id'])
        pos.name = p['singular_name']
        pos.name_short = p['singular_name_short']
        pos.save()


def populate_players(players):
    for p in players:
        player = Player()
        player.id = p['id']
        data_to_player(player, p)
        player.save()


def populate_fixture(fixtures):
    for f in fixtures:
        fix = Fixtures()
        fix.id = f['id']
        data_to_fixture(fix, f)
        fix.save()


def populate_events(events, total_players):
    for e in events:
        event = Event()
        event.id = e['id']
        data_to_event(event, e, total_players)
        event.save()

def update_teams(teams):
    perf = league_table_scraper()
    for t in teams:
        team = Team.objects.get(id=t['id'])
        data_to_team(team, t, perf)
        team.save()


def update_players(players):
    for p in players:
        try:
            player = Player.objects.get(id=p['id'])
            data_to_player(player, p)
            player.save()
        except:
            player = Player()
            player.id = p['id']
            data_to_player(player, p)
            player.save()


def update_fixture(fixtures):
    for f in fixtures:
        if f['finished'] == False:
            pass
        else:
            try:
                fix = Fixtures.objects.get(id=f['id'])
                data_to_fixture(fix, f)
                fix.save()
            except:
                fix = Fixtures()
                fix.id = f['id']
                data_to_fixture(fix, f)
                fix.save()


def update_events(events, total_players):
    for e in events:
        event = Event.objects.get(id=e['id'])
        # data_to_event(event, e, total_players)
        event.save()


def update_userteam(user, player_list):
    try:
        usrtm = UserTeam.objects.get(user=user)
        data_to_userteam(usrtm, player_list)
        usrtm.save()
    except:
        usrtm = UserTeam()
        usrtm.user = user
        data_to_userteam(usrtm, player_list)
        usrtm.save()


def update_user(user, user_fpl):
    try:
        usr = UserFpl.objects.get(user=user)
        data_to_user(usr, user_fpl)
        usr.save()
    except:
        usr = UserFpl()
        usr.user = user
        data_to_user(usr, user_fpl)
        usr.save()


def get_player_data(history):
    for h in history:
        try:
            hist = PlayerHistory.objects.filter(player=Player.objects.get(id=h['element']))\
                                .filter(fixture=Fixtures.objects.get(id=h['fixture'])).first()
            data_to_player_data(hist, h)
            hist.save()
        except:
            hist = PlayerHistory()
            hist.player = Player.objects.get(id=h['element'])
            hist.fixture = Fixtures.objects.get(id=h['fixture'])
            data_to_player_data(hist, h)
            hist.save()


def get_player_fixture(game, id):
    for g in game:
        try:
            hist = PlayerHistory.objects.filter(player=Player.objects.get(id=id))\
                                    .filter(fixture=Fixtures.objects.get(id=g['id'])).first()
            data_to_player_fixture(hist, g)
            hist.save()
        except:
            hist = PlayerHistory()
            hist.player = Player.objects.get(id=id)
            hist.fixture = Fixtures.objects.get(id=g['id'])
            data_to_player_fixture(hist, g)
            hist.save()



### Functions for data assignment
def data_to_team(team, t, perf):
    team.pulse_id = t['pulse_id']
    t_perf = perf[team.pulse_id]
    team.position = t_perf[0]
    team.played = t_perf[1]
    team.win = t_perf[2]
    team.draw = t_perf[3]
    team.loss = t_perf[4]
    team.gf = t_perf[5]
    team.ga = t_perf[6]
    team.gd = t_perf[7]
    team.points = t_perf[8]
    team.form = t['form']
    team.name = t['name']
    team.short_name = t['short_name']
    team.strength = t['strength']
    team.strength_overall_home = t['strength_overall_home']
    team.strength_overall_away = t['strength_overall_away']
    team.strength_attack_home = t['strength_attack_home']
    team.strength_attack_away = t['strength_attack_away']
    team.strength_defence_home = t['strength_defence_home']
    team.strength_defence_away = t['strength_defence_away']


def data_to_player(player, p):
    player.chance_of_playing_next_round = p['chance_of_playing_next_round']
    player.chance_of_playing_this_round = p['chance_of_playing_this_round']
    player.code = p['code']
    player.cost_change_event = p['cost_change_event']
    player.cost_change_event_fall = p['cost_change_event_fall']
    player.cost_change_start = p['cost_change_start']
    player.cost_change_start_fall = p['cost_change_start_fall']
    player.dreamteam_count = p['dreamteam_count']
    player.position = Position.objects.get(id=p['element_type'])
    player.ep_next = float(p['ep_next'])
    player.ep_this = float(p['ep_this'])
    player.event_points = p['event_points']
    player.first_name = p['first_name']
    player.form = p['form']
    player.in_dreamteam = p['in_dreamteam']
    player.news = p['news']
    player.news_added = p['news_added']
    player.now_cost = p['now_cost'] / 10
    player.points_per_game = p['points_per_game']
    player.second_name = p['second_name']
    player.selected_by_percent = p['selected_by_percent']
    player.transfers_in = p['transfers_in']
    player.transfers_in_event = p['transfers_in_event']
    player.transfers_out = p['transfers_out']
    player.transfers_out_event = p['transfers_out_event']
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
    player.bps = p['bps'] / 10
    player.influence = float(p['influence'])
    player.creativity = float(p['creativity'])
    player.threat = float(p['threat'])
    player.ict_index = float(p['ict_index'])


def data_to_fixture(fix, f):
    fix.event = f['event']
    fix.finished = f['finished']
    fix.kickoff_time = f['kickoff_time']
    fix.team_h = Team.objects.get(id=f['team_h'])
    fix.team_a = Team.objects.get(id=f['team_a'])
    if f['finished'] == True:
        fix.team_h_score = str(f['team_h_score'])
        fix.team_a_score = str(f['team_a_score'])
    fix.team_h_difficulty = f['team_h_difficulty']
    fix.team_a_difficulty = f['team_a_difficulty']


def data_to_event(event, e, total_players):
    event.name = e['name']
    event.deadline_time = e['deadline_time']
    event.average_entry_score = e['average_entry_score']
    event.finished = e['finished']
    event.data_checked = e['data_checked']
    event.highest_score = e['highest_score']
    event.is_previous = e['is_previous']
    event.is_current = e['is_current']
    event.is_next = e['is_next']
    event.transfers_made = e['transfers_made']
    try:
        event.top_element_points = e['top_element_info']['points']
    except:
        event.top_element_points = 0
    if e['finished'] == True:
        event.top_element = Player.objects.get(id=e['top_element'])
        event.most_selected = Player.objects.get(id=e['most_selected'])
        event.most_transferred_in = Player.objects.get(id=e['most_transferred_in'])
        event.most_captained = Player.objects.get(id=e['most_captained'])
        event.most_vice_captained = Player.objects.get(id=e['most_vice_captained'])
    event.total_players = total_players


def data_to_player_data(hist, h):
    hist.event = Fixtures.objects.get(id=h['fixture']).event
    hist.position = hist.player.position_id
    hist.opponent_team = Team.objects.get(id=h['opponent_team'])
    hist.team_h = Fixtures.objects.get(id=h['fixture']).team_h
    hist.team_a = Fixtures.objects.get(id=h['fixture']).team_a
    hist.total_points = h['total_points']
    hist.is_home = h['was_home']
    hist.kickoff_time = h['kickoff_time']
    hist.team_h_score = h['team_h_score']
    hist.team_a_score = h['team_a_score']
    hist.finished = True
    hist.minutes = h['minutes']
    hist.goals_scored = h['goals_scored']
    hist.assists = h['assists']
    hist.clean_sheets = h['clean_sheets']
    hist.goals_conceded = h['goals_conceded']
    hist.own_goals = h['own_goals']
    hist.penalties_saved = h['penalties_saved']
    hist.penalties_missed = h['penalties_missed']
    hist.yellow_cards = h['yellow_cards']
    hist.red_cards = h['red_cards']
    hist.saves = h['saves']
    hist.bonus = h['bonus']
    hist.bps = h['bps']
    hist.influence = float(h['influence'])
    hist.creativity = float(h['creativity'])
    hist.threat = float(h['threat'])
    hist.ict_index = float(h['ict_index'])
    hist.value = h['value'] / 10
    hist.selected = h['selected']


def data_to_player_fixture(hist, g):
    hist.event = Fixtures.objects.get(id=g['id']).event
    hist.team_h = Team.objects.get(id=g['team_h'])
    hist.team_h_score = g['team_h_score']
    hist.team_a = Team.objects.get(id=g['team_a'])
    hist.team_a_score = g['team_a_score']
    hist.finished = g['finished']
    hist.minutes = g['minutes']
    hist.kickoff_time = g['kickoff_time']
    hist.is_home = g['is_home']
    hist.difficulty = g['difficulty']


def data_to_userteam(usrtm, player_list):
    usrtm.gkp = Player.objects.get(id=player_list[0])
    usrtm.def1 = Player.objects.get(id=player_list[1])
    usrtm.def2 = Player.objects.get(id=player_list[2])
    usrtm.def3 = Player.objects.get(id=player_list[3])
    usrtm.def4 = Player.objects.get(id=player_list[4])
    usrtm.mdf1 = Player.objects.get(id=player_list[5])
    usrtm.mdf2 = Player.objects.get(id=player_list[6])
    usrtm.mdf3 = Player.objects.get(id=player_list[7])
    usrtm.mdf4 = Player.objects.get(id=player_list[8])
    usrtm.fwd1 = Player.objects.get(id=player_list[9])
    usrtm.fwd2 = Player.objects.get(id=player_list[10])
    usrtm.gkpb = Player.objects.get(id=player_list[11])
    usrtm.defb = Player.objects.get(id=player_list[12])
    usrtm.mdfb = Player.objects.get(id=player_list[13])
    usrtm.fwdb = Player.objects.get(id=player_list[14])


def data_to_user(usr, user_fpl):
    usr.fpl = user_fpl['id']
    usr.joined_time = user_fpl['joined_time']
    usr.started_event = user_fpl['started_event']
    usr.favourite_team = user_fpl['favourite_team']
    usr.player_first_name = user_fpl['player_first_name']
    usr.player_last_name = user_fpl['player_last_name']
    usr.player_region_name = user_fpl['player_region_name']
    usr.player_region_iso_code_short = user_fpl['player_region_iso_code_short']
    usr.player_region_iso_code_long = user_fpl['player_region_iso_code_long']
    usr.summary_overall_points = user_fpl['summary_overall_points']
    usr.summary_overall_rank = user_fpl['summary_overall_rank']
    usr.summary_event_points = user_fpl['summary_event_points']
    usr.summary_event_rank = user_fpl['summary_event_rank']
    usr.current_event = user_fpl['current_event']
    usr.name = user_fpl['name']
    usr.last_deadline_bank = user_fpl['last_deadline_bank'] / 10
    usr.last_deadline_value = user_fpl['last_deadline_value'] / 10
    usr.last_deadline_total_transfers = user_fpl['last_deadline_total_transfers']


if __name__ == "__main__":
    download_json()