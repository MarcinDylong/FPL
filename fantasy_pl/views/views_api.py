from rest_framework import generics

from fantasy_pl.serializers import TeamSerializer, PlayerSerializer, \
    UserTeamSerializer
from fantasy_pl.models import Team, Player, UserTeam


class ApiUserTeamListView(generics.ListCreateAPIView):
    queryset = UserTeam.objects.all().order_by('id')
    serializer_class = UserTeamSerializer
    lookup_url_kwarg = 'format=JSON'


class ApiUserTeamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserTeam.objects.all()
    serializer_class = UserTeamSerializer


class ApiTeamsListView(generics.ListCreateAPIView):
    queryset = Team.objects.all().order_by('id')
    serializer_class = TeamSerializer


class ApiTeamsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class ApiPlayersListView(generics.ListCreateAPIView):
    queryset = Player.objects.all().order_by('id')
    serializer_class = PlayerSerializer


class ApiPlayersView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
