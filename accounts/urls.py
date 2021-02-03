from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('profile/', views.UpdateProfile.as_view(), name='profile'),

    re_path(r'', include('allauth.urls')),
]
