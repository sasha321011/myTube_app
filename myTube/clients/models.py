from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='clients_user_set',
        blank=True,
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='clients_user_permissions_set',
        blank=True,
        verbose_name='user permissions'
    )


    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True
                              , verbose_name='Фотография')
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name='Дата рождения')



class Subscription(models.Model):
    subscriber = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscriptions')
    channel = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='subscribers')
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('subscriber', 'channel')