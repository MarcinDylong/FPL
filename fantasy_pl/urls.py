from django.urls import path, re_path

from .views.views import IndexView, TeamView, PlayerView, StandingsView, \
    FixtureView, StatsView, PlayersSearchView, UserTeamView
from .views.views_data import PopulateTablesView, UpdateTablesView, \
    DownloadDataView, GetPlayersHistoryView, GetFixtureView, \
    DownloadUserteamView
from .views.views_api import ApiTeamsView, ApiTeamsListView, \
    ApiPlayersListView, ApiPlayersView, ApiUserTeamListView, ApiUserTeamView

app_name = 'fantasy_pl'

urlpatterns = [
    # re_path(r'^.*\.html', views.pages, name='pages'),

    path('', IndexView.as_view(), name='home'),
    path('team/<int:id>', TeamView.as_view(), name='team'),
    path('player/<int:id>', PlayerView.as_view(), name='player'),
    path('standings/', StandingsView.as_view(), name='standings'),
    path('fixtures/', FixtureView.as_view(), name='fixtures'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('player-search/', PlayersSearchView.as_view(), name='player-search'),
    path('user-team/', UserTeamView.as_view(), name='user-team'),
    ### Data download views
    path('download_data/', DownloadDataView.as_view(), name='download_json'),
    path('populate_table/', PopulateTablesView.as_view(),
         name='populate_tables'),
    path('update_table/', UpdateTablesView.as_view(), name='update_tables'),
    path('get_players_history/', GetPlayersHistoryView.as_view(),
         name="get_players_history"),
    path('get_fixture/', GetFixtureView.as_view(), name="get_fixture"),
    path('download_userteam', DownloadUserteamView,
         name='download_userteam'),
    ### API
    path('api/teams', ApiTeamsListView.as_view(), name='api_teams'),
    path('api/teams/<int:pk>', ApiTeamsView.as_view(), name='api_team_detail'),
    path('api/players', ApiPlayersListView.as_view(), name='api_players'),
    path('api/players/<int:pk>', ApiPlayersView.as_view(),
         name='api_player_detail'),
    path('api/userteam', ApiUserTeamListView.as_view(),
         name='api_user_teams'),
    path('api/userteam/<int:pk>', ApiUserTeamView.as_view(),
         name='api_userteam'),
]

# from .views.views_userteam import UserTeamView

# urlpatterns = [
#
#     path('download_userteam/', DownloadUserteamView, name="download_userteam"),
#     ## API

# ]
