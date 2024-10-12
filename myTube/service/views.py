
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from service.models import Video
from service.serializers import VideoSerializer


class VideoView(ModelViewSet):
    queryset = Video.objects.all().\
    prefetch_related('tags').\
    select_related('author').only('id',
                                  'name',
                                  'slug',
                                  'created_at',
                                  'length_time',
                                  'pre_view',
                                  'author')

    serializer_class = VideoSerializer
