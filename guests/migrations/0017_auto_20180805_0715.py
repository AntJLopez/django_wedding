# Generated by Django 2.1 on 2018-08-05 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0016_auto_20180805_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='administrative_area',
            field=models.CharField(blank=True, max_length=60, verbose_name='state'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='dependent_locality',
            field=models.CharField(blank=True, max_length=60, verbose_name='neighborhood'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='family',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Bride'), (2, 'Groom'), (3, 'Friend')]),
        ),
        migrations.AlterField(
            model_name='guest',
            name='locality',
            field=models.CharField(blank=True, max_length=60, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='premise',
            field=models.CharField(blank=True, max_length=60, verbose_name='apartment/box'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='sub_administrative_area',
            field=models.CharField(blank=True, max_length=60, verbose_name='county'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='sub_premise',
            field=models.CharField(blank=True, max_length=60, verbose_name='room'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='thoroughfare',
            field=models.CharField(blank=True, max_length=60, verbose_name='street address'),
        ),
    ]
