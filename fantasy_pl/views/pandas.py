from django_pandas.io import read_frame

import pandas as pd

from fantasy_pl.models import Player, Fixtures, Position

def players_ctx(pos, ctx, form, x_axis='points_per_game', y_axis='now_cost',
                  size='selected_by_percent', limit=20):
    position = Position.objects.get(id=pos)
    players = Player.objects.filter(position=position).filter(minutes__gt=0).order_by('now_cost')
    gw = Fixtures.objects.filter(finished=True).order_by('event_id').last().event_id
    ## Create DataFrame for Goalkeepers
    gkp = read_frame(players, fieldnames=['first_name', 'second_name',
        'team', 'points_per_game', 'total_points', 'now_cost', 'form', 
        'minutes', 'assists', 'goals_scored', 'own_goals', 'influence',
        'influence_rank', 'creativity', 'creativity_rank', 'threat',
        'threat_rank', 'clean_sheets', 'goals_conceded', 'saves', 
        'penalties_saved', 'yellow_cards', 'red_cards', 'dreamteam_count',
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
    ctx['title'] = f'Chart - {position.name}s'
    ctx['x'] = list(gkp[x_axis])
    ctx['y'] = list(gkp[y_axis])
    ctx['max_size'] = max(gkp[size]) if len(gkp[size]) > 0 else 0 
    ctx['size'] = list(((gkp[size]/ ctx['max_size']) + 1)  * 10)
    ctx['players'] = gkp['name'].tolist()
    ctx['form'] = form

    return ctx