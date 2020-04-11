from urllib import request

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import ValidationError, EmailValidator
from .models import Team
from django.contrib.auth import authenticate, login, logout


class LoginForm(forms.Form):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label='User name:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    rep_password = forms.CharField(label='Repeat password:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    # supporter = forms.ModelChoiceField(label='Choose your team:',
    #                                    widget=forms.Select(attrs={'class': 'form-control'}),
    #                                    queryset=Team.objects.all())

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
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Search...'}))


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=64, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Search...'}))
