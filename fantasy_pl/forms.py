from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import ValidationError, MinValueValidator
from fantasy_pl.models import Player, Team, Position


class LoginForm(forms.Form):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class GetDataForm(forms.Form):
    id = forms.IntegerField(label='Get by ID', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))
    team = forms.ModelChoiceField(label='Get by Team', required=False, queryset=Team.objects.all().order_by('name'),
                            widget=forms.Select(attrs={'class': 'form-control'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='User name:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    rep_password = forms.CharField(label='Repeat password:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        # Automatically called by form.is_valid()
        # ...can also use 'clean_FIELDNAME()' for individual fields

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise ValidationError('This name is already taken')

        password = self.cleaned_data['password']
        rep_password = self.cleaned_data['rep_password']

        if password != rep_password:
            raise ValidationError('Repeated password do not match')


class ResetPasswordForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    rep_password = forms.CharField(label='Repeat new password',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        user_id = self.cleaned_data['user_id']
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        rep_password = self.cleaned_data['rep_password']

        user = User.objects.get(pk=user_id)

        if user is None:
            raise forms.ValidationError('User do no exist')

        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError('Wrong old password')

        if new_password != rep_password:
            raise forms.ValidationError('Repeated password do not match')


class MessageForm(forms.Form):
    subject = forms.CharField(label='Subject', max_length=64, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Subject...'}))
    recipient = forms.ModelChoiceField(label='Recipient', queryset=User.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Content....'}))


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=64, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Search...'}))


stats = (
    ('points_per_game', 'Points per game'),
    ('now_cost', 'Cost',),
    ('form', 'Form'),
    ('total_points', 'Total Points'),
)


class AdvSearchForm(forms.Form):
    position = forms.ModelChoiceField(label='Position', queryset=Position.objects.all(), required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    stats = forms.ChoiceField(label='Stat', choices=stats, required=False,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    min = forms.FloatField(label='Min Value',
                           required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max = forms.FloatField(label='Max Value',
                           required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        position = self.cleaned_data['position']
        stats = self.cleaned_data['stats']
        min = self.cleaned_data['min']
        if min == None:
            min = 0
        max = self.cleaned_data['max']
        if max == None:
            max = 1500

        if (min != None and max != None) and (min >= max):
            raise forms.ValidationError('Minimum value has to be smaller than maximum.')

        if min < 0 or max < 0:
            raise forms.ValidationError('Min and Max value must be greater than 0')


class UserTeamForm(forms.Form):
    gkp = forms.ModelChoiceField(label='Goalkeeper',
                                 queryset=Player.objects.filter(position=1).order_by('-now_cost'),
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    def1 = forms.ModelChoiceField(label='Defender 1',
                                  queryset=Player.objects.filter(position=2).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    def2 = forms.ModelChoiceField(label='Defender 2',
                                  queryset=Player.objects.filter(position=2).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    def3 = forms.ModelChoiceField(label='Defender 3',
                                  queryset=Player.objects.filter(position=2).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    def4 = forms.ModelChoiceField(label='Defender 4',
                                  queryset=Player.objects.filter(position=2).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    mdf1 = forms.ModelChoiceField(label='Middlefielder 1',
                                  queryset=Player.objects.filter(position=3).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    mdf2 = forms.ModelChoiceField(label='Middlefielder 2',
                                  queryset=Player.objects.filter(position=3).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    mdf3 = forms.ModelChoiceField(label='Middlefielder 3',
                                  queryset=Player.objects.filter(position=3).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    mdf4 = forms.ModelChoiceField(label='Middlefielder 4',
                                  queryset=Player.objects.filter(position=3).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    fwd1 = forms.ModelChoiceField(label='Forward 1',
                                  queryset=Player.objects.filter(position=4).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    fwd2 = forms.ModelChoiceField(label='Forward 2',
                                  queryset=Player.objects.filter(position=4).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    gkpb = forms.ModelChoiceField(label='Bench goalkepper',
                                  queryset=Player.objects.filter(position=1).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    defb = forms.ModelChoiceField(label='Bench defender',
                                  queryset=Player.objects.filter(position=2).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    mdfb = forms.ModelChoiceField(label='Bench middlefielder',
                                  queryset=Player.objects.filter(position=3).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    fwdb = forms.ModelChoiceField(label='Bench forward',
                                  queryset=Player.objects.filter(position=4).order_by('-now_cost'),
                                  widget=forms.Select(attrs={'class': 'form-control'}))

    def clean(self):
        # cleaned_data = super().clean()
        fwd1 = self.cleaned_data['fwd1']
        fwd2 = self.cleaned_data['fwd2']
        fwdb = self.cleaned_data['fwdb']

        l_fwd = [fwd1, fwd2, fwdb]
        if len(l_fwd) != len(set(l_fwd)):
            raise ValidationError('Repeated player on forward position.')

        mdf1 = self.cleaned_data['mdf1']
        mdf2 = self.cleaned_data['mdf2']
        mdf3 = self.cleaned_data['mdf3']
        mdf4 = self.cleaned_data['mdf4']
        mdfb = self.cleaned_data['mdfb']
        l_mdf = [mdf1, mdf2, mdf3, mdf4, mdfb]
        if len(l_mdf) != len(set(l_mdf)):
            raise ValidationError('Repeated player on middlefielder position.')

        def1 = self.cleaned_data['def1']
        def2 = self.cleaned_data['def2']
        def3 = self.cleaned_data['def3']
        def4 = self.cleaned_data['def4']
        defb = self.cleaned_data['defb']
        l_def = [def1, def2, def3, def4, defb]
        if len(l_def) != len(set(l_def)):
            raise ValidationError('Repeated player on defender position.')
