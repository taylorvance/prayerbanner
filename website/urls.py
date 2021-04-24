from django.urls import path
from django.views.generic import TemplateView

from banners import views as banner_views

urlpatterns = [
    path('', banner_views.BannerList.as_view(), name='banner-list'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
]
