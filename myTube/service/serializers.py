from urllib import request
from rest_framework import serializers
from service.models import Video, Comment, TagPost, UserVideoRelation, AuthorVideosList, PlaylistLike
import uuid
from django.db.models import Count, Q
from django.utils.text import slugify

def slug_create(name):
    '''Генерация слага для видео'''
    existing_slugs = Video.objects.values_list("slug", flat=True)

    while True:
        new_slug = str(uuid.uuid4())

        if new_slug not in existing_slugs:
            return new_slug


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для отображения комментариев под видео'''
    author_name = serializers.CharField(source="user_comment.username")


    class Meta:
      
        model = Comment
        fields = ("id", "author_name", "text", "parent")

    # def get_children(self, obj):
    #     # Дочерние комментарии загружаются с помощью prefetch_related
    #     children_comments = obj.children.all()
    #     # Используем множество для хранения уникальных идентификаторов
    #     unique_ids = set()
    #     filtered_children = []

    #     for child in children_comments:
    #         if child.id not in unique_ids:
    #             unique_ids.add(child.id)
    #             filtered_children.append(child)

    #     return CommentSerializer(filtered_children, many=True).data


class TagsSerializer(serializers.ModelSerializer):
    '''Сериализатор тегов'''
    class Meta:
        model = TagPost
        fields = ("id", "tag_name", "tag_slug")


class VideosSerializer(serializers.ModelSerializer):
    '''Сериализатор списка видео'''
    author_name = serializers.CharField(source="author.username")
    tags_name = TagsSerializer(many=True, read_only=True, source="tags")
    url = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            "name",
            "url",

            "created_at",
            "length_time",
            "pre_view",
            "author",
            "author_name",
            "tags_name",
            "cats",
        )

    def get_url(self, obj):
        return obj.get_absolute_url()


class OneVideoSerializer(serializers.ModelSerializer):
    '''Сериализатор конкретного видео'''
    author_name = serializers.CharField(source="author.username")
    # email = serializers.CharField(source='author.email')
    comments = CommentSerializer(many=True, read_only=True, source="vid_com")
    tags_name = TagsSerializer(many=True, read_only=True, source="tags")
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Video
        fields = (
            "id",
            "name",
            "the_video",
            "created_at",
            "tags_name",
            "length_time",
            "author",
            "author_name",
            "comments",
            "likes",
            "dislikes",
            "description",
            "cats",
        )


class RatingCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для лайков/дизлайков под видео'''
    vid = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())
    vote = serializers.ChoiceField(choices=[(1, 'Like'), (-1, 'Dislike')])

    class Meta:
        model = UserVideoRelation
        fields = ("vid", "vote")

    def create(self, validated_data):
        user = self.context["request"].user
        video = validated_data["vid"]
        vote = validated_data["vote"]

        rate, created = UserVideoRelation.objects.update_or_create(
            user=user, vid=video, defaults={"vote": vote}
        )
        return rate


class CommentCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания комментариев'''
    class Meta:
        model = Comment
        fields = ("id", "parent", "text", "video_comment")

    def create(self, validated_data):
        user = self.context["request"].user
        parent = validated_data["parent"]
        text = validated_data["text"]
        video_comment = validated_data["video_comment"]

        com, created = Comment.objects.update_or_create(
            user_comment=user, parent=parent, video_comment=video_comment, text=text
        )
        return com


class VideoCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания видео'''
    tags = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )
    
    class Meta:
        model = Video
        fields = ("name", "the_video", "length_time", "pre_view", "tags", "description","cats")



    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        author = self.context["request"].user

        video = Video.objects.create(
            author=author,
            name=validated_data.get("name"),
            slug=slug_create(validated_data.get("name")),
            length_time=validated_data.get("length_time", 0),
            pre_view=validated_data.get("pre_view"),
            description=validated_data.get("description", ""),
            the_video=validated_data.get("the_video"),
            cats=validated_data.get("cats")
        )

        print("Validated data:", validated_data)
        video.tags.set(tags_data)

        return video






    # def create(self, validated_data):
    #     author = self.context["request"].user
    #     name = validated_data["name"]
    #     # slug = validated_data["slug"]
    #     length_time = validated_data["length_time"]
    #     pre_view = validated_data["pre_view"]
    #     tags = validated_data.pop("tags", [])
    #     description = validated_data["description"]
    #     the_video = validated_data["the_video"]
    #     author_video, created = Video.objects.update_or_create(
    #         author=author,
    #         name=name,
    #         length_time=length_time,
    #         slug=slug_create(name),
    #         pre_view=pre_view,
    #         description=description,
    #         the_video=the_video,
    #     )
    #     author_video.tags.set(tags)
    #     return author_video


class AuthorVideosListSerializer(serializers.ModelSerializer):
    vids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Video.objects.all()
    )
    class Meta:
        model = AuthorVideosList
        fields = ("id", "name", "vids", "slug")

    def validate_vids(self, vids):
        """Проверяем, что все видео принадлежат текущему пользователю."""
        user = self.context["request"].user
        for video in vids:
            if video.author != user:
                raise serializers.ValidationError(
                    f"Видео {video.name} не принадлежит вам."
                )
        return vids

    def create(self, validated_data):
        user = self.context["request"].user  # Получаем текущего пользователя
        name = validated_data.get('name')
        slug = slugify(name)
        vids = validated_data.pop("vids", [])  # Исправлено на "vids"
        author_videos_list = AuthorVideosList.objects.create(
            author=user,  # Присваиваем текущего пользователя полю author
            **validated_data
        )
        author_videos_list.vids.set(vids)
        return author_videos_list

    def update(self, instance, validated_data):
        user = self.context["request"].user  # Получаем текущего пользователя
        vids = validated_data.pop("vids", [])  # Исправлено на "vids"
        instance.name = validated_data.get("name", instance.name)
        instance.vids.set(vids)  # set() используется для обновления ManyToMany
        instance.author = user  # Обновляем поле author, если нужно
        instance.save()
        return instance


class PlaylistLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistLike
        fields = ("playlist",)

    def validate_playlist(self, playlist):
        user = self.context["request"].user
        if PlaylistLike.objects.filter(user=user, playlist=playlist).exists():
            raise serializers.ValidationError("Вы уже лайкнули этот плейлист.")
        return playlist

class ListAuthorVideosListSerializer(serializers.ModelSerializer):
    #vids = VideosSerializer(many=True)

    class Meta:
        model = AuthorVideosList
        fields = ("id", "name","vids","slug")


