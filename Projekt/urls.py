from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from fantasy_pl.views import IndexView

app_name = 'fantasy_pl'

urlpatterns = [
    path('', include(('fantasy_pl.urls', 'fantasy_pl'), namespace='fpl')),
    path('admin/', admin.site.urls),

]
