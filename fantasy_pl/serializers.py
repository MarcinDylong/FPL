from rest_framework import serializers
from fantasy_pl.models import Team, Player, UserTeam


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    team = serializers.HyperlinkedRelatedField(
            queryset = Team.objects.all(),
            view_name = 'fpl:api_team_detail',
        )

    class Meta:
        model = Player
        fields = '__all__'


class UserTeamSerializer(serializers.ModelSerializer):
    gkp = serializers.HyperlinkedRelatedField(
        # read_only = True,
            queryset = Player.objects.all(),
            view_name = 'fpl:api_player_detail',
        )
    def1 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    def2 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    def3 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    def4 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    mdf1 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    mdf2 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    mdf3 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    mdf4 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    fwd1 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    fwd2 = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    gkpb = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    defb = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    mdfb = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )
    fwdb = serializers.HyperlinkedRelatedField(
        # read_only = True,
        queryset=Player.objects.all(),
        view_name='fpl:api_player_detail',
    )

    class Meta:
        model = UserTeam
        fields = '__all__'