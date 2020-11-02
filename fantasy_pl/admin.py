from django.contrib import admin

from fantasy_pl.models import Team, Player, Position, UserTeam, PlayerHistory,\
                              Fixtures

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Position)
admin.site.register(UserTeam)
admin.site.register(PlayerHistory)
admin.site.register(Fixtures)