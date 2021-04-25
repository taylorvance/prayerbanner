from django.contrib import admin

from .models import Banner, Slot

class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_at', 'end_at', 'administrator')

class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner', 'user', 'start_at', 'end_at', 'reminder_sent')

admin.site.register(Banner, BannerAdmin)
admin.site.register(Slot, SlotAdmin)
