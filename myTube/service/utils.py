from tabnanny import verbose
from django_filters import rest_framework as filters

from service.models import Video, UserVideoRelation


class VideosFilter(filters.FilterSet):
    liked_by_user = filters.BooleanFilter(method="filter_liked_by_user")

    class Meta:
        model = Video
        fields = ["tags", "author", "tags", "liked_by_user"]

    def filter_liked_by_user(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset

        if value:
            return queryset.filter(
                user_video_relations__user=user,
                user_video_relations__vote=UserVideoRelation.LIKE,
            )
        else:
            return queryset.filter(
                user_video_relations__user=user,
                user_video_relations__vote=UserVideoRelation.DISLIKE,
            )
        return queryset
