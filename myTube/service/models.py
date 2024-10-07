from django.contrib.auth import get_user_model
from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    length_time = models.PositiveIntegerField(blank=True)
    pre_view = models.ImageField(blank=True)
    #the_video = video
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    description = models.TextField(blank=True)

    #likes
    #comments
    #subscription
    #вынести эти 3 коспонента в отдельное приложение

class TagPost(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_slug = models.SlugField()