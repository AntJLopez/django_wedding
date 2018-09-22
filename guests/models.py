from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date


class Guest(models.Model):
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        if self.birthday:
            delta = date.today() - self.birthday
            years = int(delta.days / 365.25)
            return years
        else:
            return ''

    username = models.SlugField(blank=True, null=True)
    phone = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True, max_length=200)
    lead_partner = models.ForeignKey(
        'self',
        blank=True,
        related_name='partner',
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
