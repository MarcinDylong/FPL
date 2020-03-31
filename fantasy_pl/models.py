from django.db import models


# Create your models here.


class Team(models.Model):
    code = models.IntegerField()
    draw = models.IntegerField()
    form = models.TextField(max_length=64, null=True)
    # id = models.IntegerField()
    loss = models.IntegerField()
    name = models.CharField(max_length=32)
    played = models.IntegerField()
    points = models.IntegerField()
    position = models.IntegerField()
    short_name = models.CharField(max_length=4)
    strength = models.IntegerField()
    team_division = models.TextField(null=True)
    unavailable = models.BooleanField
    win = models.IntegerField()
    strength_overall_home = models.IntegerField()
    strength_overall_away = models.IntegerField()
    strength_attack_home = models.IntegerField()
    strength_attack_away = models.IntegerField()
    strength_defence_home = models.IntegerField()
    strength_defence_away = models.IntegerField()
