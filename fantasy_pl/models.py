from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=4)
    position = models.SmallIntegerField()
    played = models.SmallIntegerField()
    win = models.SmallIntegerField()
    draw = models.SmallIntegerField()
    loss = models.SmallIntegerField()
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
    cost_change_event = models.IntegerField()
    cost_change_event_fall = models.IntegerField()
    cost_change_start = models.IntegerField()
    cost_change_start_fall = models.IntegerField
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

    def ratio(self):
        if self.now_cost != 0:
            return round(self.points_per_game/self.now_cost,2)
        else:
            return 0

class Message(models.Model):
    subject = models.CharField(max_length=64, null=False)
    content = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    date_sent = models.DateTimeField(auto_now_add=True)


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
    cost = models.FloatField(default=0)
    points_per_game = models.FloatField(default=0)
    influence = models.FloatField(default=0)
    creativity = models.FloatField(default=0)
    threat = models.FloatField(default=0)
    total_points = models.SmallIntegerField(default=0)
    dt_apps = models.FloatField(default=0)
    novelty = models.FloatField(default=0)


class PlayerHistory(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    fixture = models.SmallIntegerField()
    kickoff_time = models.DateTimeField()
    was_home = models.BooleanField()
    opponent_team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    team_h_score = models.SmallIntegerField()
    team_a_score = models.SmallIntegerField()
    round = models.SmallIntegerField()
    total_points = models.SmallIntegerField()
    minutes = models.SmallIntegerField()
    goals_scored = models.SmallIntegerField()
    assists = models.SmallIntegerField()
    clean_sheets = models.SmallIntegerField()
    goals_conceded = models.SmallIntegerField()
    own_goals = models.SmallIntegerField()
    penalties_saved = models.SmallIntegerField()
    penalties_missed = models.SmallIntegerField()
    yellow_cards = models.SmallIntegerField()
    red_cards = models.SmallIntegerField()
    saves = models.SmallIntegerField()
    bonus = models.SmallIntegerField()
    bps = models.SmallIntegerField()
    influence = models.FloatField()
    creativity = models.FloatField()
    threat = models.FloatField()
    ict_index = models.FloatField()
    value = models.FloatField()
    transfers_balance = models.IntegerField()
    selected = models.IntegerField()
    transfers_in = models.IntegerField()
    transfers_out = models.IntegerField()

    class Meta:
        unique_together = [['player', 'fixture']]

    def __str__(self):
        return f'{self.player} - {self.fixture}'


class Fixture(models.Model):
    code = models.IntegerField()
    team_h = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='home_team')
    team_h_score = models.SmallIntegerField(null=True)
    team_a = models.ForeignKey(Team, null=True, on_delete=models.CASCADE, related_name='away_team')
    team_a_score = models.SmallIntegerField(null=True)
    finished = models.BooleanField()
    minutes = models.SmallIntegerField()
    kickoff_time = models.DateTimeField(null=True)
    is_home = models.BooleanField()
    difficulty = models.SmallIntegerField()

    class Meta:
        unique_together=[['code','is_home']]

    def __str__(self):
        if self.is_home:
            text = f'{self.team_h} - ({self.team_a})'
        else:
            text = f'({self.team_h}) - {self.team_a}'
        return text