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
    ('now_cost', 'Cost',),
    ('form', 'Form'),
    ('total_points', 'Total Points'),
)


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
            raise forms.ValidationError('Max value must be greater than 0')


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
    gkp2 = PlayerChoiceField(label='Bench goalkepper',
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
    def5 = PlayerChoiceField(label='Bench defender',
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
    mid5 = PlayerChoiceField(label='Bench middlefielder',
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
    fwd3 = PlayerChoiceField(label='Bench forward',
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
                        return [True, player_list[p1]]
        else:
            return [False]

    def clean(self):
        cleaned_data = super().clean()
        fwd1 = cleaned_data.get('fwd1')
        fwd2 = cleaned_data.get('fwd2')
        fwdb = cleaned_data.get('fwdb')
        l_fwd = [fwd1, fwd2, fwdb]

        fwd_check = self.check_unique_models(l_fwd)
        if fwd_check[0] == True:
            raise ValidationError(f'Repeated forward {fwd_check[1]}')

        mdf1 = cleaned_data.get('mdf1')
        mdf2 = cleaned_data.get('mdf2')
        mdf3 = cleaned_data.get('mdf3')
        mdf4 = cleaned_data.get('mdf4')
        mdfb = cleaned_data.get('mdfb')
        l_mdf = [mdf1, mdf2, mdf3, mdf4, mdfb]

        mdf_check = self.check_unique_models(l_mdf)
        if mdf_check[0] == True:
            raise ValidationError(f'Repeated forward {mdf_check[1]}')

        def1 = cleaned_data.get('def1')
        def2 = cleaned_data.get('def2')
        def3 = cleaned_data.get('def3')
        def4 = cleaned_data.get('def4')
        defb = cleaned_data.get('defb')
        l_def = [def1, def2, def3, def4, defb]

        def_check = self.check_unique_models(l_def)
        if def_check[0] == True:
            raise ValidationError(f'Repeated forward {def_check[1]}')

        gkp = cleaned_data.get('gkp')
        gkpb = cleaned_data.get('gkpb')
        l_gkp = [gkp, gkpb]

        gkp_check = self.check_unique_models(l_gkp)
        if gkp_check[0] == True:
            raise ValidationError(f'Repeated forward {gkp_check[1]}')

        players_list = l_gkp + l_def + l_mdf + l_fwd
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
