from rest_framework import serializers
from service.models import Video, Comment, UserVideoRelation


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


class VideosSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username")
    # email = serializers.CharField(source='author.email')
    # comments = CommentSerializer(many=True, read_only=True, source="vid_com")

    class Meta:
        model = Video
        fields = (
            "name",
            "slug",
            "created_at",
            "tags",
            "length_time",
            "pre_view",
            "author",
            "author_name",
        )


class OneVideoSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username")
    # email = serializers.CharField(source='author.email')
    comments = CommentSerializer(many=True, read_only=True, source="vid_com")

    class Meta:
        model = Video
        fields = (
            "id",
            "name",
            "created_at",
            "tags",
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
