# Generated by Django 2.1 on 2018-09-25 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentcategory',
            options={'verbose_name': 'Payment Category', 'verbose_name_plural': 'Payment Categories'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
