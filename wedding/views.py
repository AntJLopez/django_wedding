from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.contrib.auth.decorators import login_required  # noqa
from .local_settings import GOOGLE_API_KEY


def home(request):
    params = {'google_api_key': GOOGLE_API_KEY}
    return render(request, 'wedding/home.html', params)
