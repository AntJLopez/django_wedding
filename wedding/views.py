from django.shortcuts import render, redirect, get_object_or_404  # noqa
from django.contrib.auth.decorators import login_required  # noqa
from .local_settings import GOOGLE_API_KEY, STRIPE_PUBLIC_KEY
from guests.models import Guest
from payments.forms import GiftForm


def home(request, gift_form=GiftForm()):
    sections = []
    sections.append({
        'template': 'wedding/sections/header.html'})
    sections.append({
        'title': 'Our Story',
        'template': 'wedding/sections/our_story.html'})
    sections.append({
        'title': 'The Proposal',
        'template': 'wedding/sections/proposal.html'})
    sections.append({
        'title': 'Wedding Party',
        'template': 'wedding/sections/wedding_party.html'})
    sections.append({
        'title': 'Family',
        'template': 'wedding/sections/family.html'})
    sections.append({
        'title': 'Schedule',
        'template': 'wedding/sections/schedule.html'})
    sections.append({
        'title': 'Getting There',
        'template': 'wedding/sections/directions.html'})
    sections.append({
        'template': 'wedding/sections/map.html'})
    sections.append({
        'title': 'Accommodations',
        'template': 'wedding/sections/accommodations.html'})
    sections.append({
        'title': 'Gifts',
        'template': 'wedding/sections/gifts.html'})
    sections.append({
        'title': 'RSVP',
        'template': 'wedding/sections/rsvp.html'})
    params = {
        'sections': sections,
        'google_api_key': GOOGLE_API_KEY,
        'stripe_public_key': STRIPE_PUBLIC_KEY,
        'gift_form': gift_form
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
