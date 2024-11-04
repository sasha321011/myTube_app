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
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from service.utils import VideosFilter


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
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    # Настройки фильтрации, сортировки и поиска
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = VideosFilter
    search_fields = ["^name", "^author__username"]
    ordering_fields = ["created_at", "length_time"]


# class VideosViewSet(ReadOnlyModelViewSet):
#     queryset = (
#         Video.objects.all()
#         .prefetch_related("tags")
#         .select_related("author")
#         .only("id", "name", "slug", "created_at", "length_time", "pre_view", "author")
#         .distinct()
#     )
#     serializer_class = VideosSerializer
#     pagination_class = StandardResultsSetPagination

#     filter_backends = [
#         DjangoFilterBackend,
#         filters.OrderingFilter,
#         filters.SearchFilter,
#     ]
#     filterset_class = VideosFilter
#     search_fields = ["^name", "^author__username"]
#     ordering_fields = ["created_at", "length_time"]


class VideoDetailViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    lookup_field = "slug"
    serializer_class = OneVideoSerializer
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.select_related("author").prefetch_related(
        "tags", "vid_com__user_comment", "vid_com__children"
    )

    def get_queryset(self):
        return self.queryset.annotate(
            likes=Count(
                "user_video_relations",
                filter=Q(user_video_relations__vote=UserVideoRelation.LIKE),
            ),
            dislikes=Count(
                "user_video_relations",
                filter=Q(user_video_relations__vote=UserVideoRelation.DISLIKE),
            ),
        )


# class VideoDetailViewSet(ReadOnlyModelViewSet):
#     lookup_field = "slug"
#     serializer_class = OneVideoSerializer
#     queryset = Video.objects.select_related("author").prefetch_related(
#         "tags", "vid_com__user_comment", "vid_com__children"
#     )


#     def get_queryset(self):

#         return self.queryset.annotate(
#             likes=Count(
#                 "user_video_relations",
#                 filter=Q(user_video_relations__vote=UserVideoRelation.LIKE),
#             ),
#             dislikes=Count(
#                 "user_video_relations",
#                 filter=Q(user_video_relations__vote=UserVideoRelation.DISLIKE),
#             ),
#         )


# class VideoDetailViewSet(ReadOnlyModelViewSet):
#     lookup_field = "slug"
#     serializer_class = OneVideoSerializer

#     def get_queryset(self):
#         return (
#             Video.objects.prefetch_related(
#                 "tags", "vid_com__user_comment", "vid_com__children"
#             )
#             .select_related("author")
#             .annotate(
#                 likes=Count(
#                     "user_video_relations",
#                     filter=Q(user_video_relations__vote=UserVideoRelation.LIKE),
#                 ),
#                 dislikes=Count(
#                     "user_video_relations",
#                     filter=Q(user_video_relations__vote=UserVideoRelation.DISLIKE),
#                 ),
#             )
#         )


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
    queryset = Comment.objects.all()  # Задайте queryset для комментариев


class VideoCreateViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = VideoCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Video.objects.all()


class AuthorVideosViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = Video.objects.prefetch_related("tags").select_related("author")
    serializer_class = VideosSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        author = self.kwargs.get("author")
        return super().get_queryset().filter(author__username=author)


# class AuthorVideosViewSet(ViewSet):
#     lookup_field = "author"
#     pagination_class = StandardResultsSetPagination

#     def retrieve(self, request, author=None):
#         queryset = (
#             Video.objects.filter(author__username=author)
#             .prefetch_related("tags")
#             .select_related("author")
#             .only(
#                 "id", "name", "slug", "created_at", "length_time", "pre_view", "author"
#             )
#         )
#         paginator = self.pagination_class()
#         page = paginator.paginate_queryset(queryset, request)
#         if page is not None:
#             serializer = VideosSerializer(page, many=True)
#             return paginator.get_paginated_response(serializer.data)

#         serializer = VideosSerializer(queryset, many=True)
#         return Response(serializer.data)
