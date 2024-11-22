from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from django.contrib.auth import get_user_model


@receiver(post_delete, sender=get_user_model())
def delete_user_avatar(sender, instance, **kwargs):
    '''Сигнал для удаление аватарки пользователя при удалении пользователя'''
    try:
        if instance.photo:
            photo_path = instance.photo.path
            if os.path.isfile(photo_path):
                os.remove(photo_path)
    except Exception as e:
        pass
