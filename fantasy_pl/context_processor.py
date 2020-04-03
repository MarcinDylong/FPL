from .models import Team

def my_cp(request):
    teams = Team.objects.all()
    ctx = {
    'teams': teams
    }
    return ctx