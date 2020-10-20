import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View

from fantasy_pl.forms import LoginForm, CreateUserForm, ResetPasswordForm, \
    MessageForm
from fantasy_pl.models import Team, Player, Message


class IndexView(View):

    def get(self, request):
        ctx = {'title': 'Landing page'}
        # Random team
        try:
            team = list(Team.objects.all())
            random.shuffle(team)
            photo = "/static/logos/" + team[0].short_name.lower() + ".png "
            cnt = len(Player.objects.filter(team=team[0]))
            ctx['team'] = team[0]
            ctx['cnt'] = cnt
            ctx['photo'] = photo
        except:
            pass
        # Random player
        try:
            player = list(Player.objects.all())
            random.shuffle(player)
            tp = Team.objects.get(name=player[0].team)
            tpphoto = "/static/logos/" + tp.short_name.lower() + ".png "
            ctx['player'] = player[0]
            ctx['tp'] = tp
            ctx['tpphoto'] = tpphoto
        except:
            pass
        # Random statistic
        try:
            stats_names = ['goals_scored', 'minutes', 'assists', 'own_goals',
                           'penalties_saved', 'yellow_cards', 'red_cards']
            random.shuffle(stats_names)
            s_name = stats_names[0]
            rename = Player.objects.extra(select={'stat': s_name, 'id': 'id',
                                                  'name': 'second_name'})
            rename_t = Player.objects.select_related('team')
            rename.union(rename_t)
            stat = rename.order_by('-stat')[:10]
            name_stat = s_name.replace('_', ' ').capitalize()
            ctx['stat'] = stat
            ctx['name_stat'] = name_stat
        except:
            pass

        return render(request, "components/index/index.html", ctx)


class BlankView(View):
    def get(self, request):
        ctx = {'title': "Blank Page"}
        return render(request, "components/blank.html", ctx)


class LoginView(View):
    def get(self, request):
        ctx = {'title': "Log in", 'form': LoginForm()}
        return render(request, 'components/login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                # request.session['user_id'] = User.id
                return render(request, 'components/login.html',
                              {'form': LoginForm(), 'unsuccessful': True})

        return redirect('/')


def LogoutView(request):
    logout(request)
    return redirect('/')


class CreateUserView(View):

    def get(self, request):
        ctx = {'form': CreateUserForm(), 'title': 'Create user'}
        return render(request, 'components/create_user.html', ctx)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Don't use User.objects.create() as it won't hash the password!
            # ...need to: user.set_password()
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            return redirect('/login')
        else:
            ctx = {'form': CreateUserForm(), 'title': 'Create user'}
            return render(request, 'components/create_user.html', ctx)


class ChangetPasswordView(LoginRequiredMixin, View):
    login_url = '/login'
    permission_required = 'exercises.change_user'

    def get(self, request, user_id):
        try:
            if 'user_name' in request.session:
                username = request.session['user_name']
                user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        return render(request, 'components/change_password.html', {
            'form': ResetPasswordForm(initial={
                'user_id': user_id, 'title': 'Change password'
            }),
            'logged_user': request.user.username
        })

    def post(self, request, user_id):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=user_id)
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            return redirect('/login')
        else:
            return render(request, 'components/change_password.html',
                          {'form': form, 'unsuccessful': True,
                           'title': 'Change password'})


class SendMessageView(View):

    def get(self, request):
        form = MessageForm()
        return render(request, 'components/message_sending.html',
                      {'form': form, 'title': 'Send Massage'})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = User.objects.get(
                username=form.cleaned_data['recipient'])
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            ctx = {'form': MessageForm()}
            try:
                Message.objects.create(subject=subject, content=content,
                                       recipient=recipient,
                                       sender=request.user)
                ctx['success'] = 'Message was sent!'
            except:
                ctx['failure'] = 'Something went wrong'

            ctx['title'] = 'Send message'
            return render(request, 'components/message_sending.html', ctx)
        else:
            ctx = {'form': MessageForm()}
            ctx['failure'] = 'Cannot send message with empty Subject or content!'
            return render(request, 'components/message_sending.html', ctx)


class MessageReceivedView(View):

    def get(self, request):
        messages = Message.objects.filter(recipient=request.user.id).order_by('date_sent')
        return render(request, 'components/message_received.html', {'messages': messages, 'title': 'Received'})


class MessageSentView(View):

    def get(self, request):
        messages = Message.objects.filter(sender=request.user.id).order_by('date_sent')
        return render(request, 'components/message_sent.html', {'messages': messages, 'title': 'Sent'})