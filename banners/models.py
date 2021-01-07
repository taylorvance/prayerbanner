from django.db import models
from django.conf import settings


class Banner(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_banners')
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='administered_banners')
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='moderated_banners')
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    staff = models.TextField(blank=True)
    participants = models.TextField(blank=True)

    class Meta:
        ordering = ["start_at", "end_at"]

    def __str__(self):
        return self.name


class Slot(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    class Meta:
        ordering = ["banner", "start_at"]
