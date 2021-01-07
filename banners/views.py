from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.utils import timezone

from .models import Banner, Slot


class BannerList(ListView):
    model = Banner
    # queryset = Banner.objects.get(end_at__gt=timezone.now())

class BannerView(DetailView):
    model = Banner

class BannerEdit(DetailView):
    model = Banner
