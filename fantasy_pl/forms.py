from django import forms
from django.core.validators import ValidationError
from django.forms import ModelChoiceField

from fantasy_pl.models import Player, Team, Position


class GetPlayerDataForm(forms.Form):
    id = forms.IntegerField(label='Get by ID', required=False,
                            widget=forms.NumberInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Id number of player'}))
    team = forms.ModelChoiceField(label='Get by Team', required=False,
                                  queryset=Team.objects.all().order_by('name'),
                                  widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    all = forms.BooleanField(label='Get all', required=False,
                             widget=forms.CheckboxInput(
                                 attrs={'class': 'form-control'}))


CHOICES_FIX = [(0, 'Update Fixtures')]


class GetFixtureForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'custom-radio'}),
        label=False,
        choices=CHOICES_FIX)


CHOICES_DATA = [(0, 'Download data to JSON'), (1, 'Populate tables'),
                (2, 'Update tables')]


class GetDataForm(forms.Form):
    choice = forms.ChoiceField(widget=forms.RadioSelect(
        attrs={'class': 'custom-radio'}),
        label=False,
        choices=CHOICES_DATA)


class GetUserteamForm(forms.Form):
    fpl_id = forms.IntegerField(label=False,
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Provide ID of your user in FPL'}))


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=64, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control',
               'placeholder': 'Search for player...'}))


stats = (
    ('points_per_game', 'Points per game'),
    ('total_points', 'Total Points'),
    ('now_cost', 'Cost',),
    ('form', 'Form'),
    ('minutes', 'Minutes'),
    ('assists', 'Assists'),
    ('goals_scored', 'Goals scored'),
    ('own_goals', 'Own goals'),
    ('influence', 'Influence'),
    ('influence_rank', 'Influence Rank'),
    ('creativity', 'Creativity'),
    ('creativity_rank', 'Creativity rank'),
    ('threat', 'Threat'),
    ('threat_rank','Threat rank'),
    ('clean_sheets', 'Clean sheets'),
    ('goals_conceded', 'Goals conceded'),
    ('saves', 'Saves'),
    ('penalties_saved', 'Penalties saved'),
    ('yellow_cards', 'Yellow cards'),
    ('red_cards', 'Red cards'),
    ('dreamteam_count', 'Dreamteam count'),
    ('selected_by_percent', 'Selected by percent'),
    ('transfers_in', 'Transfers In'),
    ('transfers_out', 'Transfers Out')
)


class ChartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(ChartForm, self).__init__(*args, **kwargs)
        # assign a (computed, I assume) default value to the choice field
        self.initial['x_axis'] = 'points_per_game'
        self.initial['y_axis'] = 'now_cost'
        self.initial['size_points'] = 'selected_by_percent'


    
    x_axis = forms.ChoiceField(label='Choose X axis value',
                                choices = stats, widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    y_axis = forms.ChoiceField(label='Choose Y axis value',
                                choices = stats, widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    size_points = forms.ChoiceField(label='Choose dot size value',
                                choices = stats, widget=forms.Select(
                                      attrs={'class': 'form-control'}))
    limit = forms.IntegerField(label='Choose minimum time of play [%]',
                widget=forms.NumberInput(
                    attrs={'type': 'range', 'class': 'custom-range',
                           'id': 'limit', 'step': '5', 'min': '0',
                           'max': '100'}), required=True)

    def clean(self):
        cleaned_data = super(ChartForm, self).clean()
        x = cleaned_data.get('x_axis')
        y = cleaned_data.get('y_axis')
        size = cleaned_data.get('size_points')

        if len(set([x, y, size])) != 3:
            raise forms.ValidationError('The options you choose must be unique.')


class PlayerSearchForm(forms.Form):
    position = forms.ModelChoiceField(label='Position',
                                      queryset=Position.objects.all(),
                                      required=False,
                                      widget=forms.Select(
                                          attrs={'class': 'form-control'}))
    max = forms.FloatField(label='Max Cost',
                           required=False, widget=forms.NumberInput(
            attrs={'class': 'form-control'}))

    def clean(self):

        max = self.cleaned_data['max']
        if max == None:
            max = 100

        if max < 0:
            raise forms.ValidationError('Max value must be greater than 0.')


class PlayerChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.second_name} ({obj.team.short_name}) - \
                 {obj.now_cost}\xa3'


class UserTeamForm(forms.Form):
    gkp1 = PlayerChoiceField(label='Goalkeeper',
                            queryset=Player.objects.filter(
                                position=1).order_by('-now_cost'),
                            widget=forms.Select(
                                attrs={'class': 'form-control', }))
    gkp2 = PlayerChoiceField(label='Goalkepper 2',
                             queryset=Player.objects.filter(
                                 position=1).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    def1 = PlayerChoiceField(label='Defender 1',
                             queryset=Player.objects.filter(
                                 position=2).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    def2 = PlayerChoiceField(label='Defender 2',
                             queryset=Player.objects.filter(
                                 position=2).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    def3 = PlayerChoiceField(label='Defender 3',
                             queryset=Player.objects.filter(
                                 position=2).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    def4 = PlayerChoiceField(label='Defender 4',
                             queryset=Player.objects.filter(
                                 position=2).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    def5 = PlayerChoiceField(label='Defender 5',
                             queryset=Player.objects.filter(
                                 position=2).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    mid1 = PlayerChoiceField(label='Middlefielder 1',
                             queryset=Player.objects.filter(
                                 position=3).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    mid2 = PlayerChoiceField(label='Middlefielder 2',
                             queryset=Player.objects.filter(
                                 position=3).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    mid3 = PlayerChoiceField(label='Middlefielder 3',
                             queryset=Player.objects.filter(
                                 position=3).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    mid4 = PlayerChoiceField(label='Middlefielder 4',
                             queryset=Player.objects.filter(
                                 position=3).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    mid5 = PlayerChoiceField(label='Middlefielder 5',
                             queryset=Player.objects.filter(
                                 position=3).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    fwd1 = PlayerChoiceField(label='Forward 1',
                             queryset=Player.objects.filter(
                                 position=4).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    fwd2 = PlayerChoiceField(label='Forward 2',
                             queryset=Player.objects.filter(
                                 position=4).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))
    fwd3 = PlayerChoiceField(label='Forward 3',
                             queryset=Player.objects.filter(
                                 position=4).order_by('-now_cost'),
                             widget=forms.Select(
                                 attrs={'class': 'form-control'}))

    @staticmethod
    def check_unique_models(player_list):
        for p1 in range(len(player_list)):
            for p2 in range(len(player_list)):
                if p1 != p2:
                    if player_list[p1] == player_list[p2]:
                        return [False, player_list[p1]]
        else:
            return [True]

    def clean(self):
        cleaned_data = super().clean()
        fwd1 = cleaned_data.get('fwd1')
        fwd2 = cleaned_data.get('fwd2')
        fwd3 = cleaned_data.get('fwd3')
        l_fwd = [fwd1, fwd2, fwd3]

        fwd_check = self.check_unique_models(l_fwd)
        if fwd_check[0] == False:
            raise ValidationError(f'Repeated forward {fwd_check[1]}')

        mid1 = cleaned_data.get('mid1')
        mid2 = cleaned_data.get('mid2')
        mid3 = cleaned_data.get('mid3')
        mid4 = cleaned_data.get('mid4')
        mid5 = cleaned_data.get('mid5')
        l_mid = [mid1, mid2, mid3, mid4, mid5]

        mid_check = self.check_unique_models(l_mid)
        if mid_check[0] == False:
            raise ValidationError(f'Repeated midfielder {mid_check[1]}')

        def1 = cleaned_data.get('def1')
        def2 = cleaned_data.get('def2')
        def3 = cleaned_data.get('def3')
        def4 = cleaned_data.get('def4')
        def5 = cleaned_data.get('def5')
        l_def = [def1, def2, def3, def4, def5]

        def_check = self.check_unique_models(l_def)
        if def_check[0] == False:
            raise ValidationError(f'Repeated defender {def_check[1]}')

        gkp1 = cleaned_data.get('gkp1')
        gkp2 = cleaned_data.get('gkp2')
        l_gkp = [gkp1, gkp2]

        gkp_check = self.check_unique_models(l_gkp)
        if gkp_check[0] == False:
            raise ValidationError(f'Repeated forward {gkp_check[1]}')

        players_list = l_gkp + l_def + l_mid + l_fwd
        teams = {}
        for p in players_list:
            team = p.team
            if team in teams.keys():
                teams[team].append(p)
            else:
                teams[team] = [p]

        for k, v in teams.items():
            if len(teams[k]) > 3:
                names = ', '.join(
                    [f'{_.first_name} {_.second_name}' for _ in v])
                raise ValidationError(f'Too much player from team '
                                      f'{k.short_name}: {names}')
