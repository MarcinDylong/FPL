import json
import time
import bs4 as bs
import urllib.request
import re
import requests

from typing import List, Tuple, Dict

'''
    Functions for retrieving data from Fantasy Premier League API
'''


def get_data():
    """Retrieve the fpl player data from the hard-coded url

    Raises:
        Exception: Status_code different than 200

    Returns:
        dict: Data converted from JSON to dictionary
    """
    response = requests.get(
        "https://fantasy.premierleague.com/api/bootstrap-static/")
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_individual_player_data(player_id):    
    """Retrieve the player-specific detailed data

    Args:
        player_id (int): Player ID

    Raises:
        Exception: Status code different than 200

    Returns:
        dict= Dictionary with individual player data
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
    """ Retrieve the fixtures for entire season 
    """
    response = requests.get(
        'https://fantasy.premierleague.com/api/fixtures/'
    )
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user(player_id: int):
    """Retrieve User data from FPL API

    Args:
        player_id (int): ID of User

    Raises:
        Exception: Status code different than 200

    Returns:
        dict: Dictionary with data about User from FPL
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user_history_and_season(player_id: int):
    """Retrieve Player season data

    Args:
        player_id (int): Player ID

    Raises:
        Exception: Status different than 200

    Returns:
        dict: Dictionary with season data of player
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/history/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user_transfers(player_id: int):
    """Retrieve Player season data

    Args:
        player_id (int): Player ID

    Raises:
        Exception: Status different than 200

    Returns:
        dict: Dictionary with season data of player
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/transfers/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_user_picks(player_id: int, gameweek_id: int):
    """Retrieve user team for given gameweek

    Args:
        player_id (int): User ID
        gw (int): Gameweek

    Raises:
        Exception: Status code different than 200

    Returns:
        dict: Dictionary with data about user team
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/event/{gameweek_id}/picks/'
    response = requests.get(base_url)
    print(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def league_table_scraper():
    """Table scrapper for BPL standings

    Returns:
        dict: Dictionary with data for BPL standings 
    """    
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


def team_name_scrapper(season: str='2021') -> List[str]:
    """ Import names of teams used in understat.com

    Args:
        season (str, optional): Year of season start. Defaults to '2021'.

    Returns:
        List[str]: Names of teams
    """

    teams = []
    
    ## Request url
    source_url = f'https://understat.com/league/EPL/2021'
    source = urllib.request.urlopen(source_url)
    soup = bs.BeautifulSoup(source, 'lxml')

    ## Extract data from URL
    table = soup.find_all('script')[2]
    table_content = table.contents
    table_split = table_content[0].split('=')
    table_json = re.findall(r'JSON\.parse\(\'(.*)\'\)',table_split[1])
    decoded_table = codecs.escape_decode(table_json[0], 'hex')[0].decode('utf-8')
    table_data = json.loads(decoded_table)
    
    ## Append team names to list
    for key in table_data.keys():
        teams.append(table_data[key]['title'])

    return teams


def team_understat_scrapper(team:str) -> Tuple[List[Dict], Dict]:
    """Scrap understats for given team and players from that team


    Args:
        team (str): team name

    Returns:
        Tuple[List[Dict], Dict]: List of dictionaries with understats for all 
            EPL players and dictionary with understats for all EPL Teams.
    """
    
    ## Request url for team
    source_url = f'https://understat.com/team/{team}/2021'
    source = urllib.request.urlopen(source_url)
    soup = bs.BeautifulSoup(source, 'lxml')

    ## Extract scripts with data for team
    scripts = soup.find_all('script')

    '''
        Scripts content:
        [1] - Team calendar
        [2] - Team stats
        [3] - Individual players stats
    '''

    ## Extract JSON for individual players data
    players_script = scripts[3]
    players_script_content = players_script.contents
    split_players = players_script_content[0].split('=')
    players_content_type = split_players[0].strip()
    players_content = re.findall(r'JSON\.parse\(\'(.*)\'\)',split_players[1])
    decoded_players_content = codecs.escape_decode(players_content[0], 'hex')[0].decode('utf-8')
    players_data = json.loads(decoded_players_content)

    ## Extract JSON with team data
    team_script = scripts[2]
    team_script_content = team_script.contents
    split_team = team_script_content[0].split('=')
    team_content_type = split_team[0].strip()
    team_content = re.findall(r'JSON\.parse\(\'(.*)\'\)',split_team[1])
    decoded_team_content = codecs.escape_decode(team_content[0], 'hex')[0].decode('utf-8')
    team_data = json.loads(decoded_team_content)
    
    return players_data, team_data


def create_players_understat_list() -> List:
    team_names = team_name_scrapper()
    all_players = list()
    for team in team_names:
        team_name = '_'.join(team.split(' '))
        players, team = team_understat_scrapper(team_name)
        all_players.extend(players)
        
    return all_players


def download_json():
    """Function for downloading JSON from API
    """    
    data = get_data()
    with open('data.json', 'w') as outf:
        json.dump(data, outf)


def read_json():
    """Read JSON safe in repository

    Returns:
        dict: Data converted from JSON to dictionary
    """    
    with open('data.json', 'r+') as f:
        read_data = json.load(f)
        data = read_data
        return data


def download_data_json():
    try:
        download_json()
        ctx = {'event': 'success', 'info': 'Data has been downloaded to JSON'}
        return ctx
    except Exception as e:
        ctx = {'event': 'error', 'error': format(e)}
        return ctx


if __name__ == "__main__":
    download_json()