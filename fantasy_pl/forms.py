from django import forms
from django.core.validators import EmailValidator, URLValidator
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(label='User name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # myfield = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))


class SearchForm(forms.Form):
    search = forms.CharField(label='', max_length=64, widget=forms.TextInput(
        attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Search...'}))
