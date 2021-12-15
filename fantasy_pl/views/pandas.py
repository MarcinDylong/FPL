from django_pandas.io import read_frame

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

from fantasy_pl.models import Player, Fixtures, Position, PlayerHistory, Team

pd.options.mode.chained_assignment = None

def linear_regr(x, y):
    """
        Create linear regression for provided data, return two list which can be 
        visualize in chart.
    """
    regr = LinearRegression()

    X = np.array(x).reshape(-1, 1)
    Y = np.array(y)

    regr.fit(X, Y)
    
    point_pred = regr.predict(X)

    return list(X.flatten()), list(point_pred)


def poly_regr(x, y):
    """
        Create polynomial regression for provided data, return two list which can be 
        visualize in chart.
    """
    regr_poly = LinearRegression()

    X = np.array(x).reshape(-1, 1)
    Y = np.array(y)
    
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X)

    
    regr_poly.fit(X_poly, Y)

    point_pred = regr_poly.predict(X_poly)

    return list(X.flatten()), list(point_pred)


def players_ctx(pos, ctx, form, x_axis='points_per_game', y_axis='now_cost',
                  size='selected_by_percent', limit=50):
    """
        Create dictonary with data for players performance chart 
    """
    position = Position.objects.get(id=pos)
    players = Player.objects.filter(position=position).filter(minutes__gt=0) \
        .order_by('-'+x_axis)
    gameweek_id = Fixtures.objects.filter(finished=True).order_by('event_id') \
        .last().event_id
    ## Create DataFrame for Goalkeepers
    player_df = read_frame(players, fieldnames=['first_name', 
        'second_name', 'team', 'points_per_game', 'total_points', 'now_cost', 
        'form', 'minutes', 'assists', 'goals_scored', 'own_goals', 'influence',
        'influence_rank', 'creativity', 'creativity_rank', 'threat',
        'threat_rank', 'clean_sheets', 'goals_conceded', 'saves', 
        'penalties_saved', 'yellow_cards', 'red_cards', 'dreamteam_count',
        'selected_by_percent', 'transfers_in', 'transfers_out'])
    # Merge first_name and second_name
    player_df['name'] = player_df['first_name'] + ' ' + player_df['second_name']
    player_df.drop(['first_name','second_name'], axis=1, inplace=True)
    # Change number of minutes to percent of time
    max_minutes = 90 * gameweek_id
    player_df.minutes = player_df.minutes.apply(
        lambda x: round(float(x) * 100 / max_minutes, 2)
        )
    # Filter
    min_filter = player_df.minutes >= limit
    player_df = player_df[min_filter]
    # Add data to ctx dictionary
    ctx['title'] = f'Chart - {position.name}s'
    ctx['x'] = list(player_df[x_axis])
    ctx['y'] = list(player_df[y_axis])
    ctx['max_size'] = max(player_df[size]) if len(player_df[size]) > 0 else 0 
    ctx['size'] = list(((player_df[size]/ ctx['max_size']) + 1)  * 10)
    ctx['players'] = player_df['name'].tolist()
    ctx['form'] = form
    x_regr, pred_regr = linear_regr(player_df[x_axis], player_df[y_axis])
    ctx['x_regr'] = x_regr
    ctx['pred_regr'] = pred_regr
    x_regr_poly, pred_regr_poly = poly_regr(player_df[x_axis], player_df[y_axis])
    ctx['x_regr_poly'] = x_regr_poly
    ctx['pred_regr_poly'] = pred_regr_poly

    return ctx


def player_gwByGw(playerhistory, category='selected'):
    """
        Create list of overall performance made by player for chart in 
        player.html .

    Args:
        playerhistory (DjangoORM): Djano querysets with performance of player 
            gameweek by gameweek
        category (str, optional): Category of data chosen by user. Defaults to 
            'selected'.

    Returns:
        [list]: List of data for chosen category showing changes in overall 
            value for this category. 
    """    
    player_history_raw = read_frame(playerhistory)
    player_history_raw = player_history_raw[::-1]
    team_raw = read_frame(Team.objects.all())

    ## Create team dict
    team = team_raw[['name', 'short_name']]
    team_list = team.values.tolist()
    team_dict = {k:v for k,v in team_list}

    if category == 'selected':
        player_history = player_history_raw[['opponent_team', category]]
        ## Create column day_by_day
        player_history['category_changes'] = player_history[category].diff()
        try:
            start = player_history.iloc[0][1]
            player_history.fillna(value=start, inplace=True)
        except IndexError:
            None
    else:
        player_history = player_history_raw[['opponent_team', category]]
        ## Create column day_by_day
        player_history['category_changes'] = player_history[category].cumsum()
        # print(ph)
        start = player_history.iloc[0][1]
        player_history.fillna(value=start, inplace=True)
        player_history = player_history[
            ['opponent_team','category_changes',category]
            ]

    player_history['opponent_team'].replace(team_dict, inplace=True)

    return player_history.values.tolist()
