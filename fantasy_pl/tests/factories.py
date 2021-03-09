import factory
from pytest_factoryboy import register

# from django.contrib.auth.models import User
from fantasy_pl.models import Team

class TeamFactory(factory.Factory):
    class Meta:
        model = Team

register(TeamFactory)


def test_factory_fixture(team_factory):
    team = team_factory(name='Chelsea')
    assert team.name == 'Chelsea'