from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import LoginForm


class IndexView(View):

    def get(self, request):
        # user =
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

class MorrisView(View):

    def get(self, request):
        ctx = {'title': "Morris charts"}
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
