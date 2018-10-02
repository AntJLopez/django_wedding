from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wedding.local_settings import STRIPE_SECRET_KEY
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Guest
from .forms import GuestForm, RSVPForm

stripe.api_key = STRIPE_SECRET_KEY


@login_required
def guest_list(request, template_name='guests/list.html'):
    guests = Guest.objects.all()
    data = {'guests': guests}
    return render(request, template_name, data)


@login_required
def guest_create(request, template_name='guests/form.html'):
    form = GuestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('guest_list')
    data = {'form': form}
    return render(request, template_name, data)


@login_required
def guest_read(request, pk, template_name='guests/read.html'):
    guest = get_object_or_404(Guest, pk=pk)
    data = {'guest': guest}
    return render(request, template_name, data)


@login_required
def guest_update(request, pk, template_name='guests/form.html'):
    guest = get_object_or_404(Guest, pk=pk)
    form = GuestForm(request.POST or None, instance=guest)
    if form.is_valid():
        form.save()
        return redirect('guest_list')
    data = {'form': form}
    return render(request, template_name, data)


@login_required
def guest_delete(request, pk, template_name='guests/delete.html'):
    guest = get_object_or_404(Guest, pk=pk)
    if request.method == 'POST':
        guest.delete()
        return redirect('guest_list')
    data = {'guest': guest}
    return render(request, template_name, data)


@require_POST
def rsvp(request):
    response = {'errors': {}}

    form = RSVPForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
    else:
        # The form is invalid
        response['errors'] = form.errors

    return JsonResponse(response)
