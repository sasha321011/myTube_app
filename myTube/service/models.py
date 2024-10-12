from django.contrib.auth import get_user_model
from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    length_time = models.PositiveIntegerField(blank=True)
    pre_view = models.ImageField(blank=True)

    #the_video = video
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='Теги')
    description = models.TextField(blank=True)

    @property
    def total_likes(self):
        return self.uservideorelation_set.filter(vote=UserVideoRelation.LIKE).count()

    @property
    def total_dislikes(self):
        return self.uservideorelation_set.filter(vote=UserVideoRelation.DISLIKE).count()


class TagPost(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_slug = models.SlugField(unique=True)


class Comment(models.Model):
    video_comment = models.ForeignKey(Video,related_name='vid_com',on_delete=models.CASCADE)
    user_comment = models.ForeignKey(get_user_model(),related_name='user_com',on_delete=models.CASCADE)

    text = models.TextField(max_length=300)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

class UserVideoRelation(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    vid = models.ForeignKey(Video, on_delete=models.CASCADE)

    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    vote = models.SmallIntegerField(choices=VOTE_CHOICES, null=True)
