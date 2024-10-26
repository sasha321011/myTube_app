from django_filters import rest_framework as filters

from service.models import Video


class VideosFilter(filters.FilterSet):
    class Meta:
        model = Video
        fields = ["tags", "created_at", "length_time", "author", "tags"]
