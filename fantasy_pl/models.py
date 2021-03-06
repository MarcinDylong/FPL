from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    pulse_id = models.SmallIntegerField(null=True)
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=4)
    position = models.SmallIntegerField()
    played = models.SmallIntegerField()
    win = models.SmallIntegerField()
    draw = models.SmallIntegerField()
    loss = models.SmallIntegerField()
    gf = models.SmallIntegerField(null=True)
    ga = models.SmallIntegerField(null=True)
    gd = models.SmallIntegerField(null=True)
    points = models.SmallIntegerField()
    form = models.TextField(max_length=8, null=True)
    strength = models.SmallIntegerField()
    strength_overall_home = models.SmallIntegerField()
    strength_overall_away = models.SmallIntegerField()
    strength_attack_home = models.SmallIntegerField()
    strength_attack_away = models.SmallIntegerField()
    strength_defence_home = models.SmallIntegerField()
    strength_defence_away = models.SmallIntegerField()

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    name_short = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=32)
    second_name = models.CharField(max_length=32)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    # position = models.SmallIntegerField()
    news = models.TextField(max_length=256)
    news_added = models.DateTimeField(null=True)
    # Stats from BPL
    minutes = models.IntegerField()
    # minutes_pg = models.FloatField(null=True)
    goals_scored = models.IntegerField()
    assists = models.IntegerField()
    clean_sheets = models.IntegerField()
    goals_conceded = models.IntegerField()
    own_goals = models.IntegerField()
    penalties_saved = models.IntegerField()
    penalties_missed = models.IntegerField()
    yellow_cards = models.IntegerField()
    red_cards = models.IntegerField()
    saves = models.IntegerField()
    # Stats in game
    chance_of_playing_next_round = models.IntegerField(null=True)
    chance_of_playing_this_round = models.IntegerField(null=True)
    cost_change_event = models.IntegerField(null=True)
    cost_change_event_fall = models.IntegerField(null=True)
    cost_change_start = models.IntegerField(null=True)
    cost_change_start_fall = models.IntegerField(null=True)
    dreamteam_count = models.IntegerField()
    ep_next = models.FloatField()
    ep_this = models.FloatField()
    event_points = models.IntegerField()
    form = models.FloatField()
    in_dreamteam = models.BooleanField()
    now_cost = models.FloatField()
    points_per_game = models.FloatField()
    selected_by_percent = models.FloatField(null=True)
    special = models.BooleanField(null=True)
    total_points = models.IntegerField(null=True)
    value_form = models.FloatField()
    value_season = models.FloatField()
    bonus = models.IntegerField()
    bps = models.IntegerField()
    influence = models.FloatField()
    creativity = models.FloatField()
    threat = models.FloatField()
    ict_index = models.FloatField()

    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

    def form_str(self):
        return f'{self.first_name} {self.second_name} - {self.now_cost} Ł'

    def ratio(self):
        if self.now_cost != 0:
            return round(self.points_per_game/self.now_cost,2)
        else:
            return 0


class UserTeam(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    gkp = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='gkp')
    def1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def1')
    def2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def2')
    def3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def3')
    def4 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def4')
    mdf1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mdf1')
    mdf2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mdf2')
    mdf3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mdf3')
    mdf4 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mdf4')
    fwd1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwd1')
    fwd2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwd2')
    gkpb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='gkpb')
    defb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='defb')
    mdfb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mfdb')
    fwdb = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwdb')
    overall_cost = models.FloatField(default=0)
    ppg = models.FloatField(default=0)
    influence = models.FloatField(default=0)
    creativity = models.FloatField(default=0)
    threat = models.FloatField(default=0)
    total_points = models.SmallIntegerField(default=0)
    dt_apps = models.FloatField(default=0)
    novelty = models.FloatField(default=0)


class Fixtures(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.IntegerField(null=True)
    finished = models.BooleanField()
    kickoff_time = models.DateTimeField(null=True)
    team_h = models.ForeignKey(Team, null=True, on_delete=models.CASCADE,
                               related_name='f_home_team')
    team_h_score = models.CharField(max_length=4, default='-')
    team_a = models.ForeignKey(Team, null=True, on_delete=models.CASCADE,
                               related_name='f_away_team')
    team_a_score = models.CharField(max_length=4, default='-')
    team_h_difficulty = models.IntegerField()
    team_a_difficulty = models.IntegerField()

    def __str__(self):
        return f'{self.team_h} - {self.team_a}, {self.kickoff_time}'


class PlayerHistory(models.Model):
    player = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL)
    position = models.SmallIntegerField(null=True)
    fixture = models.ForeignKey(Fixtures, null=True, on_delete=models.SET_NULL)
    round = models.SmallIntegerField()
    kickoff_time = models.DateTimeField(null=True)
    difficulty = models.SmallIntegerField(null=True)
    team_h = models.ForeignKey(Team, null=True,
                               on_delete=models.SET_NULL,
                               related_name='p_home_team')
    team_h_score = models.SmallIntegerField(null=True)
    team_a = models.ForeignKey(Team, null=True,
                               on_delete=models.SET_NULL,
                               related_name='p_away_team')
    team_a_score = models.SmallIntegerField(null=True)
    is_home = models.BooleanField()
    opponent_team = models.ForeignKey(Team, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='opp_team')
    finished = models.BooleanField()
    minutes = models.SmallIntegerField()
    total_points = models.SmallIntegerField(null=True)
    goals_scored = models.SmallIntegerField(null=True)
    assists = models.SmallIntegerField(null=True)
    clean_sheets = models.SmallIntegerField(null=True)
    goals_conceded = models.SmallIntegerField(null=True)
    own_goals = models.SmallIntegerField(null=True)
    penalties_saved = models.SmallIntegerField(null=True)
    penalties_missed = models.SmallIntegerField(null=True)
    yellow_cards = models.SmallIntegerField(null=True)
    red_cards = models.SmallIntegerField(null=True)
    saves = models.SmallIntegerField(null=True)
    bonus = models.SmallIntegerField(null=True)
    bps = models.SmallIntegerField(null=True)
    influence = models.FloatField(null=True)
    creativity = models.FloatField(null=True)
    threat = models.FloatField(null=True)
    ict_index = models.FloatField(null=True)
    value = models.FloatField(null=True)
    selected = models.IntegerField(null=True)

    class Meta:
        unique_together = ('fixture','player',)

    def __str__(self):
        if self.is_home:
            text = f'{self.team_h} - ({self.team_a})'
        else:
            text = f'({self.team_h}) - {self.team_a}'
        return text

    def diff_rest(self):
        return 5 - self.difficulty

