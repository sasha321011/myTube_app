from django_filters import rest_framework as filters

from service.models import Video


class TagsFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class VideosFilter(filters.FilterSet):
    tags = TagsFilterInFilter(
        field_name="tags__tag_name", lookup_expr="in"
    )  # Правильное поле
    created_at = filters.DateFromToRangeFilter()  # Диапазон дат
    length_time = filters.AllValuesFilter()
    class Meta:
        model = Video
        fields = ["tags", "created_at"]
