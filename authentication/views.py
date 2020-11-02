from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from .forms import LoginForm, SignUpForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                return render(request, "accounts/login.html", {"form": form})
        else:
            return render(request, "accounts/login.html", {"form": form})


class RegisterUserView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/register.html",
                      {"form": form, "msg": None, "success": False})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            messages.success(request, "User Created, please log in")
            return redirect('/login/')

        return render(request, "accounts/register.html", {"form": form})


class PasswordResetRequestView(View):
    def get(self, request):
        password_reset_form = PasswordResetForm()
        return render(request=request,
                      template_name="accounts/reset_password.html",
                      context={"form": password_reset_form})

    def post(self, request):
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/reset_password_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return redirect("done/")
            else:
                messages.error(request, 'Email was not found in database.')
                return render(request=request,
                              template_name="accounts/reset_password.html",
                              context={"form": password_reset_form})
        else:
            return render(request=request,
                          template_name="accounts/reset_password.html",
                          context={"form": password_reset_form})

def LogoutView(request):
    logout(request)
    return redirect('fpl:home')