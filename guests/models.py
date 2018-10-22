from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from decimal import Decimal


INVITED_THRESHOLD = Decimal('0.40')


class Activity(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Activities'


class RSVP(models.Model):
    def __str__(self):
        leader = self.guests.first()
        if leader and str(leader):
            # Return the name of the leader of the party
            return str(leader)
        # If there is no named guest, name it by the date and time
        d = self.created
        ampm = 'pm' if d.hour >= 12 else 'am'
        return f'{d:%b} {d.day}, {d.hour}:{d:%M} {ampm}'

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    attending = models.BooleanField()
    attending_kuwait = models.BooleanField(default=False)
    nights_onsite = models.PositiveSmallIntegerField(blank=True, default=0)
    activities = models.ManyToManyField(Activity, related_name='groups')
    payment = models.ForeignKey(
        'payments.Payment', blank=True, null=True, on_delete=models.SET_NULL)
    message = models.TextField(blank=True, default='')

    class Meta:
        verbose_name = 'RSVP'


class GuestQuerySet(models.QuerySet):
    def leads(self):
        return self.filter(lead_partner=None, parent=None)

    def invited(self):
        return self.filter(percentile__gte=INVITED_THRESHOLD)


class Guest(models.Model):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def unnamed(self):
        # Returns True if guest has no name, False if they do
        return not bool(str(self))

    def is_lead(self):
        return not self.lead_partner and not self.parent
    is_lead.boolean = True
    is_lead.short_description = 'Group Lead'

    def invited(self):
        return self.percentile >= INVITED_THRESHOLD
    invited.boolean = True

    def age(self):
        if self.birthday:
            delta = date.today() - self.birthday
            years = int(delta.days / 365.25)
            return years
        else:
            return None

    def party(self):
        party = []
        if self.lead_partner:
            # This person has a lead partner, so make them first then self
            party.append(self.lead_partner)
            party.append(self)
        elif self.parent:
            # This person has a parent, so make them first
            party.append(self.parent)
        else:
            # This person has no senior, so make self first
            party.append(self)
            # Add partner(s) if present
            for partner in self.partners.all().order_by('first_name'):
                party.append(partner)
        # Add all the children to the party, ordered by age then name
        for child in party[0].children.all().order_by(
                'birthday', 'first_name'):
            party.append(child)
        return [guest for guest in party if guest.invited()]

    def address(self):
        if self.country == 'US':
            lines = []
            lines.append(self.thoroughfare)
            if self.premise:
                lines.append(self.premise)
            line = (f'{self.locality}, {self.administrative_area} ')
            line += self.postal_code
            lines.append(line)
            return lines
        return None

    def party_line(self, max_line_length=28):
        party = len(self.party())

        if party == 1:
            return str(self)
        elif party == 2:
            plus_one = self.party()[1]
            if plus_one.unnamed():
                line = f'{self} & Guest'
                if len(line) > max_line_length:
                    line = f'{self.first_name} & Guest'
                return line
            elif self.last_name == plus_one.last_name:
                first_names = f'{self.first_name} & {plus_one.first_name}'
                line = f'{first_names} {self.last_name}'
                if len(line) > max_line_length:
                    line = first_names
                return line
            else:
                line = f'{self} & {plus_one}'
                if len(line) > max_line_length:
                    line = f'{self} & {plus_one.first_name}'
                if len(line) > max_line_length:
                    line = f'{self.first_name} & {plus_one.first_name}'
                if len(line) > max_line_length:
                    line = f'{self.first_name} & Guest'
                return line
        else:
            line = f'{self.first_name}, '
            plus_one = self.party()[1]
            line += 'Guest' if plus_one.unnamed() else plus_one.first_name
            line += ' & Family'
            if len(line) > max_line_length:
                line = f'{self.first_name} & Family'
            return line

    username = models.SlugField(blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True, max_length=200)
    lead_partner = models.ForeignKey(
        'self',
        blank=True,
        related_name='partners',
        null=True,
        on_delete=models.SET_NULL)
    parent = models.ForeignKey(
        'self',
        blank=True,
        related_name='children',
        null=True,
        on_delete=models.SET_NULL)
    birthday = models.DateField(blank=True, null=True)
    percentile = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=2)
    likelihood = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=2)
    rsvp = models.ForeignKey(
        RSVP, blank=True, null=True, related_name='guests',
        on_delete=models.SET_NULL)
    family = models.PositiveSmallIntegerField(
        default=3,
        choices=(
            (1, 'Bride'),
            (2, 'Groom'),
            (3, 'Friend'),
        ))
    language = models.CharField(
        default='en',
        max_length=2,
        choices=(
            ('en', 'English'),
            ('es', 'Spanish'),
            ('ar', 'Arabic'),
        ))
    first_name = models.CharField(blank=True, max_length=40)
    last_name = models.CharField(blank=True, max_length=40)
    kuwait_invite = models.BooleanField(default=False)
    country = CountryField(blank=True)
    administrative_area = models.CharField(
        'state',
        blank=True,
        max_length=60)
    sub_administrative_area = models.CharField(
        'county',
        blank=True,
        max_length=60)
    locality = models.CharField(
        'city',
        blank=True,
        max_length=60)
    dependent_locality = models.CharField(
        'neighborhood',
        blank=True,
        max_length=60)
    postal_code = models.CharField(blank=True, max_length=20)
    thoroughfare = models.CharField(
        'street address',
        blank=True,
        max_length=60)
    premise = models.CharField(
        'apartment/box',
        blank=True,
        max_length=60)
    sub_premise = models.CharField(
        'room',
        blank=True,
        max_length=60)
    notes = models.TextField(blank=True)

    # Model managers, for filtering queries
    objects = GuestQuerySet.as_manager()
