from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .models import User

class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'church', 'weekend']
    template_name = 'profile.html'
    success_url = '/'

    def get_object(self):
        return self.request.user
