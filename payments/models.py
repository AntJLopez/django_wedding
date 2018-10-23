from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PaymentCategory(models.Model):
    def __str__(self):
        if self.parent:
            return f'{str(self.parent)} : {self.name}'
        return self.name

    def has_subcategory(self):
        child = PaymentCategory.objects.filter(parent=self).first()
        return bool(child)

    def is_gift(self):
        if str(self) == 'Gift':
            return True
        if self.parent:
            return self.parent.is_gift()
        return False

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Payment Category'
        verbose_name_plural = 'Payment Categories'


class Payer(models.Model):
    def __str__(self):
        if self.guest:
            return f'{self.guest.first_name} {self.guest.last_name}'
        return f'{self.first_name} {self.last_name}'

    guest = models.ForeignKey(
        'guests.Guest', null=True, blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(blank=True, max_length=40)
    last_name = models.CharField(blank=True, max_length=40)
    email = email = models.EmailField(blank=True, max_length=200)

    def clean(self):
        named_guest = bool(self.guest)
        contact_info = bool(self.first_name and self.last_name and self.email)
        if not (named_guest or contact_info):
            raise ValidationError(_(
                'We need either a named guest or full contact information'))


class Payment(models.Model):
    def __str__(self):
        return f'{self.created:%Y-%m-%d} – ${self.amount} – {self.payer}'

    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(
        PaymentCategory, null=True, on_delete=models.SET_NULL)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)
    stripe_id = models.CharField(blank=True, max_length=255)
