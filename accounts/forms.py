from django import forms

from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField


class MySignupForm(SignupForm):
    first_name = forms.CharField(required=True, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    church = forms.CharField(required=False, max_length=100)
    weekend = forms.CharField(
        required=False,
        max_length=100,
        label='Participant weekend',
        help_text='What was the name of the weekend that you attended as a participant?',
    )
    captcha = CaptchaField(help_text="Don't worry &mdash; if you get it wrong you can try again. The rest of your input will be saved.")

    def save(self, request):
        user = super(MySignupForm, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.church = self.cleaned_data['church']
        user.weekend = self.cleaned_data['weekend']

        user.save()
        return user
