from django.urls import path

from . import views

urlpatterns = [
    path('', views.BannerList.as_view(), name='banner-list'),
    path('view/<int:pk>/', views.BannerView.as_view(), name='banner-view'),
    path('edit/<int:pk>/', views.BannerEdit.as_view(), name='banner-edit'),
]
