from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

from smtplib import SMTPException

from .models import Banner, Slot
from .forms import BannerForm


class BannerList(ListView):
    queryset = Banner.objects.filter(end_at__gt=timezone.now(), hide=False)
    template_name = 'banners/banner_list.html'


class BannerSlots(DetailView):
    model = Banner
    template_name = 'banners/banner_slots.html'


class BannerCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'banners.add_banner'
    model = Banner
    form_class = BannerForm
    template_name = 'banners/banner_create.html'
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super(BannerCreate, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Banner()
        # Set author to session user
        kwargs['instance'].author = self.request.user
        return kwargs


class BannerEdit(UserPassesTestMixin, UpdateView):
    model = Banner
    form_class = BannerForm
    template_name = 'banners/banner_edit.html'
    success_url = '/'

    def test_func(self):
        return self.request.user.has_perm('banners.change_banner') or self.request.user == self.get_object().administrator


class BannerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'banners.delete_banner'
    model = Banner
    success_url = '/'


@login_required
def reserve_slot(request, pk):
    banner = Banner.objects.get(pk=pk)

    date_format = "%b %d, %I:%M %p %Z"

    if 'interval_idx' in request.POST and request.POST['interval_idx'].isnumeric():
        interval = banner.intervals()[int(request.POST['interval_idx'])]

        if interval['slot']:
            #.error: slot already reserved
            pass
        else:
            slot = Slot(banner=banner, user=request.user)
            slot.start_at = interval['start_at']
            slot.end_at = interval['end_at']
            slot.save()

            messages.add_message(request, messages.INFO, 'Successfully reserved {} prayer slot'.format(timezone.localtime(slot.start_at).strftime(date_format)))

            #.redir to thank you page with calendar downloads
            return redirect('/banners/{}'.format(banner.pk))
    elif 'release_slot_id' in request.POST and request.POST['release_slot_id'].isnumeric():
        slot = Slot.objects.get(pk=int(request.POST['release_slot_id']))
        if slot.user == request.user:
            slot.delete()

            messages.add_message(request, messages.INFO, 'Successfully released {} prayer slot'.format(timezone.localtime(slot.start_at).strftime(date_format)))

    return redirect('/banners/{}'.format(banner.pk))


class StaffParticipants(DetailView):
    model = Banner
    template_name = 'banners/staff_participants.html'

@login_required
@require_POST
def email_staff_participants(request, pk):
    banner = Banner.objects.get(pk=pk)

    try:
        result = send_mail(
            'Prayer Banner - {} Staff & Participants'.format(banner.name),
            '<h4>Staff</h4><p>{}</p><h4>Participants</h4><p>{}</p>'.format(banner.staff, banner.participants),
            None, # (defaults to DEFAULT_FROM_EMAIL)
            [request.user.email],
            fail_silently=False,
        )
        if result == 1:
            messages.success(request, 'Email sent to {}'.format(request.user.email))
        else:
            raise
    except SMTPException:
        messages.error(request, 'Failed to send email')
    except:
        messages.warning(request, 'Something went wrong. If you do not receive the email in a few minutes please try again or contact us.')

    return redirect('/banners/{}'.format(banner.pk))
