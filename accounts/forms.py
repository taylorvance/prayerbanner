from django import forms
from django.core.exceptions import ValidationError

import re
import logging

from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField


logger = logging.getLogger('db')

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # hp stands for [Pooh's favorite treat] + [weed synonym]
        self.hp_hint = None

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        # The following is unfortunate and hacky, but this is the current production mole I'm whacking.
        # If they didn't enter a church or weekend
        if not cleaned_data.get("church") and not cleaned_data.get("weekend"):
            # If the first and last name end with the same two capital letters, preceded by any lowercase letter
            p = re.compile('[a-z]([A-Z]{2})$')
            m1 = p.search(first_name)
            m2 = p.search(last_name)
            if m1 and m2 and m1.group(1) == m2.group(1):
                logger.debug("%s %s (%s) \"signed up\" ;)" % (first_name, last_name, cleaned_data.get("email")))
                self.hp_hint = "Thank you for signing up! You should receive a verification email at %s soon." % (cleaned_data.get("email"))
                raise ValidationError(self.hp_hint)

    def save(self, request):
        user = super().save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.church = self.cleaned_data['church']
        user.weekend = self.cleaned_data['weekend']

        user.save()
        return user
