from django.urls import path

from . import views

urlpatterns = [
    path('', views.banner_list, name='banner_list'),
    path('edit', views.banner_edit, name='banner_edit'),
    path('view', views.banner_view, name='banner_view'),
]
