from django.urls import path

from .views import IndexView, LoginView, BlankView, ButtonsView, FlotView, FormsView, GridView, IconsView, MorrisView, \
                   NotificationsView, PanelsView, TablesView, TypographyView

app_name = 'fantasy_pl'

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('index/', IndexView.as_view(), name="index"),
    path('blank/', BlankView.as_view(), name="blank"),
    path('buttons/', ButtonsView.as_view(), name="buttons"),
    path('flot/', FlotView.as_view(), name="flot"),
    path('forms/', FormsView.as_view(), name="forms"),
    path('grid/', GridView.as_view(), name="grid"),
    path('icons/', IconsView.as_view(), name="icons"),
    path('morris/', MorrisView.as_view(), name="morris"),
    path('notifications/', NotificationsView.as_view(), name="notifications"),
    path('panels/', PanelsView.as_view(), name="panels"),
    path('tables/', TablesView.as_view(), name="tables"),
    path('typography/', TypographyView.as_view(), name="typography"),
]
