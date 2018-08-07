# Generated by Django 2.0.7 on 2018-08-05 04:27

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='likelihood',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='guest',
            name='percentile',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=2),
        ),
        migrations.AlterField(
            model_name='guest',
            name='administrative_area',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
        migrations.AlterField(
            model_name='guest',
            name='dependent_locality',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.EmailField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='guest',
            name='family',
            field=models.CharField(blank=True, choices=[('Tony', 'Tony'), ('Haya', 'Haya'), ('Friend', 'Friend')], max_length=6),
        ),
        migrations.AlterField(
            model_name='guest',
            name='first_name',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='guest',
            name='language',
            field=models.CharField(blank=True, choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish')], max_length=2),
        ),
        migrations.AlterField(
            model_name='guest',
            name='last_name',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='guest',
            name='lead_partner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partner', to='guests.Guest'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='locality',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='guests.Guest'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='phone',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='guest',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='guest',
            name='premise',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='sub_administrative_area',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='sub_premise',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='thoroughfare',
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AlterField(
            model_name='guest',
            name='username',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
