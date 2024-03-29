from django import forms

from datetime import datetime

from flatpickr import DateTimePickerInput
from tinymce.widgets import TinyMCE

from .models import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['name', 'url', 'start_at', 'end_at', 'administrator', 'moderator_name', 'moderator_email', 'staff', 'participants', 'hide']
        help_texts = {'hide': 'Hide from public banner list'}
        widgets = {
            'start_at': DateTimePickerInput(options={"dateFormat":"D, M j, Y h:i K"}).start_of('banner'),
            'end_at': DateTimePickerInput(options={"dateFormat":"D, M j, Y h:i K"}).end_of('banner'),
            'staff': TinyMCE(),
            'participants': TinyMCE(),
        }
