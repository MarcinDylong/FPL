from .models import Team, Position, Message
from .forms import SearchForm
from django.db.models.functions import Substr


def my_cp(request):
    teams = Team.objects.all().order_by('name')
    positions = Position.objects.all().order_by('id')
    messages = Message.objects.filter(recipient=request.user.id)[:3]
    messages = messages.annotate(short_content=Substr('content',1,32))
    ctx = {
        'teams': teams,
        'positions': positions,
        'search_form': SearchForm,
        'messages_short': messages
    }

    return ctx

