from rest_framework import serializers
from service.models import Video, Comment, UserVideoRelation, TagPost


class FilterCommentListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="user_comment.username")
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "author_name", "children", "text")


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPost
        fields = ("id", "tag_name", "tag_slug")


class VideosSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username")
    tags_name = TagsSerializer(many=True, read_only=True, source="tags")

    class Meta:
        model = Video
        fields = (
            "name",
            "slug",
            "created_at",
            "length_time",
            "pre_view",
            "author",
            "author_name",
            "tags_name",
        )


class OneVideoSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username")
    # email = serializers.CharField(source='author.email')
    comments = CommentSerializer(many=True, read_only=True, source="vid_com")
    tags_name = TagsSerializer(many=True, read_only=True, source="tags")

    class Meta:
        model = Video
        fields = (
            "id",
            "name",
            "created_at",
            "tags_name",
            "length_time",
            "author",
            "author_name",
            "comments",
        )


class RatingCreateSerializer(serializers.ModelSerializer):
    vid = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

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


class CommentCreaetSerializer(serializers.ModelSerializer):

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
    
class VideoCreaetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("name","slug","length_time","pre_view","tags","description")

    def create(self, validated_data):
        author = self.context["request"].user
        name = validated_data["name"]
        slug = validated_data["slug"]
        length_time = validated_data["length_time"]
        pre_view = validated_data["pre_view"]
        tags = validated_data.pop("tags", [])
        description = validated_data["description"]

        author_video, created = Video.objects.update_or_create(
            author=author,
            name=name,
            length_time=length_time,
            slug=slug,
            pre_view=pre_view,
            description = description,
        )
        author_video.tags.set(tags)
        return author_video