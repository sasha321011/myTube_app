
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from service.models import Video
from clients.models import Subscription

@shared_task
def send_messages_for_subs(video_id):
    video = Video.objects.get(id=video_id)
    author = video.author
    

    subscribers = Subscription.objects.filter(channel=author).select_related('subscriber')

    for subscription in subscribers:
        subscriber = subscription.subscriber
        send_mail(
            subject=f"Новое видео от {author.username}",
            message=f"{author.username} загрузил новое видео: {video.name}. Смотрите его по ссылке: {video.get_absolute_url()}",
            from_email="noreply@yourdomain.com",
            recipient_list=[subscriber.email],
        )
