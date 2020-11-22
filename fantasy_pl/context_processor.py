from .models import Team, Position, UserFplPicks, UserFpl, UserFplSeason
from .forms import SearchForm

from django.core.exceptions import ObjectDoesNotExist

def get_userTeam_players_id(request):

    player_id_list = []
    try:
        current_user = UserFpl.objects.get(user=request.user)
        user_season = UserFplSeason.objects.filter(userfpl=current_user).order_by('id').last()
        picks = UserFplPicks.objects.get(user=user_season)
        for k,v in picks.__dict__.items():
            if k == 'user_id':
                continue
            elif k.endswith('_id'):
                player_id_list.append(v)
            else:
                pass
    except:
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
