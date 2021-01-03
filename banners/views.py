from django.shortcuts import render
from django.http import HttpResponse

def banner_list(request):
    return HttpResponse("listing banners...")

def banner_edit(request):
    return HttpResponse("editing banner...")

def banner_view(request):
    return HttpResponse("viewing banner...")
