import json
import time

import requests
from .models import Team, Position, Player, PlayerHistory


def get_data():
    """ Retrieve the fpl player data from the hard-coded url
    """
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
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


def download_json():
    data = get_data()
    with open('data.json', 'w') as outf:
        json.dump(data, outf)


def read_json():
    with open('fantasy_pl/data.json', 'r+') as f:
        read_data = json.load(f)
        data = read_data
        return data


# Team updates and populates
def populate_teams(teams):
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


def update_teams(teams):
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


## Positions populate
def populate_positions(positions):
    for p in positions:
        pos = Position()
        pos.id = int(p['id'])
        pos.name = p['singular_name']
        pos.name_short = p['singular_name_short']
        pos.save()

## Players updates and populates
def populate_players(players):
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
        player.position = Position.objects.get(id=p['element_type'])
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


def update_players(players):

    for p in players:
        player = Player.objects.get(id=p['id'])
        player.chance_of_playing_next_round = p['chance_of_playing_next_round']
        player.chance_of_playing_this_round = p['chance_of_playing_this_round']
        player.cost_change_event = p['cost_change_event']
        player.cost_change_event_fall = p['cost_change_event_fall']
        player.cost_change_start = p['cost_change_start']
        player.cost_change_start_fall = p['cost_change_start_fall']
        player.dreamteam_count = p['dreamteam_count']
        player.position = Position.objects.get(id=p['element_type'])
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


def get_player_data(history):
    for h in history:
        if PlayerHistory.objects.filter(player=Player.objects.get(id=h['element'])).filter(
                fixture=h['fixture']):
            pass
        else:
            hist = PlayerHistory()
            hist.player = Player.objects.get(id=h['element'])
            hist.fixture = h['fixture']
            hist.opponent_team = Team.objects.get(id=h['opponent_team'])
            hist.total_points = h['total_points']
            hist.was_home = h['was_home']
            hist.kickoff_time = h['kickoff_time']
            hist.team_h_score = h['team_h_score']
            hist.team_a_score = h['team_a_score']
            hist.round = h['round']
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
            hist.value = h['value']
            hist.transfers_balance = h['transfers_balance']
            hist.selected = h['selected']
            hist.transfers_in = h['transfers_in']
            hist.transfers_out = h['transfers_out']
            hist.save()


if __name__=="__main__":
    download_json()