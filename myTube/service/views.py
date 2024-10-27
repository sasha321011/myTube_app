from cgitb import lookup
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
    VideoCreateSerializer,
    CommentSerializer,
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from service.utils import VideosFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12


# http://127.0.0.1:8000/api/video/?tags=1&tags=2&author=1
# дублирующиеся запросы
class VideosViewSet(ModelViewSet):
    queryset = (
        Video.objects.all()
        .prefetch_related("tags")
        .select_related("author")
        .only("id", "name", "slug", "created_at", "length_time", "pre_view", "author")
        .distinct()
    )
    serializer_class = VideosSerializer
    pagination_class = StandardResultsSetPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    filterset_class = VideosFilter
    search_fields = ["^name", "^author"]
    ordering_fields = ["created_at", "length_time"]

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Метод создания не разрешен."})


class VideoDetailViewSet(ViewSet):
    lookup_field = "slug"

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
            )
            .first()
        )
        serializer = OneVideoSerializer(queryset)
        return Response(serializer.data)


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
    serializer_class = VideoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class AuthorVideosViewSet(ViewSet):
    lookup_field = "author"
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, author=None):
        queryset = (
            Video.objects.filter(author=author)
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
