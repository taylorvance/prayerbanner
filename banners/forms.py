from django import forms

from datetime import datetime

from website.widgets import DateTimePicker
from flatpickr import DateTimePickerInput
from .models import Banner


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['name', 'start_at', 'end_at', 'administrator', 'moderator', 'staff', 'participants', 'url']
        widgets = {
            'start_at': DateTimePickerInput(options={"dateFormat":"D, M j, Y h:i K"}).start_of('banner'),
            'end_at': DateTimePickerInput(options={"dateFormat":"D, M j, Y h:i K"}).end_of('banner'),
        }
