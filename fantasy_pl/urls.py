from django.urls import path

from .views import IndexView, LoginView, BlankView, LogoutView, PopulateTeamsView, UpdateTeamsView, PopulatePlayersView, \
                   UpdatePlayersView, PopulatePositionsView, TeamView, StandingsView, PlayerView, PositionsView, \
                   StatsView, SearchView

app_name = 'fantasy_pl'

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView, name='logout'),
    path('', IndexView.as_view(), name="index"),
    path('blank/', BlankView.as_view(), name="blank"),
    #  Data download & update
    path('populate_teams/', PopulateTeamsView.as_view(), name="populate_teams"),
    path('update_teams/', UpdateTeamsView.as_view(), name="update_teams"),
    path('populate_players/', PopulatePlayersView.as_view(), name="populate_players"),
    path('update_players/', UpdatePlayersView.as_view(), name="update_players"),
    path('populate_positions/', PopulatePositionsView.as_view(), name="positions_players"),
    #  Teams, players, stats
    path('team/<int:id>/<str:sort>', TeamView.as_view(), name='team'),
    path('standings/', StandingsView.as_view(), name='standings'),
    path('player/<int:id>/', PlayerView.as_view(), name='player'),
    path('positions/<str:pos>/<str:sort>', PositionsView.as_view(), name='positions'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('search/', SearchView.as_view(), name='search'),

]