from django.urls import path

from . import views

urlpatterns = [
    path('', views.BannerList.as_view(), name='banner-list'),
    path('create/', views.BannerCreate.as_view(), name='banner-create'),
    path('<int:pk>/', views.BannerSlots.as_view(), name='banner-slots'),
    path('<int:pk>/edit/', views.BannerEdit.as_view(), name='banner-edit'),
    path('<int:pk>/delete/', views.BannerDelete.as_view(), name='banner-delete'),

    path('<int:pk>/reserve/', views.reserve_slot, name='reserve-slot'),

    path('<int:pk>/staff-participants/', views.StaffParticipants.as_view(), name='staff-participants'),
    path('<int:pk>/staff-participants/email/', views.email_staff_participants, name='email-staff-participants'),
]
