from rest_framework import serializers
from fantasy_pl.models import Team, Player


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.HyperlinkedRelatedField(
            queryset=Team.objects.all(),
            view_name='fpl:api_team_detail',
        )

    class Meta:
        model = Player
        fields = '__all__'
