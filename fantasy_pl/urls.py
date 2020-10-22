from django.urls import path

from .views.views_main import IndexView, LoginView, BlankView, LogoutView, \
     CreateUserView, ChangetPasswordView, SendMessageView, MessageReceivedView, \
     MessageSentView
from .views.views_display import TeamView, StandingsView, PlayerView, \
     StatsView, PlayersSearchView, FixtureView
from .views.views_api import ApiTeamsView, ApiTeamsListView, ApiPlayersListView, \
     ApiPlayersView, ApiUserTeamListView, ApiUserTeamView
from .views.views_data import PopulateTablesView, UpdateTablesView, \
     DownloadDataView, GetPlayersHistoryView, GetFixtureView, \
     DownloadUserteamView
from .views.views_userteam import UserTeamView

app_name = 'fantasy_pl'

urlpatterns = [
    ## User related
    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView, name='logout'),
    path('signin/', CreateUserView.as_view(), name='sign_in'),
    path('change_password/<int:user_id>', ChangetPasswordView.as_view(),
         name='change_password'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('received_message/', MessageReceivedView.as_view(),
         name='received_message'),
    path('sent_message/', MessageSentView.as_view(), name='sent_message'),
    path('user_team/', UserTeamView.as_view(), name='user_team'),
    path('download_userteam/', DownloadUserteamView, name="download_userteam"),
    path('blank/', BlankView.as_view(), name="blank"),
    ##  Data download & update
    path('download_data/', DownloadDataView.as_view(), name='download_data'),
    path('populate_tables/', PopulateTablesView.as_view(),
         name="populate_tables"),
    path('update_tables/', UpdateTablesView.as_view(), name="update_tables"),
    path('get_players_history/', GetPlayersHistoryView.as_view(),
         name="get_players_history"),
    path('get_fixture/', GetFixtureView.as_view(), name="get_fixture"),
    ##  Display data
    path('team/<int:id>/<str:sort>', TeamView.as_view(), name='team'),
    path('standings/', StandingsView.as_view(), name='standings'),
    path('fixture/', FixtureView.as_view(), name='fixture'),
    path('player/<int:id>/', PlayerView.as_view(), name='player'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('search/', PlayersSearchView.as_view(), name='search'),
    ## API
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