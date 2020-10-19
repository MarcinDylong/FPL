from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from fantasy_pl.forms import UserTeamForm
from fantasy_pl.models import UserTeam


class UserTeamView(View):

    def team_overall(self, uteam, ctx):
        luteam = [uteam.gkp, uteam.gkpb, uteam.def1, uteam.def2, uteam.def3,
                  uteam.def4, uteam.defb, uteam.mdf1, uteam.mdf2, uteam.mdf3,
                  uteam.mdf4, uteam.mdfb, uteam.fwd1, uteam.fwd2, uteam.fwdb]
        ctx['uteam'] = luteam

        overall_cost = sum([u.now_cost for u in luteam])
        ctx['overall_cost'] = uteam.overall_cost = round(overall_cost, 1)
        if overall_cost > 100:
            ctx['overpaid'] = round(overall_cost - 100, 2)

        ppg = sum([u.points_per_game for u in luteam])
        ctx['ppg'] = uteam.ppg = round(ppg, 1)

        influence = sum([u.influence for u in luteam])
        ctx['influence'] = uteam.influence = round(influence, 1)

        creativity = sum([u.creativity for u in luteam])
        ctx['creativity'] = uteam.creativity = round(creativity, 1)

        threat = sum([u.threat for u in luteam])
        ctx['threat'] = uteam.threat = round(threat, 1)

        dreamteam = sum([u.dreamteam_count for u in luteam])
        ctx['dreamteam'] = uteam.dt_apps = round(dreamteam, 1)

        total_points = sum([u.total_points for u in luteam])
        ctx['total_points'] = uteam.total_points = round(total_points, 1)

        novelty = sum([u.selected_by_percent for u in luteam])
        ctx['novelty'] = uteam.novelty = round(novelty / 15, 1)

        uteam.save()
        return ctx

    def get(self, request):
        ctx = {}
        form = UserTeamForm()
        ctx['form'] = form
        ctx['title'] = 'Your Team'

        if UserTeam.objects.filter(user=request.user):
            uteam = UserTeam.objects.get(user=request.user)
            form.fields['gkp'].initial  = uteam.gkp_id
            form.fields['def1'].initial = uteam.def1_id
            form.fields['def2'].initial = uteam.def2_id
            form.fields['def3'].initial = uteam.def3_id
            form.fields['def4'].initial = uteam.def4_id
            form.fields['mdf1'].initial = uteam.mdf1_id
            form.fields['mdf2'].initial = uteam.mdf2_id
            form.fields['mdf3'].initial = uteam.mdf3_id
            form.fields['mdf4'].initial = uteam.mdf4_id
            form.fields['fwd1'].initial = uteam.fwd1_id
            form.fields['fwd2'].initial = uteam.fwd2_id
            form.fields['gkpb'].initial = uteam.gkpb_id
            form.fields['defb'].initial = uteam.defb_id
            form.fields['mdfb'].initial = uteam.mdfb_id
            form.fields['fwdb'].initial = uteam.fwdb_id
            self.team_overall(uteam, ctx)

        return render(request, 'components/userteam.html', ctx)

    def post(self, request):
        form = UserTeamForm(request.POST)
        ctx = {}
        ctx['title'] = 'Your Team'
        if form.is_valid():
            try:
                userTeam = UserTeam.objects.get(user=request.user)
                userTeam.gkp  = form.cleaned_data['gkp']
                userTeam.gkpb = form.cleaned_data['gkpb']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.defb = form.cleaned_data['defb']
                userTeam.mdf1 = form.cleaned_data['mdf1']
                userTeam.mdf2 = form.cleaned_data['mdf2']
                userTeam.mdf3 = form.cleaned_data['mdf3']
                userTeam.mdf4 = form.cleaned_data['mdf4']
                userTeam.mdfb = form.cleaned_data['mdfb']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.fwdb = form.cleaned_data['fwdb']
                userTeam.save()
                ctx['success'] = 'Team updated'
            except ObjectDoesNotExist:
                userTeam = UserTeam()
                userTeam.user = request.user
                userTeam.gkp = form.cleaned_data['gkp']
                userTeam.gkpb = form.cleaned_data['gkpb']
                userTeam.def1 = form.cleaned_data['def1']
                userTeam.def2 = form.cleaned_data['def2']
                userTeam.def3 = form.cleaned_data['def3']
                userTeam.def4 = form.cleaned_data['def4']
                userTeam.defb = form.cleaned_data['defb']
                userTeam.mdf1 = form.cleaned_data['mdf1']
                userTeam.mdf2 = form.cleaned_data['mdf2']
                userTeam.mdf3 = form.cleaned_data['mdf3']
                userTeam.mdf4 = form.cleaned_data['mdf4']
                userTeam.mdfb = form.cleaned_data['mdfb']
                userTeam.fwd1 = form.cleaned_data['fwd1']
                userTeam.fwd2 = form.cleaned_data['fwd2']
                userTeam.fwdb = form.cleaned_data['fwdb']
                userTeam.save()
                ctx['success'] = 'Team created'

            uteam = UserTeam.objects.get(user=request.user)
            self.team_overall(uteam, ctx)
            ctx['form'] = form
            return render(request, 'components/userteam.html', ctx)
        else:
            uteam = UserTeam.objects.get(user=request.user)
            self.team_overall(uteam, ctx)
            ctx['failure'] = True
            ctx['form'] = form
            return render(request, 'components/userteam.html', ctx)