import json
import time
import bs4 as bs
import urllib.request

import requests

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


def get_fpl_user_picks(player_id: int, gw: int):
    """Retrieve user team for given gameweek

    Args:
        player_id (int): User ID
        gw (int): Gameweek

    Raises:
        Exception: Status code different than 200

    Returns:
        dict: Dictionary with data about user team
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/event/{gw}/picks/'
    response = requests.get(base_url)

    if response.status_code != 200:
        raise Exception('Response was code ' + str(response.status_code))
    responseStr = response.text
    data = json.loads(responseStr)
    return data


def get_fpl_userteam(player_id: int, gw: int):
    """Retrieve user team for given gameweek

    Args:
        player_id (int): User ID
        gw (int): Gameweek

    Raises:
        Exception: Status code different than 200

    Returns:
        dict: Dictionary with data about user team
    """    
    base_url = f'https://fantasy.premierleague.com/api/entry/{player_id}/event/{gw}/picks/'
    response = requests.get(base_url)

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


def DownloadDataJSON():
    try:
        download_json()
        ctx = {'event': 'success', 'info': 'Data has been downloaded to JSON'}
        return ctx
    except Exception as e:
        ctx = {'event': 'error', 'error': format(e)}
        return ctx


if __name__ == "__main__":
    download_json()