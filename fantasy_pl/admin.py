from django.contrib import admin

from fantasy_pl.models import Team, Player, Position#, UserTeam, User

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Position)
# admin.site.register(UserTeam)