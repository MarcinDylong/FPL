from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class UserFpl(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    fpl = models.IntegerField(null=True)
    joined_time = models.DateTimeField(null=True)
    started_event = models.IntegerField(null=True)
    favourite_team = models.IntegerField(null=True)
    player_first_name = models.CharField(max_length=16, null=True)
    player_last_name = models.CharField(max_length=16, null=True)
    player_region_name = models.CharField(max_length=32, null=True)
    player_region_iso_code_short = models.CharField(max_length=6, null=True)
    player_region_iso_code_long = models.CharField(max_length=6, null=True)
    summary_overall_points = models.IntegerField(null=True)
    summary_overall_rank = models.IntegerField(null=True)
    summary_event_points = models.IntegerField(null=True)
    summary_event_rank = models.IntegerField(null=True)
    current_event = models.IntegerField(null=True)
    name = models.CharField(max_length=64, null=True)
    last_deadline_bank = models.FloatField(null=True)
    last_deadline_value = models.FloatField(null=True)
    last_deadline_total_transfers = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.player_first_name} {self.player_last_name}'

    class Meta:
        unique_together = ('user', 'fpl',)


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

    class Meta:
        unique_together = ('id','pulse_id','name',)


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
    cost_change_event = models.IntegerField(null=True)
    cost_change_event_fall = models.IntegerField(null=True)
    cost_change_start = models.IntegerField(null=True)
    cost_change_start_fall = models.IntegerField(null=True)
    dreamteam_count = models.IntegerField(null=True)
    ep_next = models.FloatField(null=True)
    ep_this = models.FloatField(null=True)
    event_points = models.IntegerField(null=True)
    form = models.FloatField(null=True)
    in_dreamteam = models.BooleanField(null=True)
    now_cost = models.FloatField(null=True)
    points_per_game = models.FloatField(null=True)
    selected_by_percent = models.FloatField(null=True)
    transfers_in = models.IntegerField(null=True)
    transfers_in_event = models.IntegerField(null=True)
    transfers_out = models.IntegerField(null=True)
    transfers_out_event = models.IntegerField(null=True)
    special = models.BooleanField(null=True)
    total_points = models.IntegerField(null=True)
    value_form = models.FloatField(null=True)
    value_season = models.FloatField(null=True)
    bonus = models.IntegerField(null=True)
    bps = models.FloatField(null=True)
    influence = models.FloatField(null=True)
    creativity = models.FloatField(null=True)
    threat = models.FloatField(null=True)
    ict_index = models.FloatField(null=True)
    influence_rank = models.IntegerField(null=True)
    influence_rank_type = models.IntegerField(null=True)
    creativity_rank = models.IntegerField(null=True)
    creativity_rank_type = models.IntegerField(null=True)
    threat_rank = models.IntegerField(null=True)
    threat_rank_type = models.IntegerField(null=True)
    ict_index_rank = models.IntegerField(null=True)
    ict_index_rank_type = models.IntegerField(null=True)
    corners_and_indirect_freekicks_order = models.IntegerField(null=True)
    corners_and_indirect_freekicks_text = models.CharField(max_length=128, null=True)
    direct_freekicks_order = models.IntegerField(null=True)
    direct_freekicks_text = models.CharField(max_length=128, null=True)
    penalties_order = models.IntegerField(null=True)
    penalties_text = models.CharField(max_length=128, null=True)

    objects = models.Manager()

    def __str__(self):
        return f'{self.first_name} {self.second_name}'

    def form_str(self):
        return f'{self.first_name} {self.second_name} - {self.now_cost} Ł'

    def ppg_chart_str(self):
        return f'{self.second_name}'

    def ratio(self):
        if self.now_cost != 0:
            return round(self.points_per_game/self.now_cost,2)
        else:
            return 0

    def next_game(self):
        games = PlayerHistory.objects.filter(player_id=self.id)
        next_game = games.filter(finished=False).filter(kickoff_time__isnull=False).order_by('event').first()
        try:
            if next_game.is_home == True:
                return f'H - {next_game.team_a.short_name}'
            else:
                return f'A - {next_game.team_h.short_name}'
        except AttributeError:
            return '-'

    def last_game(self, gw:int):
        try:
            games = PlayerHistory.objects.filter(player_id=self.id)
            last_game = games.get(event_id=gw)
            if last_game.is_home == True:
                return f'H - {last_game.team_a.short_name}'
            else:
                return f'A - {last_game.team_h.short_name}'
        except:
            return '-'

    def last_game_stats(self, gw:int): 
        try:
            games = PlayerHistory.objects.filter(player_id=self.id)
            last_game = games.get(event_id=gw)
            return last_game
        except :
            return '-'

    class Meta:
        unique_together = ('id','first_name','second_name',)


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    deadline_time = models.DateTimeField()
    average_entry_score = models.IntegerField()
    finished = models.BooleanField()
    data_checked = models.BooleanField()
    highest_score = models.IntegerField(null=True)
    is_previous = models.BooleanField()
    is_current = models.BooleanField()
    is_next = models.BooleanField()
    most_selected = models.ForeignKey(Player, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='most_selected')
    most_transferred_in = models.ForeignKey(Player, null=True,
                                            on_delete=models.SET_NULL,
                                            related_name='most_transferred_ind')
    top_element = models.ForeignKey(Player, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='top_element')
    top_element_points = models.IntegerField(null=True)
    transfers_made = models.IntegerField(null=True)
    most_captained = models.ForeignKey(Player, null=True,
                                       on_delete=models.SET_NULL,
                                       related_name='most_captained')
    most_vice_captained = models.ForeignKey(Player, null=True,
                                            on_delete=models.SET_NULL,
                                            related_name='most_vice_captained')
    total_players = models.IntegerField()

    class Meta:
        unique_together=('id', 'name',)

    def __str__(self):
        return f'{self.name}'

class UserFplHistory(models.Model):
    userfpl = models.OneToOneField(UserFpl, on_delete=models.CASCADE)
    past = JSONField()
    chips = JSONField()

    class Meta:
        unique_together = ('userfpl',)

    def __str__(self):
        return f'{self.userfpl} history'


class UserFplSeason(models.Model):
    userfpl = models.ForeignKey(UserFpl, on_delete=models.CASCADE,
                                related_name='user_history')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True,
                              related_name='user_event')
    points = models.IntegerField(null=True)
    total_points = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    rank_sort = models.IntegerField(null=True)
    overall_rank = models.IntegerField(null=True)
    bank = models.FloatField(null=True)
    value = models.FloatField(null=True)
    event_transfers = models.IntegerField(null=True)
    event_transfers_cost = models.IntegerField(null=True)
    points_on_bench = models.IntegerField(null=True)

    class Meta:
        unique_together=('userfpl', 'event',)

    def __str__(self):
        return f'Season data for {self.userfpl}'



class UserFplPicks(models.Model):
    user = models.OneToOneField(UserFplSeason, on_delete=models.CASCADE)
    pck1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick1')
    pck1_pos = models.IntegerField()
    pck1_mult = models.IntegerField()
    pck1_cpt = models.BooleanField()
    pck1_vcpt = models.BooleanField()
    pck2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick2')
    pck2_pos = models.IntegerField()
    pck2_mult = models.IntegerField()
    pck2_cpt = models.BooleanField()
    pck2_vcpt = models.BooleanField()
    pck3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick3')
    pck3_pos = models.IntegerField()
    pck3_mult = models.IntegerField()
    pck3_cpt = models.BooleanField()
    pck3_vcpt = models.BooleanField()
    pck4 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick4')
    pck4_pos = models.IntegerField()
    pck4_mult = models.IntegerField()
    pck4_cpt = models.BooleanField()
    pck4_vcpt = models.BooleanField()
    pck5 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick5')
    pck5_pos = models.IntegerField()
    pck5_mult = models.IntegerField()
    pck5_cpt = models.BooleanField()
    pck5_vcpt = models.BooleanField()
    pck6 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick6')
    pck6_pos = models.IntegerField()
    pck6_mult = models.IntegerField()
    pck6_cpt = models.BooleanField()
    pck6_vcpt = models.BooleanField()
    pck7 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick7')
    pck7_pos = models.IntegerField()
    pck7_mult = models.IntegerField()
    pck7_cpt = models.BooleanField()
    pck7_vcpt = models.BooleanField()
    pck8 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick8')
    pck8_pos = models.IntegerField()
    pck8_mult = models.IntegerField()
    pck8_cpt = models.BooleanField()
    pck8_vcpt = models.BooleanField()
    pck9 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick9')
    pck9_pos = models.IntegerField()
    pck9_mult = models.IntegerField()
    pck9_cpt = models.BooleanField()
    pck9_vcpt = models.BooleanField()
    pck10 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick10')
    pck10_pos = models.IntegerField()
    pck10_mult = models.IntegerField()
    pck10_cpt = models.BooleanField()
    pck10_vcpt = models.BooleanField()
    pck11 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick11')
    pck11_pos = models.IntegerField()
    pck11_mult = models.IntegerField()
    pck11_cpt = models.BooleanField()
    pck11_vcpt = models.BooleanField()
    pck12 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick12')
    pck12_pos = models.IntegerField()
    pck12_mult = models.IntegerField()
    pck12_cpt = models.BooleanField()
    pck12_vcpt = models.BooleanField()
    pck13 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick13')
    pck13_pos = models.IntegerField()
    pck13_mult = models.IntegerField()
    pck13_cpt = models.BooleanField()
    pck13_vcpt = models.BooleanField()
    pck14 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick14')
    pck14_pos = models.IntegerField()
    pck14_mult = models.IntegerField()
    pck14_cpt = models.BooleanField()
    pck14_vcpt = models.BooleanField()
    pck15 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='pick15')
    pck15_pos = models.IntegerField()
    pck15_mult = models.IntegerField()
    pck15_cpt = models.BooleanField()
    pck15_vcpt = models.BooleanField()

    class Meta:
        unique_together = ('user',)


class UserTeam(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    gkp1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='gkp1')
    gkp1_pos = models.IntegerField()
    gkp1_mult = models.IntegerField()
    gkp1_cpt = models.BooleanField()
    gkp1_vcpt = models.BooleanField()
    gkp2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='gkp2')
    gkp2_pos = models.IntegerField()
    gkp2_mult = models.IntegerField()
    gkp2_cpt = models.BooleanField()
    gkp2_vcpt = models.BooleanField()
    def1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def1')
    def1_pos = models.IntegerField()
    def1_mult = models.IntegerField()
    def1_cpt = models.BooleanField()
    def1_vcpt = models.BooleanField()
    def2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def2')
    def2_pos = models.IntegerField()
    def2_mult = models.IntegerField()
    def2_cpt = models.BooleanField()
    def2_vcpt = models.BooleanField()
    def3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def3')
    def3_pos = models.IntegerField()
    def3_mult = models.IntegerField()
    def3_cpt = models.BooleanField()
    def3_vcpt = models.BooleanField()
    def4 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def4')
    def4_pos = models.IntegerField()
    def4_mult = models.IntegerField()
    def4_cpt = models.BooleanField()
    def4_vcpt = models.BooleanField()
    def5 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='def5')
    def5_pos = models.IntegerField()
    def5_mult = models.IntegerField()
    def5_cpt = models.BooleanField()
    def5_vcpt = models.BooleanField()
    mid1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mid1')
    mid1_pos = models.IntegerField()
    mid1_mult = models.IntegerField()
    mid1_cpt = models.BooleanField()
    mid1_vcpt = models.BooleanField()
    mid2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mid2')
    mid2_pos = models.IntegerField()
    mid2_mult = models.IntegerField()
    mid2_cpt = models.BooleanField()
    mid2_vcpt = models.BooleanField()
    mid3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mid3')
    mid3_pos = models.IntegerField()
    mid3_mult = models.IntegerField()
    mid3_cpt = models.BooleanField()
    mid3_vcpt = models.BooleanField()
    mid4 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mid4')
    mid4_pos = models.IntegerField()
    mid4_mult = models.IntegerField()
    mid4_cpt = models.BooleanField()
    mid4_vcpt = models.BooleanField()
    mid5 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='mid5')
    mid5_pos = models.IntegerField()
    mid5_mult = models.IntegerField()
    mid5_cpt = models.BooleanField()
    mid5_vcpt = models.BooleanField()
    fwd1 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwd1')
    fwd1_pos = models.IntegerField()
    fwd1_mult = models.IntegerField()
    fwd1_cpt = models.BooleanField()
    fwd1_vcpt = models.BooleanField()
    fwd2 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwd2')
    fwd2_pos = models.IntegerField()
    fwd2_mult = models.IntegerField()
    fwd2_cpt = models.BooleanField()
    fwd2_vcpt = models.BooleanField()
    fwd3 = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name='fwd3')
    fwd3_pos = models.IntegerField()
    fwd3_mult = models.IntegerField()
    fwd3_cpt = models.BooleanField()
    fwd3_vcpt = models.BooleanField()
    overall_cost = models.FloatField(default=0)
    ppg = models.FloatField(default=0)
    influence = models.FloatField(default=0)
    creativity = models.FloatField(default=0)
    threat = models.FloatField(default=0)
    total_points = models.SmallIntegerField(default=0)
    dt_apps = models.FloatField(default=0)
    novelty = models.FloatField(default=0)

    class Meta:
        unique_together = ('user','event',)



class Fixtures(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL,
                              related_name='f_event')
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

    class Meta:
        unique_together = ('id', 'event',)


class PlayerHistory(models.Model):
    player = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL)
    position = models.SmallIntegerField(null=True)
    fixture = models.ForeignKey(Fixtures, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL,
                              related_name='ph_event')
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