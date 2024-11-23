from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel
from django.urls import reverse
from django.core.validators import FileExtensionValidator


def get_path_upload_video(instance, file):
    '''Путь для сохранения видео'''
    return f"videos/{file}"


class Video(models.Model):
    '''Модель видео'''
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="videos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    length_time = models.PositiveIntegerField(blank=True)
    pre_view = models.ImageField(blank=True, null=True)

    the_video = models.FileField(
        upload_to=get_path_upload_video,
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "avi"])],
        blank=True,
    )
    tags = models.ManyToManyField(
        "TagPost", blank=True, related_name="video_tags", verbose_name="Теги"
    )
    description = models.TextField(blank=True)

    # def delete(self, *args, **kwargs):
    #     if self.the_video:
    #         delete_old_file(self.the_video.path)
    #     super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("video-detail", kwargs={"slug": self.slug})


class TagPost(models.Model):
    '''Модель тегов к видео'''
    tag_name = models.CharField(max_length=50)
    tag_slug = models.SlugField(unique=True)


class Comment(MPTTModel, models.Model):
    '''Модель комментариев для создания комментариев под видео'''
    video_comment = models.ForeignKey(
        Video, related_name="vid_com", on_delete=models.CASCADE
    )
    user_comment = models.ForeignKey(
        get_user_model(), related_name="user_com", on_delete=models.CASCADE
    )

    text = models.TextField(max_length=300)
    parent = models.ForeignKey(
        "self", related_name="children", null=True, blank=True, on_delete=models.PROTECT
    )


class UserVideoRelation(models.Model):
    '''Модель для создания лайков/дизлайков под видео'''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    vid = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="user_video_relations"
    )

    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
    ]

    vote = models.SmallIntegerField(choices=VOTE_CHOICES, null=True)


class AuthorVideosList(models.Model):
    '''Модель для создания плейлиста дял автора'''
    vids = models.ManyToManyField(Video, related_name="video_lst")
    name = models.CharField(max_length=100)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name="user_video_lst")
    slug=models.SlugField(unique=True,blank=True,null=True)
    # def save(self, *args, **kwargs):
    #     # Генерация slug, если он пустой
    #     if not self.slug:
    #         # Генерируем slug из названия
    #         self.slug = slugify(self.name)
    #         # Добавляем случайную строку для уникальности, если slug уже существует
    #         while AuthorVideosList.objects.filter(slug=self.slug).exists():
    #             random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    #             self.slug = f"{slugify(self.name)}-{random_string}"

    #     super().save(*args, **kwargs)


class PlaylistLike(models.Model):
    """Модель для лайков плейлистов"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    playlist = models.ForeignKey(AuthorVideosList, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "playlist")
