from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.contrib.auth.decorators import login_required  # noqa
from .local_settings import GOOGLE_API_KEY
from sections import views
from guests.models import Guest


def home(request):
    sections = []
    sections.append(views.header(request))
    print(views.header)

    params = {
        'sections': sections,
        'google_api_key': GOOGLE_API_KEY
    }
    try:
        guest = Guest.objects.get(id=request.session['guest'])
        params['guest'] = guest
    except (KeyError, ValueError):
        pass
    return render(request, 'wedding/home.html', params)


def guest_login(request, guest_username):
    try:
        guest = Guest.objects.get(username=guest_username)
        request.session['guest'] = guest.id
    except Guest.DoesNotExist:
        pass
    return redirect('home')


def guest_logout(request):
    try:
        del request.session['guest']
    except KeyError:
        pass
    return redirect('home')
