from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

from fantasy_pl.models import Team, Player, Position, UserTeam

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Position)
admin.site.register(UserTeam)