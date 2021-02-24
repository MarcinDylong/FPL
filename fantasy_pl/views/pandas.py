from django_pandas.io import read_frame

import pandas as pd

from fantasy_pl.models import Player

def gkp_dataframe():
    players = Player.objects.filter(position=1).filter(minutes__gt=0).order_by('now_cost')
    ## Create DataFrame for Goalkeepers
    gkp = read_frame(players, fieldnames=['first_name', 'second_name',
        'team', 'now_cost', 'points_per_game', 'total_points', 'minutes',
        'clean_sheets', 'goals_conceded', 'saves', 'penalties_saved',
        'yellow_cards', 'red_cards', 'dreamteam_count', 'form',
        'selected_by_percent', 'transfers_in', 'transfers_out'])
    # Merge first_name and second_name
    gkp['name'] = gkp['first_name'] + ' ' + gkp['second_name']
    gkp.drop(['first_name','second_name'], axis=1, inplace=True)
    ## Filter keepers with less than 30% times played
    max_minutes = 90 * 21 ## Change value 21 by numbers of GW later
    min_filter = gkp.minutes > max_minutes*0.3
    gkp = gkp[min_filter]
    # Change number of minutes to percent of time
    gkp.minutes = gkp.minutes.apply(lambda x: round(float(x)*100/max_minutes,2))
    return gkp