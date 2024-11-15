from django.db.models import Count, Q
from rest_framework.response import Response
from rest_framework.viewsets import (
    ViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from service.models import Video, UserVideoRelation, Comment
from service.serializers import (
    VideosSerializer,
    OneVideoSerializer,
    RatingCreateSerializer,
    CommentCreateSerializer,
    VideoCreateSerializer,
    CommentSerializer,
)
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from service.utils import VideosFilter
from django.core.cache import cache
from service.models import delete_old_file

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12


class VideosListViewSet(mixins.ListModelMixin, GenericViewSet):
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
    search_fields = ["^name", "^author__username"]
    ordering_fields = ["created_at", "length_time"]

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class VideoDetailViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    lookup_field = "slug"
    serializer_class = OneVideoSerializer
    queryset = (
        Video.objects.select_related("author")
        .prefetch_related("tags", "vid_com__user_comment", "vid_com__children")
        .only(
            "id",
            "the_video",
            "name",
            "created_at",
            "length_time",
            "author",
        )
    )

    def get_queryset(self):
        total_votes_vid = self.queryset.annotate(
            likes=Count(
                "user_video_relations",
                filter=Q(user_video_relations__vote=UserVideoRelation.LIKE),
            ),
            dislikes=Count(
                "user_video_relations",
                filter=Q(user_video_relations__vote=UserVideoRelation.DISLIKE),
            ),
        )
        return total_votes_vid

    def retrieve(self, request, *args, **kwargs):
        video_slug = self.kwargs.get(self.lookup_field)
        cache_key = f"video_details:{video_slug}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        response = super().retrieve(request, *args, **kwargs)
        cached_data = {
            "id": response.data["id"],
            "the_video":response.data['the_video'],
            "name": response.data["name"],
            "created_at": response.data["created_at"],
            "length_time": response.data["length_time"],
            "author": response.data["author"],
        }
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)

        return response


class RatingCreateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = RatingCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserVideoRelation.objects.all()


class CommentCreateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


class VideoCreateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = VideoCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()

    def perform_destroy(self, instance):
        delete_old_file(instance.the_video.path)
        super().perform_destroy(instance)

class AuthorVideosViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Video.objects.prefetch_related("tags").select_related("author")
    serializer_class = VideosSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.kwargs.get("author")
        return super().get_queryset().filter(author__username=author)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
