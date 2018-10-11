from django.http import JsonResponse, HttpResponseRedirect  # noqa
from django.urls import reverse
from django.views.decorators.http import require_POST
from wedding.local_settings import STRIPE_SECRET_KEY
import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Guest
from .forms import GuestForm, RSVPForm
from payments.models import Payer, PaymentCategory, Payment
from pprint import pprint  # noqa

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


def test_rsvp(request):
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('test_rsvp_complete'))
    else:
        form = RSVPForm()

    return render(request, 'wedding/test_rsvp.html', {'form': form})


def test_rsvp_complete(request):
    return render(request, 'wedding/test_rsvp_complete.html')


@require_POST
def rsvp(request):
    response = {'errors': {}}
    form = RSVPForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        for key, value in request.POST.items():
            words = key.split('_')
            if words[0] == 'unnamed':
                guest = Guest.objects.get(pk=int(words[-1]))
                if words[1] == 'first':
                    guest.first_name = value
                elif words[1] == 'last':
                    guest.last_name = value
                guest.save()

        guest = Guest.objects.get(id=cd['guest_id'])
        if cd['attending'] and cd['nights_onsite'] > 0:
            # The guest(s) will be staying onsite, so we need payment
            amount = len(cd['guests']) * (35 + 48 * cd['nights_onsite'])
            try:
                stripe_kwargs = {
                    'amount': int(amount * 100),  # Convert dollars to cents
                    'currency': 'usd',
                    'source': cd['stripe_token'],
                    'description': "Lodging for Tony & Haya's Wedding"}
                if guest.email:
                    stripe_kwargs['receipt_email'] = guest.email
                charge = stripe.Charge.create(**stripe_kwargs)
                payment = Payment(
                    amount=amount,
                    payer=Payer.objects.get_or_create(guest=guest)[0],
                    category=PaymentCategory.objects.get(name='Lodging'),
                    stripe_id=charge.id)
                payment.save()
            except stripe.error.CardError as card_error:
                # There was an error processing the credit card
                card_error = str(card_error)
                if 'Request req' in card_error:
                    card_error = card_error.split(':', 1)[1].strip()
                response['errors']['gift_cc'] = [card_error]
        if not response['errors']:
            form.save()
    else:
        # The form is invalid
        response['errors'] = form.errors

    return JsonResponse(response)
