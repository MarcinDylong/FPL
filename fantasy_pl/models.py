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


class Message(models.Model):
    subject = models.CharField(max_length=64, null=False)
    content = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    date_sent = models.DateTimeField(auto_now_add=True)


class UserTeam(models.Model):
    name = models.CharField(max_length=32, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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


    # class Meta:
        # unique_together = ['gkp','def1','def2','def3','def4','mdf1','mdf2','mdf3','mdf4','fwd1','fwd2']