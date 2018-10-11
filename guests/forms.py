from django import forms
from .models import Guest, RSVP, Activity
from payments.models import Payment, PaymentCategory  # noqa
from pprint import pprint  # noqa


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
    guest_id = forms.IntegerField()
    stripe_token = forms.CharField(max_length=255, required=False)

    class Meta:
        model = RSVP
        fields = ['attending', 'nights_onsite', 'payment', 'message']

    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Select interesting activities in (if any)")

    guests = forms.ModelMultipleChoiceField(
        queryset=Guest.objects.all(),
        required=False,
        help_text='Select guests in RSVP')

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
            initial['guests'] = [
                g.pk for g in kwargs['instance'].guests.all()]
        forms.ModelForm.__init__(self, *args, **kwargs)

    def clean_attending(self):
        if 'attending' not in self.data:
            raise forms.ValidationError('Will you be attending?')
        return self.cleaned_data['attending']

    def clean_guests(self):
        guests = self.cleaned_data['guests']
        attending = self.data['attending']
        # If no guests were checked
        if not guests:
            # And the RSVP is attending
            if attending:
                # We need to know which guests are attending
                raise forms.ValidationError('Who will be attending?')
            # And the RSVP is declined
            else:
                # Nobody's coming; include all guests in party
                lead = Guest.objects.get(pk=self.data['guest_id'])
                guests = [guest for guest in lead.party()]
        return guests

    def clean(self):
        cd = super().clean()  # noqa
        if cd.get('attending') and cd.get('nights_onsite') is None:
            print(cd.get('attending'))
            print(cd.get('nights_onsite'))
            self.add_error(
                'nights_onsite',
                'How many nights (if any) do you plan to stay onsite?'
            )
        if (cd.get('attending') and cd.get('nights_onsite')
                and not cd.get('stripe_token')):
            self.add_error(
                'rsvp_cc',
                ('We need to pay the venue for your stay; '
                 'please fill out your credit card information'))

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
            # Associate Guests with RSVP
            instance.guests.clear()
            instance.guests.add(*self.cleaned_data['guests'])
        self.save_m2m = save_m2m

        # Only commit if commit == True
        if commit:
            instance.save()
            self.save_m2m()

        return instance
