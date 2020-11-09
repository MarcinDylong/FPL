import pytest
from fantasy_pl.models import Team, Player, Fixtures, Position, PlayerHistory


@pytest.mark.django_db
def test_team_model():
    team = Team.objects.create(
        id = 21,
        pulse_id= 20,
        name = 'Test_team',
        short_name = 'Tst',
        position = 21,
        played = 0,
        win = 0,
        draw = 0,
        loss = 0,
        points = 0,
        strength = 0,
        strength_overall_home = 0,
        strength_overall_away = 0,
        strength_attack_home = 0,
        strength_attack_away = 0,
        strength_defence_home = 0,
        strength_defence_away = 0,
    )
    assert team.short_name == 'Tst'
    assert team.name =='Test_team'
    assert team.id == 21
    assert str(team) == 'Test_team'


@pytest.mark.django_db
def test_position_model():
    position = Position.objects.create(
        id = 5,
        name= 'Test',
        name_short= 'Tst'
    )

    assert position.name == 'Test'
    assert str(position) == 'Test'


@pytest.mark.django_db
def test_player_model():
    player = Player.objects.create(
        id=20000,
        first_name = 'Test_name',
        second_name = 'Test_surname',
        team = Team.objects.get(id=1),
        position = Position.objects.get(id=1),
        news = '',
        minutes = 0,
        goals_scored = 0,
        assists = 0,
        clean_sheets = 0,
        goals_conceded = 0,
        own_goals = 0,
        penalties_saved = 0,
        penalties_missed = 0,
        yellow_cards = 0,
        red_cards = 0,
        saves = 0,
        cost_change_event = 0,
        cost_change_event_fall = 0,
        cost_change_start = 0,
        cost_change_start_fall = 0,
        dreamteam_count = 0,
        ep_next = 0,
        ep_this = 0,
        event_points = 0,
        form = 0,
        in_dreamteam = False,
        now_cost = 0,
        points_per_game = 0,
        selected_by_percent = 0,
        value_form = 0,
        value_season = 0,
        bonus = 0,
        bps = 0,
        influence = 0,
        creativity = 0,
        threat = 0,
        ict_index = 0,
    )

    assert player.first_name == 'Test_name'
    assert player.second_name ==  'Test_surname'
    assert str(player) == 'Test_name Test_surname'
    assert player.id == 20000
    assert Player.form_str(player) == 'Test_name Test_surname - 0 Ł'
    assert Player.ratio(player) == 0


@pytest.mark.django_db
def test_fixtures_model():
    fixture = Fixtures.objects.create(
        id= 381,
        event = 39,
        finished = False,
        kickoff_time = '2020-12-31 00:00:00.000000',
        team_h = Team.objects.get(id=1),
        team_h_score = 0,
        team_a = Team.objects.get(id=2),
        team_a_score = 0,
        team_h_difficulty = 2,
        team_a_difficulty = 4,
    )

    assert fixture.id == 381
    assert fixture.event == 39
    assert fixture.finished == False
    assert str(fixture) == 'Arsenal - Aston Villa, 2020-12-31 00:00:00.000000'


@pytest.mark.django_db
def test_playerhistory_model():
    playerhistory = PlayerHistory.objects.create(
        player= Player.objects.get(id=1),
        position = 2,
        fixture = Fixtures.objects.get(id=1),
        round = 1,
        kickoff_time = '2020-12-31 00:00:00.000000',
        difficulty = 3,
        team_h = Team.objects.get(id=1),
        team_h_score = 0,
        team_a = Team.objects.get(id=2),
        team_a_score = 0,
        is_home = True,
        opponent_team = Team.objects.get(id=2),
        finished = False,
        minutes = 0,
    )

    assert str(playerhistory) == 'Arsenal - (Aston Villa)'
    assert PlayerHistory.diff_rest(playerhistory) == 2