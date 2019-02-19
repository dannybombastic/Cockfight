"""from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

def check_email_exists(request, backend, details, uid, user=None, *args, **kwargs):
    email = details.get('email', '')
    provider = backend.name

    # check if social user exists to allow logging in (not sure if this is necessary)
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    # check if given email is in use
    count = User.objects.filter(username=email).count()

    success_message = messages.success(request, 'Sorry User With That Email Already Exists')

    # user is not logged in, social profile with given uid doesn't exist
    # and email is in use
    if not user and not social and count:
        return HttpResponseRedirect(reverse('accounts:registrar', success_message))
"""
