from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Banner, Slot


class BannerList(ListView):
    model = Banner
    # queryset = Banner.objects.get(end_at__gt=timezone.now())
    template_name = 'banners/banner_list.html'

class BannerView(DetailView):
    model = Banner
    template_name = 'banners/banner_view.html'

class BannerEdit(DetailView):
    model = Banner
    template_name = 'banners/banner_edit.html'
