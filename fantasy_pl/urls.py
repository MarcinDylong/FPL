from django.urls import path

from .views import IndexView, LoginView, BlankView, ButtonsView, FlotView, FormsView, GridView, IconsView, MorrisView, \
                   NotificationsView, PanelsView, TablesView, TypographyView

app_name = 'fantasy_pl'

urlpatterns = [
    path(r'^$', LoginView.as_view(), name="login"),
    path('index/', IndexView.as_view(), name="index"),
    path(r'^blank/$', BlankView.as_view(), name="blank"),
    path(r'^buttons/$', ButtonsView.as_view(), name="buttons"),
    path(r'^flot/$', FlotView.as_view(), name="flot"),
    path(r'^forms/$', FormsView.as_view(), name="forms"),
    path(r'^grid/$', GridView.as_view(), name="grid"),
    path(r'^icons/$', IconsView.as_view(), name="icons"),
    path(r'^morris/$', MorrisView.as_view(), name="morris"),
    path(r'^notifications/$', NotificationsView.as_view(), name="notifications"),
    path(r'^panels/$', PanelsView.as_view(), name="panels"),
    path(r'^tables/$', TablesView.as_view(), name="tables"),
    path(r'^typography/$', TypographyView.as_view(), name="typography"),
]
