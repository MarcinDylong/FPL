from django_pandas.io import read_frame

import pandas as pd

from fantasy_pl.models import Player, Fixtures

def gkp_ctx(ctx, form, x_axis='now_cost', y_axis='total_points',
                  size='dreamteam_count', limit=20):
    players = Player.objects.filter(position=1).filter(minutes__gt=0).order_by('now_cost')
    gw = Fixtures.objects.filter(finished=True).order_by('event_id').last().event_id
    ## Create DataFrame for Goalkeepers
    gkp = read_frame(players, fieldnames=['first_name', 'second_name',
        'team', 'now_cost', 'points_per_game', 'total_points', 'minutes',
        'clean_sheets', 'goals_conceded', 'saves', 'penalties_saved',
        'yellow_cards', 'red_cards', 'dreamteam_count', 'form',
        'selected_by_percent', 'transfers_in', 'transfers_out'])
    # Merge first_name and second_name
    gkp['name'] = gkp['first_name'] + ' ' + gkp['second_name']
    gkp.drop(['first_name','second_name'], axis=1, inplace=True)
    # Change number of minutes to percent of time
    max_minutes = 90 * gw
    gkp.minutes = gkp.minutes.apply(lambda x: round(float(x) * 100 / max_minutes, 2))
    # Filter
    min_filter = gkp.minutes > limit
    gkp = gkp[min_filter]
    # Add data to ctx dictionary
    ctx['x'] = list(gkp[x_axis])
    ctx['y'] = list(gkp[y_axis])
    ctx['max_size'] = max(gkp[size]) if len(gkp[size]) > 0 else 0 
    ctx['size'] = list(((gkp[size]/ ctx['max_size']) + 1)  * 10)
    ctx['players'] = gkp['name'].tolist()
    ctx['form'] = form

    return ctx