from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
    ViewSet,
    ModelViewSet,
    GenericViewSet,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import mixins
from service.models import Video, UserVideoRelation
from service.serializers import (
    VideosSerializer,
    OneVideoSerializer,
    RatingCreateSerializer,
    CommentCreateSerializer,
    VideoCreaetSerializer,
    CommentSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12


class VideosViewSet(ViewSet):
    pagination_class = StandardResultsSetPagination
    lookup_field = "slug"

    def list(self, request):
        queryset = (
            Video.objects.all()
            .prefetch_related("tags")
            .select_related("author")
            .only(
                "id", "name", "slug", "created_at", "length_time", "pre_view", "author"
            )
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = VideosSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = VideosSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        queryset = (
            Video.objects.filter(slug=slug)
            .prefetch_related("tags", "vid_com__user_comment", "vid_com__children")
            .select_related("author")
            .annotate(
                likes=Count(
                    "user_video_relations",
                    filter=Q(user_video_relations__vote=UserVideoRelation.LIKE),
                ),
                dislikes=Count(
                    "user_video_relations",
                    filter=Q(user_video_relations__vote=UserVideoRelation.DISLIKE),
                ),
            ).first()
        )
        response_data = OneVideoSerializer(queryset)
        return Response(response_data.data)

class RatingCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = RatingCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class CommentCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class VideoCreateViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = VideoCreaetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
