from django import forms
from django.core.exceptions import ValidationError  # noqa
from .models import Guest, RSVP, Activity
from payments.models import Payment, PaymentCategory  # noqa


class GuestForm(forms.ModelForm):
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


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['attending', 'attending_kuwait', 'nights_onsite', 'payment']

    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all())

    def __init__(self, *args, **kwargs):
        # Only if the form is built from an instance
        # Otherwise, 'activities' list should be empty
        if kwargs.get('instance'):
            # Get the 'initial' keyword argument, or initialize it as a dict
            # if it didn't exist
            initial = kwargs.setdefault('initial', {})
            # The widget for a ModelMultipleChoiceField expects a list of
            # primary keys for the selected activities
            initial['activities'] = [
                a.pk for a in kwargs['instance'].activities.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        # Get the unsaved Activity instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # Associate RSVP with activities
            instance.activities.clear()
            instance.activities.add(*self.cleaned_data['activities'])
        self.save_m2m = save_m2m

        # Only commit if commit == True
        if commit:
            instance.save()
            self.save_m2m()

        return instance
