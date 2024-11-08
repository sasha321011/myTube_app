from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from service.tasks import send_messages_for_subs  

@receiver(post_save, sender=Video)
def notify_subscribers_on_new_video(sender, instance, created, **kwargs):
    if created:
        send_messages_for_subs.delay(instance.id)
