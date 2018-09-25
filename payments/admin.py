from django.contrib import admin
from .models import PaymentCategory, Payer, Payment


@admin.register(PaymentCategory)
class PaymentCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payer', 'amount', 'category', 'stripe_id')
