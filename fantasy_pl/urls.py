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

    path('team/<int:id>/<str:sort>', TeamView.as_view(), name='team'),
    path('standings/', StandingsView.as_view(), name='standings'),
    path('player/<int:id>/', PlayerView.as_view(), name='player'),
    path('positions/<str:pos>/<str:sort>', PositionsView.as_view(), name='positions'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('search/', SearchView.as_view(), name='search'),
    # path('buttons/', ButtonsView.as_view(), name="buttons"),
    # path('flot/', FlotView.as_view(), name="flot"),
    # path('forms/', FormsView.as_view(), name="forms"),
    # path('grid/', GridView.as_view(), name="grid"),
    # path('icons/', IconsView.as_view(), name="icons"),
    # path('morris/', MorrisView.as_view(), name="morris"),
    # path('notifications/', NotificationsView.as_view(), name="notifications"),
    # path('panels/', PanelsView.as_view(), name="panels"),
    # path('tables/', TablesView.as_view(), name="tables"),
    # path('typography/', TypographyView.as_view(), name="typography"),

]



# 35mF)nKzX8Xw?dc