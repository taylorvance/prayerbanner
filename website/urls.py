from django.urls import path

from . import views
from banners import views as banner_views

urlpatterns = [
    path('', banner_views.BannerList.as_view(), name='banner-list'),
]
