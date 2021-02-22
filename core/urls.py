from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("authentication.urls", 'authentication'), namespace='auth')),  # authentication
    path("", include(("fantasy_pl.urls", 'fantasy_pl'), namespace='fpl')), # fantasy_pl app
]

handler400 = 'fantasy_pl.views.views_display_data.view_400'
handler403 = 'fantasy_pl.views.views_display_data.view_403'
handler404 = 'fantasy_pl.views.views_display_data.view_404'
handler500 = 'fantasy_pl.views.views_display_data.view_500'
