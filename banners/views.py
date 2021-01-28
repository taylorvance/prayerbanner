from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Banner, Slot


class BannerList(ListView):
    queryset = Banner.objects.filter(end_at__gt=timezone.now())
    template_name = 'banners/banner_list.html'

class BannerView(DetailView):
    model = Banner
    template_name = 'banners/banner_view.html'

class BannerEdit(DetailView):
    model = Banner
    template_name = 'banners/banner_edit.html'

@login_required
def reserve_slot(request, pk):
    banner = Banner.objects.get(pk=pk)

    if 'interval_idx' in request.POST and request.POST['interval_idx'].isnumeric():
        interval = banner.intervals()[int(request.POST['interval_idx'])]

        if interval['slot']:
            #.error: slot already reserved
            pass
        else:
            slot = Slot(banner=banner, user=request.user)
            slot.start_at = interval['start_at']
            slot.end_at = interval['end_at']
            slot.save()

            return redirect('/banners/{}'.format(banner.pk))
            #.redir to thank you page with calendar downloads
    elif 'release_slot_id' in request.POST and request.POST['release_slot_id'].isnumeric():
        slot = Slot.objects.get(pk=int(request.POST['release_slot_id']))
        if slot.user == request.user:
            slot.delete()

    return redirect('/banners/{}'.format(banner.pk))
