from django import forms
from allauth.account.forms import SignupForm


class SignupForm(SignupForm):
    first_name = forms.CharField(required=True, max_length=50, label='First Name')
    last_name = forms.CharField(required=True, max_length=50, label='Last Name')
    church = forms.CharField(required=False, max_length=100, label='Church')
    weekend = forms.CharField(required=False, max_length=100, label='Weekend Attended')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.church = self.cleaned_data['church']
        user.weekend = self.cleaned_data['weekend']
        user.save()
        return user
