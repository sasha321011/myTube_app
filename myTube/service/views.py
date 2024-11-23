from urllib import request
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
from service.models import (
    Video,
    UserVideoRelation,
    Comment,
    AuthorVideosList,
    PlaylistLike,
)
from service.serializers import (
    VideosSerializer,
    OneVideoSerializer,
    RatingCreateSerializer,
    CommentCreateSerializer,
    VideoCreateSerializer,
    CommentSerializer,
    AuthorVideosListSerializer,
    PlaylistLikeSerializer,
    ListAuthorVideosListSerializer,
)
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from service.utils import VideosFilter
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_delete


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = "page_size"
    max_page_size = 12


class VideosListView(mixins.ListModelMixin, GenericViewSet):
    """Список Video"""

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


class VideoDetailView(mixins.RetrieveModelMixin, GenericViewSet):
    """Конкретное Video"""

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
            "the_video": response.data["the_video"],
            "name": response.data["name"],
            "created_at": response.data["created_at"],
            "length_time": response.data["length_time"],
            "author": response.data["author"],
        }
        cache.set(cache_key, response.data, timeout=settings.CACHE_TTL)

        return response


class RatingCreateView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Создание/удаление лайка/дизлайка для видео"""

    serializer_class = RatingCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserVideoRelation.objects.all()


class CommentCreateView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Создание удаление изменение комментария под видео"""

    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()


class VideoCreateView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """Создание удаление изменение видео"""

    serializer_class = VideoCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()

    # def perform_destroy(self, instance):
    #     cache_key = f"video_details:{instance.slug}"
    #     cache.delete(cache_key)
    #     delete_old_file(instance.the_video.path)
    #     super().perform_destroy(instance)


class AuthorVideosView(mixins.ListModelMixin, GenericViewSet):
    """Видео конкретного автора"""

    queryset = Video.objects.prefetch_related("tags").select_related("author")
    serializer_class = VideosSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.kwargs.get("author")
        return super().get_queryset().filter(author__username=author)

    @method_decorator(cache_page(settings.CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RatedVideoView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = VideosSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Video.objects.filter(
                user_video_relations__user=self.request.user,
                user_video_relations__vote=1,
            )
            .select_related("author")
            .prefetch_related("tags")
        )


class MakeAuthorVideosListView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """Создание плейлистов видео автора"""
    permission_classes = [IsAuthenticated]
    serializer_class = AuthorVideosListSerializer


class PlaylistLikeViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet
):
    """Лайк/дизлайк плейлиста"""

    queryset = PlaylistLike.objects.all()
    serializer_class = PlaylistLikeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikedPlaylistsViewSet(mixins.ListModelMixin, GenericViewSet):
    """Вывод списка плейлистов, лайкнутых пользователем"""

    serializer_class = ListAuthorVideosListSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return AuthorVideosList.objects.filter(likes__user=self.request.user)


class AuthorPlaylistsViewSet(mixins.ListModelMixin, GenericViewSet):
    """Вывод плейлистов определенного автора"""

    serializer_class = ListAuthorVideosListSerializer

    def get_queryset(self):
        author_username = self.kwargs.get("author")
        return AuthorVideosList.objects.filter(author__username=author_username)


class PlaylistVideosViewSet(ReadOnlyModelViewSet):
    """Список видео из определенного плейлиста"""

    serializer_class = VideosSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        return Video.objects.filter(video_lst__slug=slug)
