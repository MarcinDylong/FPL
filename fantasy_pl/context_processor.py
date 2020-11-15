from .models import Team, Position, UserTeam, User
from .forms import SearchForm

from django.core.exceptions import ObjectDoesNotExist

def get_userTeam_players_id(request):

    player_id_list = []
    try:
        current_user = User.objects.get(username=request.user.username)
        uteam = UserTeam.objects.filter(user=current_user).values()[0]
        for k, v in uteam.items():
            if k == 'user_id':
                continue
            elif k.endswith('_id'):
                player_id_list.append(v)
            else:
                pass
    except (ObjectDoesNotExist,IndexError):
        pass
    return player_id_list


def my_cp(request):

    player_id_list = get_userTeam_players_id(request)
    teams = Team.objects.all().order_by('name')
    positions = Position.objects.all().order_by('id')
    ctx = {
        'teams': teams,
        'positions': positions,
        'search_form': SearchForm,
        'ut_ids': player_id_list
    }
    
    return ctx
