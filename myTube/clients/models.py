from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from django.core.validators import FileExtensionValidator




class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group", related_name="clients_user_set", blank=True, verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="clients_user_permissions_set",
        blank=True,
        verbose_name="user permissions",
    )

    date_birth = models.DateTimeField(blank=True,
        verbose_name="Дата рождения"
    )
    

class Subscription(models.Model):
    subscriber = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscribers"
    )
    channel = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="channels"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("subscriber", "channel")
