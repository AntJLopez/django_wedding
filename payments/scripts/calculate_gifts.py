from payments.models import Payment, PaymentCategory
from django.db.models import Sum


def run():
    for category in PaymentCategory.objects.all():
        filtered_payments = Payment.objects.filter(category=category)
        total = filtered_payments.aggregate(Sum('amount'))['amount__sum']
        print(f'{category}: ${total:,.2f}')
