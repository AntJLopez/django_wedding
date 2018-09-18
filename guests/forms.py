from django.forms import ModelForm
from .models import Guest


class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = [
            'first_name',
            'last_name',
            'percentile',
            'likelihood',
            'family',
            'email',
            'phone',
            'lead_partner',
            'parent',
            'birthday',
            'username',
            'language',
            'country',
            'administrative_area',
            'sub_administrative_area',
            'locality',
            'dependent_locality',
            'postal_code',
            'thoroughfare',
            'premise',
            'sub_premise',
            'notes',
        ]
