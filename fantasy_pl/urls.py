from django.urls import path

from .views.views_display_data import IndexView, TeamView, PlayerView, \
     StandingsView, FixtureView, StatsView, PlayersSearchView, UserTeamView, \
     UserProfile, BlankView, StatsChartView, UserProfileTrans
from .views.views_download_data import GetPlayersHistoryView, GetFixtureView, \
     DownloadUserteamView, GetDataView, DownloadUserView, GetAllDataView
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
    path('stats_chart/<int:id>', StatsChartView.as_view(), name='stats-chart'),
    path('player-search/', PlayersSearchView.as_view(), name='player-search'),
    path('user-team/', UserTeamView.as_view(), name='user-team'),
    path('user-profile/', UserProfile.as_view(), name='user-profile'),
    path('user-profile/transfers/', UserProfileTrans.as_view(),
         name='user-profile-transfers'),
    ### Data download views
    path('get_all', GetAllDataView.as_view(), name='get_all'),
    path('get_data/', GetDataView.as_view(), name='get_data'),
    path('get_players_history/', GetPlayersHistoryView.as_view(),
         name="get_players_history"),
    path('get_fixture/', GetFixtureView.as_view(), name="get_fixture"),
    path('download_userteam', DownloadUserteamView,
         name='download_userteam'),
    path('download_user', DownloadUserView, name='download_user'),
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
