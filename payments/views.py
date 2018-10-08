from django.http import JsonResponse
from django.views.decorators.http import require_POST
from wedding.local_settings import STRIPE_SECRET_KEY
import stripe
from .forms import GiftForm
from .models import Payment, PaymentCategory, Payer
from guests.models import Guest

stripe.api_key = STRIPE_SECRET_KEY


@require_POST
def make_gift(request):
    response = {'errors': {}}

    form = GiftForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        gift = Payment(amount=cd['amount'])
        gift.category = PaymentCategory.objects.get(name=cd['category_name'])

        try:
            # Try charging the credit card
            charge = stripe.Charge.create(
                amount=int(cd['amount'] * 100),  # Convert dollars to cents
                currency='usd',
                source=cd['stripe_token'],
                description=str(gift.category)
            )
            gift.stripe_id = charge.id
        except stripe.error.CardError as card_error:
            # There was an error processing the credit card
            card_error = str(card_error)
            if 'Request req' in card_error:
                card_error = card_error.split(':', 1)[1].strip()
            response['errors']['gift_cc'] = [card_error]
        else:
            # Create the payment object and save it
            if cd['guest_id']:
                guest = Guest.objects.get(id=cd['guest_id'])
            else:
                guest = None
            if guest:
                payer = Payer.objects.filter(guest=guest).first()
                if not payer:
                    payer = Payer.objects.create(guest=guest)
            else:
                payer = Payer.objects.filter(
                    email=cd['email']).first()
                if payer:
                    payer.first_name = cd['first_name']
                    payer.last_name = cd['last_name']
                    payer.save()
                if not payer:
                    payer = Payer.objects.create(
                        first_name=cd['first_name'],
                        last_name=cd['last_name'],
                        email=cd['email'])
            gift.payer = payer
            gift.save()
    else:
        # The form is invalid
        response['errors'] = form.errors

    return JsonResponse(response)
