from django.db import models


class Profile(models.Model):
    picture = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=30)
    category = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Couple'),
            (2, 'Bridal Party'),
            (3, 'Family'),
        ))
    description = models.TextField()
