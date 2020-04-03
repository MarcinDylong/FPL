from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .models import Team
from .forms import LoginForm
from .getters import read_json, get_data


class IndexView(View):

    def get(self, request):
        # user =
        # teams = Team.objects.all()
        ctx = {'title': 'Landing page'}
        return render(request, "components/index.html", ctx)


class BlankView(View):

    def get(self, request):
        ctx = {'title': "Blank Page"}
        return render(request, "components/blank.html", ctx)


class ButtonsView(View):

    def get(self, request):
        ctx = {'title': "Buttons"}
        return render(request, "components/buttons.html", ctx)


class FlotView(View):

    def get(self, request):
        ctx = {'title': "Flot Charts"}
        return render(request, "components/flot.html", ctx)


class FormsView(View):

    def get(self, request):
        ctx = {'title': "Forms"}
        return render(request, "components/forms.html", ctx)


class GridView(View):

    def get(self, request):
        ctx = {'title': "Grid"}
        return render(request, "components/grid.html", ctx)


class IconsView(View):

    def get(self, request):
        ctx = {'title': "Icons"}
        return render(request, "components/icons.html", ctx)


# class LoginView(View):
#
#     def get(self, request):
#         ctx = {'title': "Log in"}
#         return render(request, "components/login.html", ctx)


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
                return redirect('/index')
            else:
                return render(request, 'components/login.html', {'form': LoginForm(), 'unsuccessful': True})

        return redirect('')


def LogoutView(request):
    logout(request)
    return redirect('/')

class PopulateTeamsView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.add_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        teams = data['teams']
        try:
            for t in teams:
                team = Team()
                team.id = int(t['id'])
                team.code = t['code']
                team.draw = t['draw']
                team.form = t['form']
                team.loss = t['loss']
                team.name = t['name']
                team.played = t['played']
                team.points = t['points']
                team.position = t['position']
                team.short_name = t['short_name']
                team.strength = t['strength']
                team.team_division = t['team_division']
                team.unavailable = t['unavailable']
                team.win = t['win']
                team.strength_overall_home = t['strength_overall_home']
                team.strength_overall_away = t['strength_overall_away']
                team.strength_attack_home = t['strength_attack_home']
                team.strength_attack_away = t['strength_attack_away']
                team.strength_defence_home = t['strength_defence_home']
                team.strength_defence_away = t['strength_defence_away']
                team.save()
        except:
            return render(request, "components/blank.html", {'name': "Błąd"})

        return redirect('/index')


class UpdateTeamsView(PermissionRequiredMixin,View):
    permission_required = 'fantasy_pl.change_team'
    permission_denied_message = 'Sorry, You do not have permission!'

    def get(self, request):
        data = read_json()
        teams = data['teams']
        # try:
        for t in teams:
            team = Team.objects.get(id=t['id'])
            team.draw = t['draw']
            team.form = t['form']
            team.loss = t['loss']
            team.played = t['played']
            team.points = t['points']
            team.position = t['position']
            team.strength = t['strength']
            team.unavailable = t['unavailable']
            team.win = t['win']
            team.strength_overall_home = t['strength_overall_home']
            team.strength_overall_away = t['strength_overall_away']
            team.strength_attack_home = t['strength_attack_home']
            team.strength_attack_away = t['strength_attack_away']
            team.strength_defence_home = t['strength_defence_home']
            team.strength_defence_away = t['strength_defence_away']
            team.save()
        # except:
        #     return render(request, "components/blank.html", {'name': "Błąd"})

        return redirect('/index')
        # return render(request, "components/blank.html", data)



class MorrisView(View):

    def get(self, request):
        data = {'title': "Morris charts"}
        ctx = data['teams'][0]
        return render(request, "components/morris.html", ctx)


class NotificationsView(View):

    def get(self, request):
        ctx = {'title': "Notifications"}
        return render(request, "components/notifications.html", ctx)


class PanelsView(View):

    def get(self, request):
        ctx = {'title': "Panels and wells"}
        return render(request, "components/panels-wells.html", ctx)


class TablesView(View):

    def get(self, request):
        ctx = {'title': "Tables"}
        return render(request, "components/tables.html", ctx)


class TypographyView(View):

    def get(self, request):
        ctx = {'title': "Typography"}
        return render(request, "components/typography.html", ctx)