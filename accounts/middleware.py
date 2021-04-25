from django.utils import timezone

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            if request.session.get('detected_tz'): # relies on django-tz-detect mw
                # Update the user's preferred timezone if it is different from the one that django-tz-detect detected.
                tz = timezone.get_current_timezone()
                if tz and tz != request.user.tzinfo:
                    request.user.timezone = tz
                    request.user.save()

        return response
