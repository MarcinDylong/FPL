from .models import Team, Position
from .forms import SearchForm

def my_cp(request):
    teams = Team.objects.all().order_by('name')
    positions = Position.objects.all().order_by('id')

    ctx = {
        'teams': teams,
        'positions': positions,
        'search_form': SearchForm
    }

    return ctx

