from django.contrib import admin

from fantasy_pl.models import Team, Player, Position, UserTeam, PlayerHistory,\
                              Fixtures, UserFpl, UserFplSeason, UserFplPicks, \
                              UserTeam

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Position)
admin.site.register(UserTeam)
admin.site.register(PlayerHistory)
admin.site.register(Fixtures)
<<<<<<< HEAD
# admin.site.register(UserTeam)
# admin.site.register(UserFpl)
# admin.site.register(UserFplSeason)
# admin.site.register(UserFplPicks)
=======
admin.site.register(UserTeam)
admin.site.register(UserFpl)
admin.site.register(UserFplSeason)
admin.site.register(UserFplPicks)
>>>>>>> 77c2455980d6812dbcb8bdf1b80bcb55dce2bd52
