from django.http import JsonResponse
from django.views.decorators.http import require_POST
from pprint import pprint  # noqa
from .forms import GiftForm
from .models import Payment, PaymentCategory, Payer
from guests.models import Guest


@require_POST
def make_gift(request):
    form = GiftForm(request.POST)
    response = {'errors': []}
    if form.is_valid():
        print('The form is valid!')
        cd = form.cleaned_data
        gift = Payment(amount=cd['amount'])
        gift.category = PaymentCategory.objects.get(id=cd['category_id'])
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
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                email=cd['email']).first()
            if not payer:
                payer = Payer.objects.create(
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    email=cd['email'])
        gift.payer = payer
        gift.save()
    else:
        # The form is invalid
        print('The form is invalid!')
        response['errors'] = form.errors
        # pprint(response['errors'])

    return JsonResponse(response)
