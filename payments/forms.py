from django import forms
from django.core.exceptions import ValidationError
from guests.models import Guest
from .models import PaymentCategory


class GiftForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    category_name = forms.CharField(max_length=40)
    guest_id = forms.IntegerField(required=False)
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    email = forms.EmailField(max_length=200, required=False)
    stripe_token = forms.CharField(max_length=255, required=False)

    def clean_category_name(self):
        category_name = self.cleaned_data['category_name']
        if category_name:
            category = PaymentCategory.objects.filter(
                name=category_name).first()
            if not (category and category.is_gift()):
                raise ValidationError('Not a valid gift category name')
        return category_name

    def clean_guest_id(self):
        guest_id = self.cleaned_data['guest_id']
        if guest_id:
            guest = Guest.objects.filter(id=guest_id).first()
            if not guest:
                raise ValidationError('Not a valid guest ID')
        return guest_id

    def clean(self):
        cd = super().clean()
        if not cd.get('guest_id'):
            if not cd.get('first_name'):
                self.add_error('first_name', "What's your first name?")
            if not cd.get('last_name'):
                self.add_error('last_name', "What's your last name?")
            if not cd.get('email'):
                self.add_error(
                    'email',
                    'Please give us your email address so we can thank you!'
                )
