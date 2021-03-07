from django.db import models
from django.conf import settings

from datetime import timedelta

from tinymce.models import HTMLField


class Banner(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_banners')
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    # Field for slot duration? Options 15, 30 (default). May not be changed after creation. It hasn't been needed for 30 years so I'll leave that scope uncrept.
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='administered_banners')
    moderator_name = models.CharField(blank=True, max_length=127)
    moderator_email = models.EmailField(blank=True)
    staff = HTMLField(blank=True)
    participants = HTMLField(blank=True)
    hide = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_at", "end_at"]

    def __str__(self):
        return self.name

    def intervals(self):
        delta = 30
        intervals = []

        cur_datetime = self.start_at
        i = 0

        slots = list(self.slot_set.all())

        while cur_datetime < self.end_at:
            interval = {'i': i, 'start_at': cur_datetime, 'end_at': cur_datetime + timedelta(minutes=30)}

            interval['slot'] = next((x for x in slots if x.start_at==interval['start_at']), None)

            intervals.append(interval)

            cur_datetime = interval['end_at']
            i += 1

        return intervals


class Slot(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        unique_together = [['banner', 'start_at']]
        ordering = ['banner', 'start_at']
