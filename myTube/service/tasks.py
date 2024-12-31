from celery import shared_task
from django.core.mail import send_mail
from service.models import Video
from clients.models import Subscription

import os
from django.conf import settings
from service.models import Video

@shared_task
def send_messages_for_subs(video_id):
    '''Задача для рассылки писем на почту о новом Video'''
    video = Video.objects.get(id=video_id)
    author = video.author

    subscribers = Subscription.objects.filter(channel=author).select_related(
        "subscriber"
    )

    for subscription in subscribers:
        subscriber = subscription.subscriber
        send_mail(
            subject=f"Новое видео от {author.username}",
            message=f"{author.username} загрузил новое видео: {video.name}.",
            from_email="noreply@yourdomain.com",
            recipient_list=[subscriber.email],
        )


@shared_task
def process_video_upload(video_id, filename, file_content):
    """Обработка загрузки видео"""
    video = Video.objects.get(id=video_id)


    upload_path = os.path.join(settings.MEDIA_ROOT, f"videos/{filename}")

    with open(upload_path, "wb") as f:
        f.write(file_content)

    video.the_video.name = f"videos/{filename}"
    video.save()
