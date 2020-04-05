from django.db import models


# Create your models here.


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=4)
    position = models.IntegerField()
    played = models.IntegerField()
    win = models.IntegerField()
    draw = models.IntegerField()
    loss = models.IntegerField()
    points = models.IntegerField()
    form = models.TextField(max_length=8, null=True)
    strength = models.IntegerField()
    strength_overall_home = models.IntegerField()
    strength_overall_away = models.IntegerField()
    strength_attack_home = models.IntegerField()
    strength_attack_away = models.IntegerField()
    strength_defence_home = models.IntegerField()
    strength_defence_away = models.IntegerField()

    def __str__(self):
        return self.name


class Position(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    name_short = models.CharField(max_length=4)

    def __str__(self):
        return self.name


class Player(models.Model):
    chance_of_playing_next_round = models.IntegerField(null=True)
    chance_of_playing_this_round = models.IntegerField(null=True)
    code = models.IntegerField
    cost_change_event = models.IntegerField()
    cost_change_event_fall = models.IntegerField()
    cost_change_start = models.IntegerField()
    cost_change_start_fall = models.IntegerField
    dreamteam_count = models.IntegerField()
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    ep_next = models.FloatField()
    ep_this = models.FloatField()
    event_points = models.IntegerField()
    first_name = models.CharField(max_length=32)
    form = models.FloatField()
    id = models.IntegerField(primary_key=True)
    in_dreamteam = models.BooleanField()
    news = models.TextField(max_length=256)
    news_added = models.DateTimeField(null=True)
    now_cost = models.FloatField()
    points_per_game = models.FloatField()
    second_name = models.CharField(max_length=32)
    selected_by_percent = models.FloatField
    special = models.BooleanField
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    total_points = models.IntegerField
    value_form = models.FloatField()
    value_season = models.FloatField()
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
    bonus = models.IntegerField()
    bps = models.IntegerField()
    influence = models.FloatField()
    creativity = models.FloatField()
    threat = models.FloatField()
    ict_index = models.FloatField()

    def __str__(self):
        return f'{self.first_name} {self.second_name}'
