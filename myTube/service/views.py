from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet, ModelViewSet
from rest_framework.response import Response

from service.models import Video
from service.serializers import (
    VideosSerializer,
    OneVideoSerializer,
    RatingCreateSerializer,
    CommentCreaetSerializer,
    VideoCreaetSerializer
)


class VideosViewSet(ViewSet):
    def list(self, request):
        queryset = (
            Video.objects.all()
            .prefetch_related("tags")
            .select_related("author")
            .only(
                "id", "name", "slug", "created_at", "length_time", "pre_view", "author"
            )
        )
        serializer = VideosSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = (
            Video.objects.filter(slug=slug)
            .prefetch_related("tags", "vid_com__children")
            .select_related("author")
            .only("id", "name", "created_at", "length_time", "author")
        )
        serializer = OneVideoSerializer(queryset, many=True)
        return Response(serializer.data)


class RatingCreateViewSet(ModelViewSet):
    serializer_class = RatingCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


class CommentCreateViewSet(ModelViewSet):
    serializer_class = CommentCreaetSerializer

    def perform_create(self, serializer):
        serializer.save()

class VideoCreateViewSet(ModelViewSet):
    serializer_class = VideoCreaetSerializer

    def perform_create(self, serializer):
        serializer.save()
