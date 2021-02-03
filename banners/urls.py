from django.urls import path

from . import views

urlpatterns = [
    path('', views.BannerList.as_view(), name='banner-list'),
    path('<int:pk>/', views.BannerView.as_view(), name='banner-view'),
    path('<int:pk>/edit/', views.BannerEdit.as_view(), name='banner-edit'),
    path('create/', views.BannerCreate.as_view(), name='banner-create'),

    path('<int:pk>/reserve/', views.reserve_slot, name='reserve-slot'),
]
