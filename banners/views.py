from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags

from allauth.account.models import EmailAddress

from smtplib import SMTPException
from collections import defaultdict
from datetime import datetime

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
            messages.error(request, 'That slot has already been reserved')
        else:
            slot = Slot(banner=banner, user=request.user)
            slot.start_at = interval['start_at']
            slot.end_at = interval['end_at']
            slot.save()

            local_start_time = timezone.localtime(slot.start_at).strftime(date_format)

            #.make the time a link to a calendar download
            messages.success(request, 'Successfully reserved {} prayer slot'.format(local_start_time))

            email = request.user.email
            if EmailAddress.objects.filter(email=email, verified=True).exists():
                html = '{}, <p>Thank you for signing up for the {} prayer slot for {}!</p> <p>Please add a reminder to your calendar.</p>'.format(request.user.first_name, local_start_time, banner.name)
                result = send_mail(
                    'Pray for {}'.format(banner.name),
                    strip_tags(html),
                    None, # (defaults to DEFAULT_FROM_EMAIL)
                    [email],
                    fail_silently=True,
                    html_message=html,
                )
                if result == 1:
                    messages.info(request, 'You should receive an email confirmation soon')
    elif 'release_slot_id' in request.POST and request.POST['release_slot_id'].isnumeric():
        slot = Slot.objects.get(pk=int(request.POST['release_slot_id']))
        if slot.user == request.user:
            slot.delete()

            local_start_time = timezone.localtime(slot.start_at).strftime(date_format)
            messages.info(request, 'Released {} prayer slot'.format(local_start_time))

    return redirect('/banners/{}'.format(banner.pk))


class StaffParticipants(DetailView):
    model = Banner
    template_name = 'banners/staff_participants.html'

@login_required
@require_POST
def email_staff_participants(request, pk):
    banner = Banner.objects.get(pk=pk)

    try:
        email = request.user.email
        if EmailAddress.objects.filter(email=email, verified=True).exists():
            html = '<h3>Staff</h3> <p>{}</p> <h3>Participants</h3> <p>{}</p>'.format(banner.staff, banner.participants)
            result = send_mail(
                '{} Staff & Participants'.format(banner.name),
                strip_tags(html),
                None, # (defaults to DEFAULT_FROM_EMAIL)
                [request.user.email],
                fail_silently=False,
                html_message=html,
            )
            if result == 1:
                messages.success(request, 'Email sent to {}'.format(request.user.email))
            else:
                raise
        else:
            messages.error(request, 'Your email address ({}) has not been verified. Visit your Profile to manage your email addresses.'.format(email))
    except SMTPException:
        messages.error(request, 'Failed to send email')
    except:
        messages.warning(request, 'Something went wrong. If you do not receive the email in a few minutes please try again or contact us.')

    return redirect('/banners/{}'.format(banner.pk))

@login_required
@require_POST
def send_banner_slot_reminders(request, pk):
    banner = Banner.objects.get(pk=pk)

    if not request.user.has_perm('banners.send_slot_reminders') and request.user != banner.administrator:
        messages.error(request, 'You do not have permission to send the prayer slot reminder email.')
        return redirect('/')

    user_slots = defaultdict(list)

    for slot in banner.slot_set.all():
        user_slots[slot.user].append(slot)

    date_format = "%b %d, %I:%M %p %Z"

    i = 0
    for user, slots in user_slots.items():
        # If all of the user's slots' reminders have been sent, skip this user.
        if not [s for s in slots if not s.reminder_sent]:
            continue

        if EmailAddress.objects.filter(email=user.email, verified=True).exists():
            html = '{},\n<p>This is a reminder that you reserved the following prayer slots.</p>\n'.format(user.first_name)

            for slot in slots:
                html += '{} - {}<br>\n'.format(timezone.localtime(slot.start_at).strftime(date_format), timezone.localtime(slot.end_at).strftime(date_format))

            result = send_mail(
                "Don't forget to pray for {}!".format(banner.name),
                strip_tags(html),
                None, # (defaults to DEFAULT_FROM_EMAIL)
                [user.email],
                fail_silently=True,
                html_message=html,
            )
            if result == 1:
                i += 1
                for slot in slots:
                    slot.reminder_sent = datetime.now()
                    slot.save()

    if i == 0:
        messages.info(request, "No reminders sent. This may be because they have already been sent, or an email address has not been verified.")
    else:
        messages.success(request, 'Reminder sent to {} user{}'.format(i, '' if i==1 else 's' ))

    return redirect('/')
