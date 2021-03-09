from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={"placeholder": "Username",
               "class": "form-control"}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"placeholder": "Password",
               "class": "form-control"}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if not User.objects.filter(username=username).exists():
            raise ValidationError('Wrong username')

        if not authenticate(username=username, password=password):
            raise ValidationError('Wrong password')


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": "Username",
               "class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={"placeholder": "Email",
               "class": "form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password",
               "class": "form-control"}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={"placeholder": "Password check",
               "class": "form-control"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if User.objects.filter(username=username).exists():
            raise ValidationError('This name is already taken')

        if User.objects.filter(email=email).exists():
            raise ValidationError(f'There is already account for {email}')

        if password1 != password2:
            raise ValidationError('Repeated password do not match')
