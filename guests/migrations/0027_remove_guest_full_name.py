# Generated by Django 2.1 on 2018-09-18 03:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0026_auto_20180917_2321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='full_name',
        ),
    ]
