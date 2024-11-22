from service.tasks import send_messages_for_subs
import os
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.core.cache import cache
from service.models import Video


@receiver(post_save, sender=Video)
def notify_subscribers_on_new_video(sender, instance, created, **kwargs):
    '''Сигнал для оповещения подписанных пользователей на почте о создании нового Video'''
    if created:
        send_messages_for_subs.delay(instance.id)


@receiver(post_delete, sender=Video)
def clear_cache_and_delete_files_on_delete(sender, instance, **kwargs):
    '''Сигнал для очистки кеша при удалении Video'''
    cache_key = f"video_details:{instance.slug}"
    cache.delete(cache_key)

    if instance.the_video and os.path.exists(instance.the_video.path):
        os.remove(instance.the_video.path)


@receiver(pre_save, sender=Video)
def delete_old_file_on_update(sender, instance, **kwargs):
    '''Удаление старого файла при обновлении объекта Video'''
    if not instance.pk:
        return

    try:
        old_instance = Video.objects.get(pk=instance.pk)
    except Video.DoesNotExist:
        return

    if old_instance.the_video != instance.the_video:
        if os.path.exists(old_instance.the_video.path):
            os.remove(old_instance.the_video.path)
